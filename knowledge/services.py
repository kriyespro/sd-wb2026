from users.roles import (
    CLIENT_ROLES,
    DELIVERY_ROLES,
    OFFICE_DESK_ROLES,
    OPS_ROLES,
    PARTNER_ROLES,
    ROLE_SUPER_ADMIN,
)

from .models import KnowledgeArticle


def audiences_for_user(user):
    if not user.is_authenticated:
        return {KnowledgeArticle.AUDIENCE_ALL}
    role = getattr(getattr(user, 'profile', None), 'role', None)
    audiences = {KnowledgeArticle.AUDIENCE_ALL}
    if role == ROLE_SUPER_ADMIN or user.is_superuser:
        return {value for value, _ in KnowledgeArticle.AUDIENCE_CHOICES}
    if role in OPS_ROLES:
        audiences.add(KnowledgeArticle.AUDIENCE_OPS)
    if role in OFFICE_DESK_ROLES:
        audiences.add(KnowledgeArticle.AUDIENCE_OFFICE)
    if role in PARTNER_ROLES:
        audiences.add(KnowledgeArticle.AUDIENCE_DGC)
    if role in CLIENT_ROLES:
        audiences.add(KnowledgeArticle.AUDIENCE_CLIENT)
    if role in DELIVERY_ROLES:
        audiences.add(KnowledgeArticle.AUDIENCE_DELIVERY)
    return audiences


def articles_for_user(user, category=None):
    qs = KnowledgeArticle.objects.filter(
        is_published=True,
        audience__in=audiences_for_user(user),
    )
    if category:
        qs = qs.filter(category=category)
    return qs
