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
                'title': 'Ecommerce Website',
                'description': (
                    'Full ecommerce store for manufacturers. Includes domain, server setup, '
                    'and full technical support. Ideal starter package for factories going online.'
                ),
                'price': Decimal('15000.00'),
                'market_price_min': Decimal('25000.00'),
                'market_price_max': Decimal('30000.00'),
                'billing_note': 'per year',
                'commission_percent': Decimal('0.00'),
                'sort_order': 1,
            },
            {
                'title': 'Ecommerce Plus',
                'description': (
                    'Ecommerce store with enhanced catalog, payments, and growth-ready setup. '
                    'Includes domain, server, and full technical support.'
                ),
                'price': Decimal('30000.00'),
                'market_price_min': Decimal('45000.00'),
                'market_price_max': Decimal('50000.00'),
                'billing_note': 'one-time',
                'commission_percent': Decimal('0.00'),
                'sort_order': 2,
            },
            {
                'title': 'Dropshipping Ecommerce + Auto Reseller Stores',
                'description': (
                    'Dropshipping ecommerce platform with auto reseller store create option. '
                    'Includes domain, server, and full technical support so partners can launch '
                    'multi-store reseller networks.'
                ),
                'price': Decimal('90000.00'),
                'market_price_min': Decimal('120000.00'),
                'market_price_max': Decimal('130000.00'),
                'billing_note': 'one-time',
                'commission_percent': Decimal('0.00'),
                'sort_order': 3,
            },
            {
                'title': 'Startup D2C Launch',
                'description': 'Store setup + ads kickoff package for first-time D2C sellers.',
                'price': Decimal('15000.00'),
                'market_price_min': Decimal('20000.00'),
                'market_price_max': Decimal('25000.00'),
                'billing_note': 'one-time',
                'commission_percent': Decimal('20.00'),
                'sort_order': 10,
            },
            {
                'title': 'Growth Ads Retainer',
                'description': 'Monthly Meta + Google ads management for manufacturer brands.',
                'price': Decimal('35000.00'),
                'market_price_min': Decimal('45000.00'),
                'market_price_max': Decimal('55000.00'),
                'billing_note': 'per month',
                'commission_percent': Decimal('15.00'),
                'sort_order': 11,
            },
            {
                'title': 'Full F2C Scale',
                'description': 'Store, ads, ops SOPs, and WhatsApp commerce for scaling factories.',
                'price': Decimal('75000.00'),
                'market_price_min': Decimal('95000.00'),
                'market_price_max': Decimal('120000.00'),
                'billing_note': 'one-time',
                'commission_percent': Decimal('12.00'),
                'sort_order': 12,
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
