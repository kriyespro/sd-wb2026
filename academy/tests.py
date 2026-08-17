from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from . import fourd_services
from .courses_data import COURSES, price_amount
from .models import ActivityLog, AdmissionApplication, Attendance, StudentLead, StudentTask, Submission, TeachingSession
from .services import create_course_payment_order, get_student_attention_items, verify_course_payment


class StudentAttendanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('student1', 'student1@test.com', 'pass1234')
        self.user.profile.role = 'student'
        self.user.profile.save()
        self.client.login(username='student1', password='pass1234')

    def test_attendance_paginates_and_computes_rate_over_full_history(self):
        start = date(2026, 1, 1)
        for i in range(25):
            Attendance.objects.create(
                user=self.user,
                session_name=f'Session {i}',
                date=start + timedelta(days=i),
                status=Attendance.STATUS_PRESENT if i % 2 == 0 else Attendance.STATUS_ABSENT,
            )
        response = self.client.get(reverse('academy_dashboard:attendance'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b'Session '), 20)
        self.assertContains(response, 'Next')
        # Rate must reflect all 25 records (13 present / 25), not just the
        # first paginated page.
        self.assertContains(response, '52%')

        response = self.client.get(reverse('academy_dashboard:attendance') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b'Session '), 5)


class FourDScoreTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('student2', 'student2@test.com', 'pass1234')
        self.user.profile.role = 'student'
        self.user.profile.save()
        self.today = timezone.localdate()

    def test_no_evidence_scores_zero(self):
        self.assertEqual(fourd_services.daily_score(self.user, self.today), 0)
        self.assertEqual(fourd_services.score_level(0), 'at_risk')

    def test_each_pillar_contributes_its_weight(self):
        from .models import Assignment, Course

        course = Course.objects.create(title='SEO 101', slug='seo-101', description='x')
        assignment = Assignment.objects.create(course=course, title='Audit', description='x', due_date=self.today)
        Submission.objects.create(user=self.user, assignment=assignment, content='done')
        self.assertEqual(fourd_services.pillar_status(self.user, self.today)['learn'], True)
        self.assertEqual(fourd_services.daily_score(self.user, self.today), 25)

        TeachingSession.objects.create(user=self.user, topic='Canonical tags')
        self.assertEqual(fourd_services.daily_score(self.user, self.today), 45)

        StudentLead.objects.create(user=self.user, business_name='Acme Co')
        self.assertEqual(fourd_services.daily_score(self.user, self.today), 70)

        task = StudentTask.objects.create(
            user=self.user, title='Deliver audit', stage=StudentTask.STAGE_EARN,
        )
        from .services import mark_task_done
        mark_task_done(task)
        self.assertEqual(fourd_services.daily_score(self.user, self.today), 100)
        self.assertEqual(fourd_services.score_level(100), 'excellent')

    def test_earn_pillar_ignores_general_and_other_stage_tasks(self):
        task = StudentTask.objects.create(user=self.user, title='Generic', stage=StudentTask.STAGE_GENERAL)
        from .services import mark_task_done
        mark_task_done(task)
        self.assertFalse(fourd_services.pillar_status(self.user, self.today)['earn'])


class LeaderboardTests(TestCase):
    def test_orders_by_average_score_descending(self):
        high = User.objects.create_user('highscorer', 'high@test.com', 'pass1234')
        high.profile.role = 'student'
        high.profile.save()
        low = User.objects.create_user('lowscorer', 'low@test.com', 'pass1234')
        low.profile.role = 'student'
        low.profile.save()

        StudentLead.objects.create(user=high, business_name='Big Co', status=StudentLead.STATUS_WON)

        rows = fourd_services.get_leaderboard()
        usernames = [row['user'].username for row in rows]
        self.assertIn('highscorer', usernames)
        self.assertIn('lowscorer', usernames)
        self.assertGreaterEqual(
            rows[usernames.index('highscorer')]['avg_score'],
            rows[usernames.index('lowscorer')]['avg_score'],
        )

    def test_query_count_does_not_scale_with_student_count(self):
        # Regression guard: get_leaderboard/get_batch_health used to call
        # pillar_status()/rolling_average() once per student per day, which
        # blew up to 600+ queries on the ops /ops/academy-4d/ page with 20
        # active students. fourd_services now fetches evidence in bulk (one
        # query per evidence model), so query count must stay flat as the
        # student roster grows.
        for i in range(15):
            student = User.objects.create_user(f'scalestudent{i}', f'scalestudent{i}@test.com', 'pass1234')
            student.profile.role = 'student'
            student.profile.save()

        with self.assertNumQueries(8):
            fourd_services.get_leaderboard()
        with self.assertNumQueries(5):
            fourd_services.get_batch_health()


class TeachingSessionOwnershipTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('owner1', 'owner1@test.com', 'pass1234')
        self.owner.profile.role = 'student'
        self.owner.profile.save()
        self.other = User.objects.create_user('other1', 'other1@test.com', 'pass1234')
        self.other.profile.role = 'student'
        self.other.profile.save()

    def test_field_lead_status_update_scoped_to_owner(self):
        # get_object_or_404 raises Http404 for a non-owned pk; this app's
        # handler404 (core/views.py) redirects that to the public home page
        # rather than rendering a raw 404, so a 302-to-home is the signal
        # that the lookup was correctly scoped and nothing was mutated.
        lead = StudentLead.objects.create(user=self.owner, business_name='Acme')
        self.client.login(username='other1', password='pass1234')
        response = self.client.post(
            reverse('academy_dashboard:field_lead_status', args=[lead.pk]),
            {'status': StudentLead.STATUS_WON},
        )
        self.assertRedirects(response, reverse('website:home'))
        lead.refresh_from_db()
        self.assertEqual(lead.status, StudentLead.STATUS_NEW)

    def test_task_complete_scoped_to_owner(self):
        task = StudentTask.objects.create(user=self.owner, title='Do a thing')
        self.client.login(username='other1', password='pass1234')
        response = self.client.post(reverse('academy_dashboard:task_complete', args=[task.pk]))
        self.assertRedirects(response, reverse('website:home'))
        task.refresh_from_db()
        self.assertEqual(task.status, StudentTask.STATUS_TODO)


