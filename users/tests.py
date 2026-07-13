from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from clients.models import ClientAccount
from partners.models import PartnerProfile
from users.roles import ROLE_CLIENT_OWNER, ROLE_PARTNER, ROLE_PM, ROLE_STUDENT
from users.services import (
    PUBLIC_SIGNUP_ROLES,
    SESSION_SIGNUP_ROLE,
    create_public_user,
    provision_public_signup,
)


class ProvisionPublicSignupTests(TestCase):
    def test_client_gets_account(self):
        user = User.objects.create_user('biz', 'biz@example.com', 'pass12345')
        provision_public_signup(user, ROLE_CLIENT_OWNER)
        user.refresh_from_db()
        self.assertEqual(user.profile.role, ROLE_CLIENT_OWNER)
        self.assertTrue(ClientAccount.objects.filter(user=user).exists())

    def test_student_role_only(self):
        user = User.objects.create_user('stu', 'stu@example.com', 'pass12345')
        provision_public_signup(user, ROLE_STUDENT)
        self.assertEqual(user.profile.role, ROLE_STUDENT)
        self.assertFalse(ClientAccount.objects.filter(user=user).exists())
        self.assertFalse(PartnerProfile.objects.filter(user=user).exists())

    def test_partner_gets_profile(self):
        user = User.objects.create_user('dgc', 'dgc@example.com', 'pass12345')
        provision_public_signup(user, ROLE_PARTNER)
        self.assertEqual(user.profile.role, ROLE_PARTNER)
        partner = PartnerProfile.objects.get(user=user)
        self.assertTrue(partner.code)
        self.assertFalse(partner.is_active)

    def test_rejects_staff_role(self):
        user = User.objects.create_user('pm', 'pm@example.com', 'pass12345')
        with self.assertRaises(ValueError):
            provision_public_signup(user, ROLE_PM)

    def test_create_public_user(self):
        user = create_public_user(
            email='owner@example.com',
            password='pass12345',
            role=ROLE_CLIENT_OWNER,
            first_name='Ada',
        )
        self.assertEqual(user.profile.role, ROLE_CLIENT_OWNER)
        self.assertTrue(ClientAccount.objects.filter(user=user).exists())
        self.assertIn(ROLE_CLIENT_OWNER, PUBLIC_SIGNUP_ROLES)


class SignupViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_join_page(self):
        r = self.client.get(reverse('website:join'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Client portal')
        self.assertContains(r, 'Continue with Google')

    def test_signup_page_prefills_role(self):
        r = self.client.get(reverse('users:signup') + '?role=student')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'value="student"')
        self.assertContains(r, 'Continue with Google')
        self.assertNotContains(r, 'Confirm password')

    def test_signup_post_starts_google(self):
        r = self.client.post(reverse('users:signup'), {'role': ROLE_PARTNER})
        self.assertEqual(r.status_code, 302)
        self.assertIn('/accounts/google/login/', r.url)
        self.assertEqual(self.client.session.get(SESSION_SIGNUP_ROLE), ROLE_PARTNER)

    def test_signup_post_requires_role(self):
        r = self.client.post(reverse('users:signup'), {})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Please choose how you are joining')

    def test_choose_role_after_flag(self):
        user = User.objects.create_user('newg', 'newg@example.com', 'pass12345')
        user.profile.role_confirmed = False
        user.profile.save(update_fields=['role_confirmed'])
        self.client.force_login(user)
        r = self.client.post(reverse('users:choose_role'), {'role': ROLE_STUDENT})
        self.assertEqual(r.status_code, 302)
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.role, ROLE_STUDENT)
        self.assertTrue(user.profile.role_confirmed)
        self.assertEqual(r.url, reverse('academy_dashboard:dashboard'))

    def test_lost_session_still_forces_role_choice(self):
        """Even if the session flag never gets set (e.g. session lost after
        Google OAuth), an unconfirmed profile must not fall through to the
        default client_owner portal."""
        user = User.objects.create_user('newg2', 'newg2@example.com', 'pass12345')
        user.profile.role_confirmed = False
        user.profile.save(update_fields=['role_confirmed'])
        self.client.force_login(user)
        r = self.client.get(reverse('users:dashboard_redirect'))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('users:choose_role'))

    def test_google_start_stores_role(self):
        r = self.client.get(reverse('users:google_start') + '?role=partner')
        self.assertEqual(r.status_code, 302)
        self.assertIn('/accounts/google/login/', r.url)
        self.assertEqual(self.client.session.get('signup_role'), ROLE_PARTNER)

    def test_staff_password_login_still_works(self):
        user = create_public_user(
            email='stu2@example.com',
            password='securepass1',
            role=ROLE_STUDENT,
            first_name='Stu',
        )
        r = self.client.post(reverse('users:login'), {
            'username': user.username,
            'password': 'securepass1',
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('academy_dashboard:dashboard'))


@override_settings(ROOT_URLCONF='core.urls')
class LoginPageTests(TestCase):
    def test_login_has_google_and_join(self):
        r = self.client.get(reverse('users:login'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Continue with Google')
        self.assertContains(r, reverse('website:join'))
        self.assertContains(r, 'Staff? Sign in with username')
