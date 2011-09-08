from django.conf.urls.defaults import *
from django.contrib.auth.views import login, password_reset
from mysite.blog import views

# To serve static media like CSS, JS, Images
from django.views.static import *
from django.conf import settings

# For RSS Feed
from mysite.blog.feed import LatestEntriesFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite_testing/', include('mysite_testing.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
	(r'^$', views.home),
    # For Django-Registration package
    (r'^accounts/', include('registration.backends.default.urls')),

	(r'^register_account/$', views.register_account),
	(r'^my_account/$', views.my_account),
	(r'^login/$', login), 
	(r'^logout/$', views.logout_user), 
	(r'^create/$', views.create),

	(r'^edit_post/(?P<blog_id>[A-Za-z-]+)/(?P<url>[A-Za-z-0-9]+)/$', views.edit_post),
	(r'^edit_profile/$', views.edit_profile),
	
	(r'^delete_post/(?P<blog_id>[A-Za-z-]+)/(?P<url>[A-Za-z-0-9]+)/$', views.delete_post),
	(r'^change_password/$', views.change_password),
	(r'^my_posts/$', views.my_posts),
	(r'^view_comments/$', views.view_comments),
	#(r'^password_recovery/$', views.password_recovery),
	(r'^password_recovery/$', password_reset),

	# For RSS Feed
	(r'^latest/feed/(?P<blog_id>[A-Za-z-]+)/$', LatestEntriesFeed()),

	(r'^(?P<blog_id>[A-Za-z-]+)/$', views.posts),
    (r'^(?P<blog_id>[A-Za-z-]+)/(?P<url>[A-Za-z-0-9]+)/$', views.post),


)

if settings.DEBUG == True:
    # Required to make static serving work 
	urlpatterns += patterns('',
			(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
