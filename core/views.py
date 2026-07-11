from django.shortcuts import redirect


def page_not_found(request, exception):
    """Redirect unknown URLs to the public home page."""
    return redirect('website:home')
