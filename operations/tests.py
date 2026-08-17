from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.roles import ROLE_FREELANCER, ROLE_PM, ROLE_SALES, ROLE_SUPER_ADMIN
from partners.models import PartnerLead, PartnerProfile
from website.models import JobApplication, Lead

from . import services


class LeadPipelineTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin', 'admin@test.com', 'pass1234')
        self.admin.is_superuser = True
        self.admin.save()
        self.admin.profile.role = ROLE_SUPER_ADMIN
        self.admin.profile.save()
        self.sales = User.objects.create_user('sales1', 'sales@test.com', 'pass1234')
        self.sales.profile.role = ROLE_SALES
        self.sales.profile.save()
        self.freelancer = User.objects.create_user('free1', 'free@test.com', 'pass1234')
        self.freelancer.profile.role = ROLE_FREELANCER
        self.freelancer.profile.save()
        self.lead = Lead.objects.create(
            name='Pipeline Lead',
            email='pipeline@example.com',
            company='Acme',
            service_interest='SEO',
        )
        self.client.login(username='admin', password='pass1234')

    def test_pipeline_counts_use_a_single_grouped_query(self):
        # Regression guard: get_lead_pipeline_counts() used to run one
        # .count() query per status choice (6 queries on the /ops/ mission
        # control page load). It must now use a single GROUP BY query.
        for status, _ in Lead.STATUS_CHOICES:
            Lead.objects.create(
                name=f'Lead {status}', email=f'{status}@example.com', status=status,
            )
        with self.assertNumQueries(1):
            counts = services.get_lead_pipeline_counts()
        self.assertEqual(counts[Lead.STATUS_QUALIFIED], 1)

    def test_lead_status_update(self):
        url = reverse('operations:lead_status', kwargs={'pk': self.lead.pk})
        response = self.client.post(url, {'status': Lead.STATUS_QUALIFIED})
        self.assertEqual(response.status_code, 200)
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.status, Lead.STATUS_QUALIFIED)

    def test_lead_assign(self):
        url = reverse('operations:lead_assign', kwargs={'pk': self.lead.pk})
        response = self.client.post(url, {'assigned_to': self.sales.pk})
        self.assertEqual(response.status_code, 200)
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.assigned_to_id, self.sales.pk)

    def test_lead_convert(self):
        url = reverse('operations:lead_convert', kwargs={'pk': self.lead.pk})
        response = self.client.post(url, {'project_name': 'Acme SEO Project'})
        self.assertEqual(response.status_code, 200)
        self.lead.refresh_from_db()
        self.assertTrue(self.lead.is_converted)
        self.assertEqual(self.lead.status, Lead.STATUS_WON)

    def test_leads_view_forbidden_for_non_office_desk_role(self):
        """A random ops role (e.g. freelancer) must not see or act on leads —
        that's office-desk-only (sales/office/account-manager/director)."""
        self.client.login(username='free1', password='pass1234')
        self.assertEqual(self.client.get(reverse('operations:leads')).status_code, 302)
        self.assertEqual(
            self.client.post(
                reverse('operations:lead_convert', kwargs={'pk': self.lead.pk}),
                {'project_name': 'Should not happen'},
            ).status_code,
            302,
        )
        self.lead.refresh_from_db()
        self.assertFalse(self.lead.is_converted)

    def test_allocation_create_forbidden_for_non_management_role(self):
        """Any ops role assigning themselves/others as PM would be a
        privilege-escalation path if not restricted to PM/office/director."""
        from clients.models import ClientAccount
        from projects.models import Project

        owner = User.objects.create_user('client_owner1', 'owner1@test.com', 'pass1234')
        account = ClientAccount.objects.create(user=owner, company_name='Escalation Co')
        project = Project.objects.create(client_account=account, name='Escalation Test Project')
        self.client.login(username='free1', password='pass1234')
        response = self.client.post(reverse('operations:allocation_add'), {
            'project': project.pk,
            'user': self.freelancer.pk,
            'role': 'pm',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(project.assignments.exists())

    def test_allocation_create_allowed_for_pm_role(self):
        from clients.models import ClientAccount
        from projects.models import Project

        pm_user = User.objects.create_user('pm1', 'pm1@test.com', 'pass1234')
        pm_user.profile.role = ROLE_PM
        pm_user.profile.save()
        owner = User.objects.create_user('client_owner2', 'owner2@test.com', 'pass1234')
        account = ClientAccount.objects.create(user=owner, company_name='Allowed Co')
        project = Project.objects.create(client_account=account, name='Allowed Allocation Project')
        self.client.login(username='pm1', password='pass1234')
        response = self.client.post(reverse('operations:allocation_add'), {
            'project': project.pk,
            'user': pm_user.pk,
            'role': 'pm',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(project.assignments.exists())

    def test_mission_control_live_partial(self):
        response = self.client.get(reverse('operations:live_mission'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ops-stats-bar', response.content)
        self.assertIn(b'Pipeline Lead', response.content)

    def test_leads_live_partial(self):
        response = self.client.get(reverse('operations:live_leads'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lead-', response.content)
        self.assertIn(b'Pipeline Lead', response.content)

    def test_job_applications_superuser_table(self):
        JobApplication.objects.create(
            name='Applicant One',
            email='applicant@example.com',
            phone='9999999999',
            role='Meta Ads Specialist',
            cover_letter='I want this role.',
        )
        response = self.client.get(reverse('operations:job_applications'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Applicant One')
        self.assertContains(response, 'Meta Ads Specialist')
        self.assertContains(response, '<table')

    def test_job_applications_sales_forbidden(self):
        self.client.login(username='sales1', password='pass1234')
        response = self.client.get(reverse('operations:job_applications'))
        self.assertEqual(response.status_code, 302)

    def test_dgc_leads_superuser_table(self):
        from users.roles import ROLE_PARTNER

        partner_user = User.objects.create_user('dgcops', 'dgcops@test.com', 'pass1234')
        partner_user.profile.role = ROLE_PARTNER
        partner_user.profile.save()
        partner = PartnerProfile.objects.create(user=partner_user, code='DGCOPS1')
        PartnerLead.objects.create(
            partner=partner,
            name='Ops Visible Lead',
            phone='9000000001',
            company='Visible Mills',
            interest='D2C',
        )
        response = self.client.get(reverse('operations:dgc_leads'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ops Visible Lead')
        self.assertContains(response, 'DGCOPS1')
        self.assertContains(response, '<table')

    def test_dgc_leads_sales_forbidden(self):
        self.client.login(username='sales1', password='pass1234')
        response = self.client.get(reverse('operations:dgc_leads'))
        self.assertEqual(response.status_code, 302)

    def test_dgc_lead_status_won_creates_commission(self):
        from decimal import Decimal

        from users.roles import ROLE_PARTNER

        partner_user = User.objects.create_user('dgcops2', 'dgcops2@test.com', 'pass1234')
        partner_user.profile.role = ROLE_PARTNER
        partner_user.profile.save()
        partner = PartnerProfile.objects.create(user=partner_user, code='DGCOPS2')
        lead = PartnerLead.objects.create(
            partner=partner,
            name='Won Via Ops',
            phone='9000000002',
            deal_value=Decimal('10000.00'),
            status=PartnerLead.STATUS_NEW,
        )
        url = reverse('operations:dgc_lead_status', kwargs={'pk': lead.pk})
        response = self.client.post(url, {'status': PartnerLead.STATUS_WON})
        self.assertEqual(response.status_code, 200)
        lead.refresh_from_db()
        self.assertEqual(lead.status, PartnerLead.STATUS_WON)
        self.assertTrue(lead.commissions.exists())
        self.assertEqual(lead.commissions.first().amount, Decimal('2000.00'))

    def test_dgc_orders_page_and_status(self):
        from decimal import Decimal

        from partners.models import PartnerOrder, ResellerOffer
        from users.roles import ROLE_PARTNER

        partner_user = User.objects.create_user('dgcord', 'dgcord@test.com', 'pass1234')
        partner_user.profile.role = ROLE_PARTNER
        partner_user.profile.save()
        partner = PartnerProfile.objects.create(user=partner_user, code='DGCORD1')
        offer = ResellerOffer.objects.create(
            title='Ops Offer',
            price=Decimal('15000.00'),
            commission_percent=Decimal('0.00'),
        )
        order = PartnerOrder.objects.create(
            partner=partner,
            offer=offer,
            quantity=1,
            unit_price=offer.price,
            total=offer.price,
        )
        response = self.client.get(reverse('operations:dgc_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ops Offer')
        self.assertContains(response, 'DGCORD1')

        url = reverse('operations:dgc_order_status', kwargs={'pk': order.pk})
        response = self.client.post(
            url,
            {'status': PartnerOrder.STATUS_FULFILLED},
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, PartnerOrder.STATUS_FULFILLED)

        self.client.login(username='sales1', password='pass1234')
        self.assertEqual(self.client.get(reverse('operations:dgc_orders')).status_code, 302)

    def test_assignee_cannot_cancel_order_only_ops_can(self):
        """A delivery assignee can move their own order forward but must not
        be able to cancel it — cancelling voids the partner's commission,
        which is an ops-management decision."""
        from decimal import Decimal

        from partners.models import PartnerOrder, ResellerOffer
        from partners.services import place_order
        from users.roles import ROLE_PARTNER

        partner_user = User.objects.create_user('dgcord2', 'dgcord2@test.com', 'pass1234')
        partner_user.profile.role = ROLE_PARTNER
        partner_user.profile.save()
        partner = PartnerProfile.objects.create(user=partner_user, code='DGCORD2')
        offer = ResellerOffer.objects.create(
            title='Ops Offer 2',
            price=Decimal('15000.00'),
            commission_percent=Decimal('10.00'),
        )
        order = place_order(partner, offer, quantity=1)
        order.assigned_to = self.freelancer
        order.save(update_fields=['assigned_to'])

        self.client.login(username='free1', password='pass1234')
        url = reverse('operations:dgc_order_status', kwargs={'pk': order.pk})
        response = self.client.post(url, {'status': PartnerOrder.STATUS_CANCELLED})
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertNotEqual(order.status, PartnerOrder.STATUS_CANCELLED)
        self.assertTrue(order.commissions.exists())

        # The assignee can still move it forward legitimately.
        response = self.client.post(url, {'status': PartnerOrder.STATUS_FULFILLED})
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, PartnerOrder.STATUS_FULFILLED)

        # Ops/superuser retains the ability to cancel.
        self.client.login(username='admin', password='pass1234')
        response = self.client.post(url, {'status': PartnerOrder.STATUS_CANCELLED})
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, PartnerOrder.STATUS_CANCELLED)
        self.assertFalse(order.commissions.exists())

    def test_academy_views_forbidden_for_non_academy_ops_role(self):
        """Mentor Allocation, 4D Academy batch dashboard, and per-student
        progress must stay restricted to academy staff — a random ops role
        (freelancer) shouldn't be able to browse student scores/mentor
        pairings."""
        from academy.models import StudentTask
        from users.roles import ROLE_STUDENT

        student = User.objects.create_user('stud_ops1', 'stud_ops1@test.com', 'pass1234')
        student.profile.role = ROLE_STUDENT
        student.profile.save()

        self.client.login(username='free1', password='pass1234')
        self.assertEqual(self.client.get(reverse('operations:mentors')).status_code, 302)
        self.assertEqual(self.client.get(reverse('operations:academy_4d')).status_code, 302)
        self.assertEqual(
            self.client.get(
                reverse('operations:student_progress', kwargs={'pk': student.pk}),
            ).status_code,
            302,
        )

        self.client.login(username='admin', password='pass1234')
        self.assertEqual(self.client.get(reverse('operations:mentors')).status_code, 200)
        self.assertEqual(self.client.get(reverse('operations:academy_4d')).status_code, 200)

    def test_performance_view_forbidden_for_non_management_role(self):
        """Performance reviews are confidential — restricted to
        director/office-manager/PM management roles, not every ops role."""
        self.client.login(username='free1', password='pass1234')
        self.assertEqual(self.client.get(reverse('operations:performance')).status_code, 302)

        self.client.login(username='admin', password='pass1234')
        self.assertEqual(self.client.get(reverse('operations:performance')).status_code, 200)

    def test_ops2_mission_control(self):
        response = self.client.get(reverse('ops2:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mission Control')
        live = self.client.get(reverse('ops2:live'))
        self.assertEqual(live.status_code, 200)
        self.assertIn(b'ops2-kpi', live.content)
