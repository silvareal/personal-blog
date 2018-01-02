from django.contrib import admin
from .models import Post, Profile
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title', 'body')    
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'publish', 'created', 'author')
    raw_id_fields = ['author']
    date_hierarchy = "publish"
    ordering = ('status', 'publish')

class ProfileAmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo')
    
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAmin)

