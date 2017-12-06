from django.contrib import admin
from .models import Post, Category
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title', 'body')    
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'publish', 'created', 'author')
    raw_id_fields = ['author']
    date_hierarchy = "publish"
    ordering = ('status', 'publish')
    
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
