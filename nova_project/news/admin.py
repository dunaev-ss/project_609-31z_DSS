from django.contrib import admin

from news.models import Article


class ArticleAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Article, ArticleAdmin)