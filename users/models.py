from django.contrib.auth.models import User
from django.db import models

from .roles import ROLE_CHOICES, ROLE_CLIENT_OWNER


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_CLIENT_OWNER)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} ({self.get_role_display()})'

    @property
    def portal(self):
        from .services import get_portal_for_role
        return get_portal_for_role(self.role)
