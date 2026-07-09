from django.conf import settings

from website.data import CONTACT_INFO, SITE_IMAGES


def site_context(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_tagline': settings.SITE_TAGLINE,
        'contact_info': CONTACT_INFO,
        'site_images': SITE_IMAGES,
        'nav_items': [
            {'label': 'Home', 'url_name': 'website:home'},
            {'label': 'Services', 'url_name': 'website:services'},
            {'label': 'Our Work', 'url_name': 'website:our_work'},
            {'label': 'Case Studies', 'url_name': 'website:case_studies'},
            {'label': 'Industries', 'url_name': 'website:industries'},
            {'label': 'Pricing', 'url_name': 'website:pricing'},
            {'label': 'About', 'url_name': 'website:about'},
            {'label': 'Careers', 'url_name': 'website:careers'},
            {'label': 'Academy', 'url_name': 'academy:courses'},
            {'label': 'Contact', 'url_name': 'website:contact'},
        ],
    }
