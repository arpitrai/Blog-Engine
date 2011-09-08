from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from mysite.blog.models import UserProfile, Post

class LatestEntriesFeed(Feed):
	title = 'Blog Feed'
	link = '/blog/'
	description = 'Updates on blog'

	def get_object(self, request, blog_id):
		return get_object_or_404(UserProfile, blog_slug=blog_id)

	def items(self, obj):
		return Post.objects.filter(blog_id=obj).order_by('-create_date')[:5]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.details
	

		
