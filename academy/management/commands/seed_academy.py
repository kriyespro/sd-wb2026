from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from academy.models import (
    Assignment,
    Attendance,
    Certificate,
    Course,
    CourseModule,
    Enrollment,
    Lesson,
    MentorAllocation,
    PlacementApplication,
    PortfolioItem,
    StudentProject,
    StudentTask,
)
from users.roles import ROLE_MENTOR

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed academy courses and student demo data'

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            slug='digital-marketing-mastery',
            defaults={
                'title': 'Digital Marketing Mastery',
                'description': (
                    'Complete program covering SEO, Google Ads, Meta Ads, content marketing, '
                    'and real client project experience.'
                ),
                'duration_weeks': 16,
            },
        )

        course2, _ = Course.objects.get_or_create(
            slug='seo-specialist-track',
            defaults={
                'title': 'SEO Specialist Track',
                'description': 'Deep dive into technical SEO, content strategy, and link building with live projects.',
                'duration_weeks': 12,
            },
        )

        if not course.modules.exists():
            mod1 = CourseModule.objects.create(course=course, title='Foundations', order=1)
            Lesson.objects.bulk_create([
                Lesson(module=mod1, title='Introduction to Digital Marketing', content='Overview of channels and strategy.', order=1, duration_minutes=45),
                Lesson(module=mod1, title='Understanding Your Audience', content='Buyer personas and research.', order=2, duration_minutes=40),
            ])
            mod2 = CourseModule.objects.create(course=course, title='Paid Advertising', order=2)
            Lesson.objects.bulk_create([
                Lesson(module=mod2, title='Google Ads Fundamentals', content='Search and display campaigns.', order=1, duration_minutes=60),
                Lesson(module=mod2, title='Meta Ads Mastery', content='Facebook and Instagram ads.', order=2, duration_minutes=55),
            ])

        mentor, _ = User.objects.get_or_create(
            username='mentor1',
            defaults={'email': 'winningblueprints@gmail.com', 'first_name': 'Raj', 'last_name': 'Mentor'},
        )
        mentor.set_password('mentor1234')
        mentor.save()
        mentor.profile.role = ROLE_MENTOR
        mentor.profile.save()

        for username in ('student1', 'intern1'):
            try:
                student = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Skip {username} — run seed_users first'))
                continue

            Enrollment.objects.get_or_create(
                user=student, course=course,
                defaults={'progress_percent': 35 if username == 'student1' else 15},
            )
            Enrollment.objects.get_or_create(user=student, course=course2, defaults={'progress_percent': 10})

            MentorAllocation.objects.get_or_create(
                student=student, defaults={
                    'mentor': mentor,
                    'notes': 'Weekly review sessions every Friday. Focus on hands-on project work.',
                },
            )

            Assignment.objects.get_or_create(
                course=course, title='SEO Audit Report',
                defaults={
                    'description': 'Perform a complete SEO audit for a sample website and submit findings.',
                    'due_date': date.today() + timedelta(days=7),
                },
            )
            Assignment.objects.get_or_create(
                course=course, title='Google Ads Campaign Plan',
                defaults={
                    'description': 'Create a campaign structure with keywords, ad copy, and budget allocation.',
                    'due_date': date.today() + timedelta(days=14),
                },
            )

            StudentTask.objects.get_or_create(
                user=student, title='Complete keyword research exercise',
                defaults={
                    'description': 'Research 50 keywords for a local business.',
                    'status': StudentTask.STATUS_IN_PROGRESS,
                    'due_date': date.today() + timedelta(days=3),
                    'assigned_by': mentor,
                },
            )
            StudentTask.objects.get_or_create(
                user=student, title='Set up Google Analytics',
                defaults={
                    'description': 'Install GA4 on practice website.',
                    'status': StudentTask.STATUS_TODO,
                    'due_date': date.today() + timedelta(days=5),
                    'assigned_by': mentor,
                },
            )

            StudentProject.objects.get_or_create(
                user=student, title='Local Restaurant SEO',
                defaults={
                    'description': 'Mock project: improve local SEO for a restaurant client.',
                    'project_type': StudentProject.TYPE_MOCK,
                },
            )
            if username == 'student1':
                StudentProject.objects.get_or_create(
                    user=student, title='E-commerce Meta Ads',
                    defaults={
                        'description': 'Real client project: manage Meta ads for D2C brand.',
                        'project_type': StudentProject.TYPE_REAL,
                    },
                )

            for i in range(5):
                Attendance.objects.get_or_create(
                    user=student,
                    session_name='Morning Training',
                    date=date.today() - timedelta(days=i * 2),
                    defaults={'status': Attendance.STATUS_PRESENT if i < 4 else Attendance.STATUS_LATE},
                )

            PortfolioItem.objects.get_or_create(
                user=student, title='SEO Case Study — Local Business',
                defaults={
                    'description': 'Increased organic traffic 3x in 4 months.',
                    'project_url': 'https://example.com',
                },
            )

            if username == 'student1':
                Certificate.objects.get_or_create(
                    user=student, title='Digital Marketing Foundations',
                    defaults={'course': course, 'issued_at': date.today() - timedelta(days=30)},
                )
                PlacementApplication.objects.get_or_create(
                    user=student, company='Growth Agency Pvt Ltd', role='SEO Executive',
                    defaults={'status': PlacementApplication.STATUS_INTERVIEW},
                )

        self.stdout.write(self.style.SUCCESS('Academy data seeded. Login as student1 / student1234'))
