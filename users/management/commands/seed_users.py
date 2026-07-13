from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from users.models import Profile
from users.roles import (
    ROLE_CLIENT_OWNER,
    ROLE_FREELANCER,
    ROLE_INTERN,
    ROLE_MENTOR,
    ROLE_OFFICE,
    ROLE_PM,
    ROLE_SALES,
    ROLE_STUDENT,
    ROLE_SUPER_ADMIN,
    ROLE_WEB_DEV,
)

TEST_USERS = [
    ('admin', 'winningblueprints@gmail.com', 'admin1234', ROLE_SUPER_ADMIN, 'Super', 'Admin'),
    ('client1', 'winningblueprints@gmail.com', 'client1234', ROLE_CLIENT_OWNER, 'Test', 'Client'),
    ('student1', 'winningblueprints@gmail.com', 'student1234', ROLE_STUDENT, 'Test', 'Student'),
    ('intern1', 'winningblueprints@gmail.com', 'intern1234', ROLE_INTERN, 'Test', 'Intern'),
    ('pm1', 'winningblueprints@gmail.com', 'pm1234', ROLE_PM, 'Test', 'PM'),
    ('mentor1', 'winningblueprints@gmail.com', 'mentor1234', ROLE_MENTOR, 'Test', 'Mentor'),
    ('sales1', 'winningblueprints@gmail.com', 'sales1234', ROLE_SALES, 'Test', 'Sales'),
    ('office1', 'winningblueprints@gmail.com', 'office1234', ROLE_OFFICE, 'Office', 'Manager'),
    ('dev1', 'winningblueprints@gmail.com', 'dev1234', ROLE_WEB_DEV, 'Web', 'Developer'),
    ('freelance1', 'winningblueprints@gmail.com', 'free1234', ROLE_FREELANCER, 'Free', 'Lancer'),
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
