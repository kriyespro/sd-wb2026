from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Attendance


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
