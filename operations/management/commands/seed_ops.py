from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from projects.models import Project
from operations.models import (
    Assessment,
    PerformanceReview,
    ProjectAssignment,
    Team,
    TeamMember,
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed operations teams, assignments, and performance data'

    def handle(self, *args, **options):
        teams_data = [
            ('SEO Team', 'seo-team', 'Organic growth specialists'),
            ('Paid Ads Team', 'paid-ads-team', 'Google and Meta ads'),
            ('Development Team', 'development-team', 'Web and app development'),
        ]
        teams = {}
        for name, slug, desc in teams_data:
            team, _ = Team.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
            teams[slug] = team

        pm = User.objects.filter(username='pm1').first()
        mentor = User.objects.filter(username='mentor1').first()
        student = User.objects.filter(username='student1').first()
        intern = User.objects.filter(username='intern1').first()

        if pm:
            TeamMember.objects.get_or_create(team=teams['seo-team'], user=pm, defaults={'seniority': TeamMember.SENIORITY_SENIOR})
        if mentor:
            TeamMember.objects.get_or_create(team=teams['seo-team'], user=mentor, defaults={'seniority': TeamMember.SENIORITY_SENIOR})
        if student:
            TeamMember.objects.get_or_create(team=teams['seo-team'], user=student, defaults={'seniority': TeamMember.SENIORITY_STUDENT})
        if intern:
            TeamMember.objects.get_or_create(team=teams['paid-ads-team'], user=intern, defaults={'seniority': TeamMember.SENIORITY_INTERN})

        project = Project.objects.first()
        if project:
            if pm:
                ProjectAssignment.objects.get_or_create(
                    project=project, user=pm,
                    defaults={'role': ProjectAssignment.ROLE_PM, 'can_contact_client': True},
                )
            if mentor:
                ProjectAssignment.objects.get_or_create(
                    project=project, user=mentor,
                    defaults={'role': ProjectAssignment.ROLE_SENIOR, 'can_contact_client': True},
                )
            if student:
                ProjectAssignment.objects.get_or_create(
                    project=project, user=student,
                    defaults={'role': ProjectAssignment.ROLE_STUDENT, 'can_contact_client': False},
                )

        for user, period, rating in [(student, 'Q2 2026', 4), (intern, 'Q2 2026', 3)]:
            if user:
                PerformanceReview.objects.get_or_create(
                    user=user, period=period,
                    defaults={'rating': rating, 'reviewer': mentor, 'notes': 'Solid progress on assigned tasks.'},
                )

        for user, title, score, status in [
            (student, 'SEO Fundamentals Test', 82, Assessment.STATUS_PASSED),
            (intern, 'Ads Basics Test', None, Assessment.STATUS_SCHEDULED),
        ]:
            if user:
                Assessment.objects.get_or_create(
                    candidate=user, title=title,
                    defaults={'score': score, 'status': status},
                )

        self.stdout.write(self.style.SUCCESS('Ops data seeded. Login as admin / admin1234 or pm1 / pm1234'))
