from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Tag, TagAdmin)
