from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	blog_slug = models.CharField(max_length=40, verbose_name='blog Slug')

	def __unicode__(self):
		return self.blog_slug

class UserProfileForm(forms.ModelForm):
	blog_slug = forms.RegexField(label=_("Blog Slug"), max_length=40, regex=r'^[\w.@+-]+$', help_text = _("Required 40 characters or fewer. Letters, digits and @/./+/-/_ only. "), error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters."), 'required': _("Required field. Enter a value.")})
	class Meta:
		model = UserProfile
		exclude = ('user',)
	def clean_blog_slug(self):
		blog_slug=self.cleaned_data["blog_slug"]
		if len(blog_slug) > 10:
			raise forms.ValidationError(_("Although I said 40 characters I meant 10."))
		else:
			return blog_slug

class Post(models.Model):
	blog_id = models.ForeignKey(UserProfile)
	url = models.CharField(max_length=40)
	title = models.CharField(max_length=60)
	create_date = models.DateField(verbose_name='create Date')
	details = models.TextField()
	tags = models.CharField(max_length=20)

	def __unicode__(self):
		return self.title

	#@models.permalink
	def get_absolute_url(self):
		return '/%s/%s/' % (self.blog_id, self.url)
		#return ('views.edit', (), {'blog_id': self.blog_id, 'url': self.url })

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ('blog_id','url',)

class Comment(models.Model):
	blog_post = models.ForeignKey(Post)
	name = models.CharField(max_length=40)
	email = models.EmailField()
	website = models.URLField(verify_exists=False)
	comment = models.TextField()
	date_time_submission = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ('blog_post',)

class PicUploads(models.Model):
	blog_post = models.ForeignKey(Post)
	pic = models.ImageField(upload_to='pics')

class PicUploadsForm(forms.ModelForm):
	class Meta:
		model=PicUploads
		exclude = ('blog_post',)

