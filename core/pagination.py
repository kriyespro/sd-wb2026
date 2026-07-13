from django.core.paginator import Paginator


def paginate(request, queryset, per_page=20, page_param='page'):
    """Shared list-view pagination. get_page() clamps out-of-range/invalid
    page numbers instead of raising, so callers don't need try/except."""
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get(page_param) or 1)
