from django.contrib import admin
from .models import Post


@admin.action(description="Make selected posts published")
def make_published(modeladmin, request, queryset):
    queryset.update(status=Post.Status.PUBLISHED)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'publish')
    search_fields = ['title', 'category__name', 'author__name', 'short_content', 'long_content']
    list_filter = ['category', 'created_at', 'updated_at', 'author', 'status']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    ordering = ['status', 'publish']
    date_hierarchy = 'publish'
    actions = [make_published]


admin.site.register(Post, PostAdmin)
