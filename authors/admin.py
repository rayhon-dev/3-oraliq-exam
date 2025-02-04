from django.contrib import admin
from .models import Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'photo')
    search_fields = ['full_name']
    prepopulated_fields = {'slug': ('full_name',)}


admin.site.register(Author, AuthorAdmin)
