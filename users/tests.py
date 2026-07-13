from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from clients.models import ClientAccount
from partners.models import PartnerProfile
from users.roles import ROLE_CLIENT_OWNER, ROLE_PARTNER, ROLE_PM, ROLE_STUDENT
from users.services import (
    PUBLIC_SIGNUP_ROLES,
    SESSION_NEEDS_ROLE,
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
        self.assertContains(r, 'DGC Partner')

    def test_signup_page_prefills_role(self):
        r = self.client.get(reverse('users:signup') + '?role=student')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'value="student"')

    def test_email_signup_client(self):
        r = self.client.post(reverse('users:signup'), {
            'role': ROLE_CLIENT_OWNER,
            'first_name': 'Riya',
            'last_name': 'Shah',
            'email': 'riya@example.com',
            'phone': '9999999999',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(r.status_code, 302)
        user = User.objects.get(email='riya@example.com')
        self.assertEqual(user.profile.role, ROLE_CLIENT_OWNER)
        self.assertTrue(ClientAccount.objects.filter(user=user).exists())
        self.assertEqual(r.url, reverse('clients:dashboard'))

    def test_email_signup_partner(self):
        r = self.client.post(reverse('users:signup'), {
            'role': ROLE_PARTNER,
            'first_name': 'Dev',
            'email': 'devpartner@example.com',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(r.status_code, 302)
        user = User.objects.get(email='devpartner@example.com')
        self.assertEqual(user.profile.role, ROLE_PARTNER)
        self.assertTrue(PartnerProfile.objects.filter(user=user).exists())
        self.assertEqual(r.url, reverse('partners:dashboard'))

    def test_rejects_duplicate_email(self):
        User.objects.create_user('exist', 'exist@example.com', 'pass12345')
        r = self.client.post(reverse('users:signup'), {
            'role': ROLE_STUDENT,
            'first_name': 'X',
            'email': 'exist@example.com',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'already exists')

    def test_choose_role_after_flag(self):
        user = User.objects.create_user('newg', 'newg@example.com', 'pass12345')
        self.client.force_login(user)
        session = self.client.session
        session[SESSION_NEEDS_ROLE] = True
        session.save()
        r = self.client.post(reverse('users:choose_role'), {'role': ROLE_STUDENT})
        self.assertEqual(r.status_code, 302)
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.role, ROLE_STUDENT)
        self.assertEqual(r.url, reverse('academy_dashboard:dashboard'))

    def test_google_start_stores_role(self):
        r = self.client.get(reverse('users:google_start') + '?role=partner')
        self.assertEqual(r.status_code, 302)
        self.assertIn('/accounts/google/login/', r.url)
        self.assertEqual(self.client.session.get('signup_role'), ROLE_PARTNER)

    def test_login_still_redirects_by_portal(self):
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