class FourDPageRenderTests(TestCase):
    """Jinja templates aren't validated at import time, only on render — hit
    every new/changed page once to catch template typos the test suite's
    other tests (which mostly POST and redirect) wouldn't exercise."""

    def setUp(self):
        self.user = User.objects.create_user('renderer', 'renderer@test.com', 'pass1234')
        self.user.profile.role = 'student'
        self.user.profile.save()
        self.client.login(username='renderer', password='pass1234')

    def test_new_and_updated_student_pages_render(self):
        for name in (
            'academy_dashboard:dashboard', 'academy_dashboard:fourd',
            'academy_dashboard:teaching', 'academy_dashboard:field_leads',
            'academy_dashboard:tasks', 'academy_dashboard:projects',
        ):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_ops_academy_4d_page_renders_for_mentor(self):
        mentor = User.objects.create_user('mentor3', 'mentor3@test.com', 'pass1234')
        mentor.profile.role = 'mentor'
        mentor.profile.save()
        self.client.login(username='mentor3', password='pass1234')
        TeachingSession.objects.create(user=self.user, topic='Rendering check')
        response = self.client.get(reverse('operations:academy_4d'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rendering check')


class TeachingEvaluateRoleGateTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user('gradee', 'gradee@test.com', 'pass1234')
        self.student.profile.role = 'student'
        self.student.profile.save()
        self.session = TeachingSession.objects.create(user=self.student, topic='SEO basics')

    def test_non_academy_ops_role_cannot_evaluate(self):
        sales = User.objects.create_user('sales_person', 'sales@test.com', 'pass1234')
        sales.profile.role = 'sales_executive'
        sales.profile.save()
        self.client.login(username='sales_person', password='pass1234')
        response = self.client.post(
            reverse('operations:teaching_evaluate', args=[self.session.pk]),
            {'score': 90, 'feedback': ''},
        )
        self.assertEqual(response.status_code, 302)
        self.session.refresh_from_db()
        self.assertEqual(self.session.status, TeachingSession.STATUS_SUBMITTED)

    def test_mentor_can_evaluate(self):
        mentor = User.objects.create_user('mentor2', 'mentor2@test.com', 'pass1234')
        mentor.profile.role = 'mentor'
        mentor.profile.save()
        self.client.login(username='mentor2', password='pass1234')
        response = self.client.post(
            reverse('operations:teaching_evaluate', args=[self.session.pk]),
            {'score': 90, 'feedback': 'Great job'},
        )
        self.assertEqual(response.status_code, 302)
        self.session.refresh_from_db()
        self.assertEqual(self.session.status, TeachingSession.STATUS_EVALUATED)
        self.assertEqual(self.session.score, 90)


class ScoreHistoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('historian', 'historian@test.com', 'pass1234')
        self.user.profile.role = 'student'
        self.user.profile.save()

    def test_history_covers_requested_range_oldest_first(self):
        history = fourd_services.get_score_history(self.user, days=5)
        self.assertEqual(len(history), 5)
        self.assertEqual(history[-1]['date'], timezone.localdate())
        self.assertEqual(history[0]['date'], timezone.localdate() - timedelta(days=4))
        self.assertTrue(all(day['score'] == 0 for day in history))

    def test_todays_evidence_reflected_in_last_entry(self):
        StudentLead.objects.create(user=self.user, business_name='Acme')
        history = fourd_services.get_score_history(self.user, days=3)
        self.assertEqual(history[-1]['score'], 25)
        self.assertTrue(history[-1]['pillars']['field'])


class ActivityLogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('journaler', 'journaler@test.com', 'pass1234')
        self.user.profile.role = 'student'
        self.user.profile.save()
        self.client.login(username='journaler', password='pass1234')

    def test_activity_log_does_not_affect_score(self):
        # Guards the explicit product decision: the free-form journal is
        # descriptive only, never scoring evidence.
        self.assertEqual(fourd_services.daily_score(self.user), 0)
        ActivityLog.objects.create(user=self.user, pillar='field', title='Called 5 shops')
        self.assertEqual(fourd_services.daily_score(self.user), 0)
        self.assertFalse(fourd_services.pillar_status(self.user, timezone.localdate())['field'])

    def test_activity_feed_merges_and_sorts_all_sources(self):
        from .models import Assignment, Course

        course = Course.objects.create(title='Ads 101', slug='ads-101', description='x')
        assignment = Assignment.objects.create(
            course=course, title='Campaign audit', description='x', due_date=timezone.localdate(),
        )
        Submission.objects.create(user=self.user, assignment=assignment, content='done')
        TeachingSession.objects.create(user=self.user, topic='Bid strategies')
        StudentLead.objects.create(user=self.user, business_name='Acme')
        ActivityLog.objects.create(user=self.user, pillar='learn', title='Read a case study')

        feed = fourd_services.get_activity_feed(self.user)
        sources = {item['source'] for item in feed}
        self.assertEqual(sources, {'submission', 'teaching', 'lead', 'note'})
        timestamps = [item['timestamp'] for item in feed]
        self.assertEqual(timestamps, sorted(timestamps, reverse=True))

    def test_activity_add_scoped_to_authenticated_user(self):
        response = self.client.post(reverse('academy_dashboard:activity_add'), {
            'pillar': 'earn', 'title': 'Followed up with a client', 'details': '',
        })
        self.assertRedirects(response, reverse('academy_dashboard:fourd'))
        log = ActivityLog.objects.get(title='Followed up with a client')
        self.assertEqual(log.user, self.user)


class StudentProgressStaffViewTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user('progressee', 'progressee@test.com', 'pass1234')
        self.student.profile.role = 'student'
        self.student.profile.save()
        self.mentor = User.objects.create_user('mentor4', 'mentor4@test.com', 'pass1234')
        self.mentor.profile.role = 'mentor'
        self.mentor.profile.save()

    def test_renders_for_a_real_student(self):
        self.client.login(username='mentor4', password='pass1234')
        response = self.client.get(reverse('operations:student_progress', args=[self.student.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'progressee')

    def test_404s_for_a_non_student_pk(self):
        self.client.login(username='mentor4', password='pass1234')
        response = self.client.get(reverse('operations:student_progress', args=[self.mentor.pk]))
        self.assertRedirects(response, reverse('website:home'))


class ProgressPageRenderTests(TestCase):
    def test_student_progress_page_renders(self):
        user = User.objects.create_user('progressview', 'progressview@test.com', 'pass1234')
        user.profile.role = 'student'
        user.profile.save()
        self.client.login(username='progressview', password='pass1234')
        response = self.client.get(reverse('academy_dashboard:progress'))
        self.assertEqual(response.status_code, 200)


class StudentAttentionItemsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('attentionstudent', 'attn@test.com', 'pass1234')
        self.user.profile.role = 'student'
        self.user.profile.save()
        self.client.login(username='attentionstudent', password='pass1234')

    def test_all_clear_when_nothing_needs_attention(self):
        # Logging teaching evidence today satisfies the "teach" pillar so the
        # 4D nudge does not fire, leaving a genuinely empty attention list.
        TeachingSession.objects.create(user=self.user, topic='Warm intro')
        self.assertEqual(get_student_attention_items(self.user), [])

        response = self.client.get(reverse('academy_dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All clear')

    def test_pending_assignment_surfaced(self):
        from .models import Assignment, Course, Enrollment

        course = Course.objects.create(title='Ads 101', slug='ads-101-attn', description='x')
        Enrollment.objects.create(user=self.user, course=course)
        Assignment.objects.create(
            course=course, title='Audit', description='x', due_date=timezone.localdate(),
        )
        items = get_student_attention_items(self.user)
        tones = {item['href_name']: item['tone'] for item in items}
        self.assertEqual(tones['academy_dashboard:assignments'], 'amber')

    def test_streak_at_risk_when_yesterday_logged_but_not_today(self):
        yesterday = timezone.now() - timedelta(days=1)
        StudentTask.objects.create(
            user=self.user, title='Deliver', stage=StudentTask.STAGE_EARN,
            status=StudentTask.STATUS_DONE, completed_at=yesterday,
        )
        items = get_student_attention_items(self.user)
        fourd_item = next(i for i in items if i['href_name'] == 'academy_dashboard:fourd')
        self.assertEqual(fourd_item['tone'], 'orange')
        self.assertIn('streak at risk', fourd_item['label'])

    def test_no_history_gives_plain_log_nudge_not_streak_warning(self):
        items = get_student_attention_items(self.user)
        fourd_item = next(i for i in items if i['href_name'] == 'academy_dashboard:fourd')
        self.assertIn("Log today's 4D", fourd_item['label'])
        self.assertNotIn('streak at risk', fourd_item['label'])

    def test_new_teaching_feedback_surfaced(self):
        TeachingSession.objects.create(
            user=self.user, topic='Bidding', status=TeachingSession.STATUS_EVALUATED,
            evaluated_at=timezone.now(), score=90,
        )
        items = get_student_attention_items(self.user)
        tones = {item['href_name']: item['tone'] for item in items}
        self.assertEqual(tones['academy_dashboard:teaching'], 'emerald')

    def test_old_teaching_feedback_not_surfaced(self):
        TeachingSession.objects.create(
            user=self.user, topic='Old', status=TeachingSession.STATUS_EVALUATED,
            evaluated_at=timezone.now() - timedelta(days=10), score=80,
        )
        items = get_student_attention_items(self.user)
        self.assertFalse(any(i['href_name'] == 'academy_dashboard:teaching' for i in items))

    def test_new_field_lead_needs_follow_up(self):
        StudentLead.objects.create(user=self.user, business_name='Acme Co')
        items = get_student_attention_items(self.user)
        tones = {item['href_name']: item['tone'] for item in items}
        self.assertEqual(tones['academy_dashboard:field_leads'], 'teal')


class CourseDetailPageRenderTests(TestCase):
    def test_course_detail_renders_with_enroll_form(self):
        course = COURSES[0]
        response = self.client.get(reverse('academy:course_detail', kwargs={'slug': course['slug']}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enroll')


class CoursePaymentServiceTests(TestCase):
    def setUp(self):
        self.course = COURSES[0]

    def test_price_amount_parses_display_string(self):
        self.assertEqual(price_amount({'price': '₹16,999'}), Decimal('16999'))

    @patch('core.razorpay_utils.get_razorpay_client')
    def test_create_course_payment_order_creates_application_and_order(self, mock_get_client):
        mock_client = MagicMock()
        expected_amount_paise = int(price_amount(self.course) * 100)
        mock_client.order.create.return_value = {'id': 'order_COURSE1', 'amount': expected_amount_paise}
        mock_get_client.return_value = mock_client

        application, order = create_course_payment_order(self.course, {
            'name': 'Riya Shah', 'email': 'riya@example.com', 'phone': '9876543210',
        })

        self.assertEqual(order['id'], 'order_COURSE1')
        self.assertEqual(application.course_interest, self.course['title'])
        self.assertEqual(application.razorpay_order_id, 'order_COURSE1')
        self.assertEqual(application.amount, price_amount(self.course))
        self.assertIsNone(application.paid_at)

    @patch('core.razorpay_utils.get_razorpay_client')
    def test_verify_course_payment_success_marks_paid_and_advances_status(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        application = AdmissionApplication.objects.create(
            name='Riya Shah', email='riya@example.com', phone='9876543210',
            course_interest=self.course['title'], motivation='Direct payment',
            razorpay_order_id='order_COURSE1', amount=price_amount(self.course),
        )

        verify_course_payment(application, 'order_COURSE1', 'pay_COURSE1', 'sig_COURSE1')

        application.refresh_from_db()
        self.assertEqual(application.razorpay_payment_id, 'pay_COURSE1')
        self.assertIsNotNone(application.paid_at)
        self.assertEqual(application.status, AdmissionApplication.STATUS_REVIEW)

    def test_verify_course_payment_rejects_order_mismatch(self):
        application = AdmissionApplication.objects.create(
            name='Riya Shah', email='riya@example.com', phone='9876543210',
            course_interest=self.course['title'], motivation='Direct payment',
            razorpay_order_id='order_REAL', amount=price_amount(self.course),
        )
        with self.assertRaises(ValueError):
            verify_course_payment(application, 'order_FAKE', 'pay_x', 'sig_x')
        application.refresh_from_db()
        self.assertIsNone(application.paid_at)


class CourseEnrollViewTests(TestCase):
    def setUp(self):
        self.course = COURSES[0]

    @patch('academy.views.create_course_payment_order')
    def test_enroll_pay_view_renders_checkout_launch(self, mock_create_order):
        application = AdmissionApplication.objects.create(
            name='Riya Shah', email='riya@example.com', phone='9876543210',
            course_interest=self.course['title'], motivation='Direct payment',
        )
        mock_create_order.return_value = (application, {'id': 'order_COURSE2', 'amount': 1699900})
        url = reverse('academy:enroll_pay', kwargs={'slug': self.course['slug']})
        response = self.client.post(url, {
            'name': 'Riya Shah', 'email': 'riya@example.com', 'phone': '9876543210',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'order_COURSE2')

    def test_enroll_pay_view_404s_for_unknown_course(self):
        url = reverse('academy:enroll_pay', kwargs={'slug': 'does-not-exist'})
        response = self.client.post(url, {
            'name': 'Riya Shah', 'email': 'riya@example.com', 'phone': '9876543210',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('website:home'))

    def test_enroll_pay_view_rejects_invalid_form(self):
        url = reverse('academy:enroll_pay', kwargs={'slug': self.course['slug']})
        response = self.client.post(url, {'name': '', 'email': 'not-an-email', 'phone': ''})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'checkout.razorpay.com')

    @patch('academy.views.verify_course_payment')
    def test_enroll_verify_view_success(self, mock_verify):
        application = AdmissionApplication.objects.create(
            name='Riya Shah', email='riya@example.com', phone='9876543210',
            course_interest=self.course['title'], motivation='Direct payment',
            razorpay_order_id='order_COURSE3', amount=price_amount(self.course),
        )
        mock_verify.return_value = application
        url = reverse('academy:enroll_verify', kwargs={'slug': self.course['slug'], 'pk': application.pk})
        response = self.client.post(url, {
            'razorpay_order_id': 'order_COURSE3', 'razorpay_payment_id': 'pay_x', 'razorpay_signature': 'sig_x',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Payment received')

    def test_enroll_verify_view_bad_signature_shows_error_page(self):
        application = AdmissionApplication.objects.create(
            name='Riya Shah', email='riya@example.com', phone='9876543210',
            course_interest=self.course['title'], motivation='Direct payment',
            razorpay_order_id='order_COURSE4', amount=price_amount(self.course),
        )
        url = reverse('academy:enroll_verify', kwargs={'slug': self.course['slug'], 'pk': application.pk})
        response = self.client.post(url, {
            'razorpay_order_id': 'order_MISMATCH', 'razorpay_payment_id': 'pay_x', 'razorpay_signature': 'sig_x',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'could not be verified')
