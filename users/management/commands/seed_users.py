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

# No 'admin' entry here on purpose — this command is safe to re-run on
# production, and a demo row named 'admin' would collide with (and silently
# reset the password of) a real live super admin login of the same username.
# Create real admin accounts separately, never through this seed command.
TEST_USERS = [
    ('client1', 'winningblueprints@gmail.com', 'Client#Demo2026!', ROLE_CLIENT_OWNER, 'Test', 'Client'),
    ('student1', 'winningblueprints@gmail.com', 'Student#Demo2026!', ROLE_STUDENT, 'Test', 'Student'),
    ('intern1', 'winningblueprints@gmail.com', 'Intern#Demo2026!', ROLE_INTERN, 'Test', 'Intern'),
    ('pm1', 'winningblueprints@gmail.com', 'ProjectMgr#Demo2026!', ROLE_PM, 'Test', 'PM'),
    ('mentor1', 'winningblueprints@gmail.com', 'Mentor#Demo2026!', ROLE_MENTOR, 'Test', 'Mentor'),
    ('sales1', 'winningblueprints@gmail.com', 'Sales#Demo2026!', ROLE_SALES, 'Test', 'Sales'),
    ('office1', 'winningblueprints@gmail.com', 'Office#Demo2026!', ROLE_OFFICE, 'Office', 'Manager'),
    ('dev1', 'winningblueprints@gmail.com', 'WebDev#Demo2026!', ROLE_WEB_DEV, 'Web', 'Developer'),
    ('freelance1', 'winningblueprints@gmail.com', 'Freelance#Demo2026!', ROLE_FREELANCER, 'Free', 'Lancer'),
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
