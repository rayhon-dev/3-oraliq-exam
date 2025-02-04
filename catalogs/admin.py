from django.contrib import admin
from .models import Catalog


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name', 'desc']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Catalog, CatalogAdmin)
