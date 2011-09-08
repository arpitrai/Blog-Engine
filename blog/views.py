from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render_to_response

from mysite.blog.models import UserProfile, Post, Comment, UserProfileForm, PostForm, CommentForm, PicUploads, PicUploadsForm

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm

from django.contrib.auth.decorators import login_required

from django.db.models import Count
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from mysite import settings
from django.template import RequestContext

def home(request):
	return render_to_response("home.html", {'request': request})

def register_account(request):
	user_registration_form = UserCreationForm()
	user_profile_form = UserProfileForm()
	if request.method=='POST':
		user_registration_form = UserCreationForm(data=request.POST)
		user_profile_form = UserProfileForm(request.POST)
		if user_registration_form.is_valid() and user_profile_form.is_valid():
				new_user = user_registration_form.save()
				user_profile = UserProfile(user=new_user)
				user_profile_form = UserProfileForm(request.POST, instance=user_profile) 
				user_profile_form.save()
				return redirect("/my_account/", {'next': '/my_account'})
	return render_to_response("registration/register.html", {'form': user_registration_form, 'user_profile_form': user_profile_form, 'request': request}, context_instance=RequestContext(request))

@login_required
def my_account(request):
	user_profile_object = UserProfile.objects.get(user=request.user)
	posts = Post.objects.filter(blog_id=user_profile_object).order_by('-create_date')
	blog_slug = UserProfile.objects.get(user=request.user).blog_slug
	return render_to_response("my_account.html",{'posts': posts, 'blog_slug': blog_slug, 'request': request}, context_instance=RequestContext(request))

@login_required
def delete_post(request, blog_id, url):
	post_object = Post.objects.get(blog_id=UserProfile.objects.get(blog_slug=blog_id), url=url)
	post_object.delete()
	return HttpResponseRedirect('/my_account/')

@login_required
def edit_profile(request):
	if request.method == 'POST':
		request.user.first_name = request.POST['first_name']
		request.user.last_name = request.POST['last_name']
		request.user.save()
		return HttpResponseRedirect("/my_account/")
	return render_to_response("edit_profile.html",{'request': request}, context_instance=RequestContext(request))

@login_required
def create(request):
	post_form = PostForm()
	pic_upload_form = PicUploadsForm()
	if request.method == 'POST':
		post_form = PostForm(request.POST)
		if post_form.is_valid():
			user_object = User.objects.get(username=request.user.username)
			user_profile_object = UserProfile.objects.get(user=user_object)
			title = request.POST['title'].lower()
			url = ''
			for char in title:
				if ('a'<=char<='z') or ('A'<=char<='Z') or (48<=ord(char)<=57) or (char==' '):
					if char==' ':
						url+='-'
					else:
						url+=char
				else:
					continue
			post = Post(blog_id=user_profile_object, url=url)
			post_form = PostForm(request.POST, instance=post)
			post_form.save()

			post_object = Post.objects.get(blog_id=user_profile_object, url=url) 
	
			pic_upload_instance = PicUploads(blog_post=post_object)
			pic_upload_form = PicUploadsForm(request.POST, request.FILES, instance=pic_upload_instance)
			if pic_upload_form.is_valid():
				pic_upload_form.save()
	
			redirect_url = '/' + request.user.username + '/' + url
			return HttpResponseRedirect(redirect_url)
	return render_to_response("create.html", {'post_form': post_form, 'pic_upload_form': pic_upload_form, 'request': request, 'post_function': 'create'}, context_instance=RequestContext(request))


@login_required
def edit_post(request, blog_id, url):
	user_profile_object = UserProfile.objects.get(blog_slug=blog_id)
	post = Post.objects.get(blog_id=user_profile_object, url=url)
	post_form = PostForm(instance=post)
	if request.method == 'POST':
		post = Post.objects.get(blog_id=user_profile_object, url=url)
		post_form = PostForm(request.POST, instance=post)
		if post_form.is_valid():
			post_form.save()
			return HttpResponseRedirect('/my_account/')
	return render_to_response("create.html", {'post_form': post_form, 'request': request, 'post_function': 'edit'}, context_instance=RequestContext(request))


def posts(request, blog_id):
	user_profile_object = UserProfile.objects.get(blog_slug=blog_id)
	post_objects = Post.objects.filter(blog_id=user_profile_object).annotate(comment_count=Count('comment')).order_by('-create_date')

	user_object = User.objects.get(pk=user_profile_object.user_id)

	paginator = Paginator(post_objects, 5)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		posts = paginator.page(page)
	except (EmptyPage, InvalidPage):
		posts = paginator.page(paginator.num_pages)
	return render_to_response("posts.html",{'posts': posts, 'user_object': user_object,'blog_slug': blog_id, 'request': request}, context_instance=RequestContext(request))


def post(request, blog_id, url):
	comment_form = CommentForm()
	user_profile_object = UserProfile.objects.get(blog_slug=blog_id)
	post_object = Post.objects.get(blog_id=user_profile_object, url=url) 

	user_object = User.objects.get(pk=user_profile_object.user_id)

	comments = Comment.objects.filter(blog_post=post_object)
	if request.method == 'POST':
		comment_object_instance = Comment(blog_post=post_object)
		comment_form = CommentForm(request.POST, instance=comment_object_instance)
		if comment_form.is_valid():
			comment_form.save()
			redirect_url = '/' + blog_id + '/' + url + '/'
			return HttpResponseRedirect(redirect_url)
	return render_to_response("comments.html",{'post': post_object, 'comments': comments, 'comment_form': comment_form, 'detail': 'Yes',  'user_object': user_object,'blog_slug': blog_id, 'request': request}, context_instance=RequestContext(request))

@login_required
def change_password(request):
	form = PasswordChangeForm(request.user)
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		print form
		if form.is_valid():
			form.save()
			return render_to_response("password_change_done.html", {'request': request})
	return render_to_response("password_change_form.html", {'form': form, 'request': request}, context_instance=RequestContext(request))

@login_required
def my_posts(request):
	user_profile_object = UserProfile.objects.get(user=request.user)
	post_objects = Post.objects.filter(blog_id=user_profile_object).order_by('-create_date')
	paginator = Paginator(post_objects,3)
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		posts = paginator.page(page)
	except (EmptyPage, InvalidPage):
		posts = paginator.page(paginator.num_pages)
	return render_to_response("my_posts.html", {'posts': posts, 'request': request}, context_instance=RequestContext(request))

@login_required
def view_comments(request):
	comments = Comment.objects.filter(blog_post__blog_id__user=request.user)
	return render_to_response("view_comments.html", {'comments': comments, 'request': request}, context_instance=RequestContext(request))

"""def password_recovery(request):
	form = PasswordResetForm()
	print form
	if request.method == 'POST':
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			form.save()
			return render_to_response("registration/password_reset_done.html")
	return render_to_response("registration/password_reset_form.html", {'form': form})"""

@login_required
def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/") 
