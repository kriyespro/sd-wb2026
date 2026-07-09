from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from users.models import Profile
from users.roles import (
    ROLE_CLIENT_OWNER,
    ROLE_INTERN,
    ROLE_MENTOR,
    ROLE_PM,
    ROLE_SALES,
    ROLE_STUDENT,
    ROLE_SUPER_ADMIN,
)

TEST_USERS = [
    ('admin', 'admin@winningblueprints.in', 'admin1234', ROLE_SUPER_ADMIN, 'Super', 'Admin'),
    ('client1', 'client@example.com', 'client1234', ROLE_CLIENT_OWNER, 'Test', 'Client'),
    ('student1', 'student@example.com', 'student1234', ROLE_STUDENT, 'Test', 'Student'),
    ('intern1', 'intern@example.com', 'intern1234', ROLE_INTERN, 'Test', 'Intern'),
    ('pm1', 'pm@winningblueprints.in', 'pm1234', ROLE_PM, 'Test', 'PM'),
    ('mentor1', 'mentor@winningblueprints.in', 'mentor1234', ROLE_MENTOR, 'Test', 'Mentor'),
    ('sales1', 'sales@winningblueprints.in', 'sales1234', ROLE_SALES, 'Test', 'Sales'),
]


class Command(BaseCommand):
    help = 'Create test users for each portal'

    def handle(self, *args, **options):
        for username, email, password, role, first, last in TEST_USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'first_name': first, 'last_name': last},
            )
            user.email = email
            user.first_name = first
            user.last_name = last
            user.set_password(password)
            user.is_staff = role == ROLE_SUPER_ADMIN
            user.is_superuser = role == ROLE_SUPER_ADMIN
            user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} {username} ({role}) — password: {password}')

        self.stdout.write(self.style.SUCCESS('Test users ready. See test_user.txt'))
