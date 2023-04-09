from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class ProfessionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_html_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Professions, ProfessionsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о профессиях'
admin.site.site_header = 'Админ-панель сайта о профессиях'
