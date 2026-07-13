from django.contrib import admin

from .models import KnowledgeArticle


@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'audience', 'is_published', 'sort_order')
    list_filter = ('audience', 'is_published', 'category')
    search_fields = ('title', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}
