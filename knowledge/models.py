from django.db import models


class KnowledgeArticle(models.Model):
    AUDIENCE_ALL = 'all'
    AUDIENCE_OPS = 'ops'
    AUDIENCE_OFFICE = 'office'
    AUDIENCE_DGC = 'dgc'
    AUDIENCE_CLIENT = 'client'
    AUDIENCE_DELIVERY = 'delivery'
    AUDIENCE_CHOICES = [
        (AUDIENCE_ALL, 'Everyone'),
        (AUDIENCE_OPS, 'Ops / Admin'),
        (AUDIENCE_OFFICE, 'Office / Sales'),
        (AUDIENCE_DGC, 'DGC partners'),
        (AUDIENCE_CLIENT, 'Clients'),
        (AUDIENCE_DELIVERY, 'Developers / Freelancers'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(max_length=80, blank=True)
    summary = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    audience = models.CharField(
        max_length=20, choices=AUDIENCE_CHOICES, default=AUDIENCE_ALL,
    )
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title
