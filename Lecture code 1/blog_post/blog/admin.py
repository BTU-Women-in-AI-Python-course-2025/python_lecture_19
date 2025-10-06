from django.contrib import admin
from blog.models import BlogPost, BlogPostImage, Author, BannerImage


admin.site.register(BlogPostImage)
admin.site.register(Author)
admin.site.register(BannerImage)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_date', 'update_date', 'active', 'deleted')
    list_editable = ('deleted',)
    list_filter = ('active', 'deleted', 'create_date', 'update_date', 'category')
    search_fields = ('title', 'text')
    filter_horizontal = ('authors',)
    readonly_fields = ('create_date', 'update_date')
    ordering = ('title',)

    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'authors', 'category', 'website', 'document')
        }),
        ('Status', {
            'fields': ('active', 'deleted')
        }),
        ('Timestamps', {
            'fields': ('create_date', 'update_date'),
        }),
    )
