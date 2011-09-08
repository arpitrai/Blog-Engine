from django.contrib import admin
from mysite.blog.models import UserProfile, Post, Comment, PicUploads

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'create_date')
	search_fields = ('title',)
	list_filter = ('create_date',)
	date_hierarchy = 'create_date'
	ordering = ('-create_date',)
	fields = ('title', 'create_date', 'details','blog_id', 'tags','url',)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('blog_post', 'name', 'email', 'website', 'comment', 'date_time_submission')
	search_fields = ('comment',)
	fields = ('blog_post', 'name', 'email', 'website', 'comment',)

admin.site.register(UserProfile)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PicUploads)
