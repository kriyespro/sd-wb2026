from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from partners.models import PartnerProfile, ResellerOffer
from users.roles import ROLE_PARTNER


class Command(BaseCommand):
    help = 'Seed reseller offers and a sample DGC partner user (dgc1)'

    def handle(self, *args, **options):
        offers = [
            {
                'title': 'Startup D2C Launch',
                'description': 'Store setup + ads kickoff package for first-time D2C sellers.',
                'price': Decimal('15000.00'),
                'commission_percent': Decimal('20.00'),
                'sort_order': 1,
            },
            {
                'title': 'Growth Ads Retainer',
                'description': 'Monthly Meta + Google ads management for manufacturer brands.',
                'price': Decimal('35000.00'),
                'commission_percent': Decimal('15.00'),
                'sort_order': 2,
            },
            {
                'title': 'Full F2C Scale',
                'description': 'Store, ads, ops SOPs, and WhatsApp commerce for scaling factories.',
                'price': Decimal('75000.00'),
                'commission_percent': Decimal('12.00'),
                'sort_order': 3,
            },
        ]
        for data in offers:
            obj, created = ResellerOffer.objects.update_or_create(
                title=data['title'],
                defaults={**data, 'is_active': True},
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} offer: {obj.title}")

        user, created = User.objects.get_or_create(
            username='dgc1',
            defaults={'email': 'winningblueprints@gmail.com'},
        )
        if created:
            user.set_password('dgc1234')
            user.first_name = 'DGC'
            user.last_name = 'Partner'
            user.save()
        else:
            user.set_password('dgc1234')
            user.save(update_fields=['password'])

        user.profile.role = ROLE_PARTNER
        user.profile.phone = '9023561533'
        user.profile.save(update_fields=['role', 'phone'])

        PartnerProfile.objects.get_or_create(
            user=user,
            defaults={'code': 'DGC1001', 'is_active': True},
        )
        self.stdout.write(self.style.SUCCESS('DGC user ready: dgc1 / dgc1234 → /dashboard/dgc/'))
