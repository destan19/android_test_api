#coding=utf-8
from django.db import models
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):

  def create_user(self, name, email, password=None):

    if not email:
      raise ValueError('Users must have an email address')

    user = self.model(
      name=name,
      email=UserManager.normalize_email(email),
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, name, email, password=None):

    user = self.create_user(name, email, password)
    user.is_admin = True
    user.save(using=self._db)
    return user
	
	
class User(AbstractBaseUser):

  name = models.CharField(max_length=100, unique=True)
  email = models.EmailField(max_length=100)
  phone_num=models.CharField(max_length=15)
  address=models.CharField(max_length=16)	
  self_image_url =models.CharField(max_length=128)
  avatar = models.URLField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_delete = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  access_token = models.CharField(max_length=100, blank=True)
  refresh_token = models.CharField(max_length=100, blank=True)
  expires_in = models.BigIntegerField(default=0)

  
  objects = UserManager()

  USERNAME_FIELD = 'name'
  REQUIRED_FIELDS = ('email',)
  def __str__(self):
	return self.name
  class Meta:
    ordering = ('-created_at',)

  def __unicode__(self):
    return self.name

  def get_full_name(self):
    return self.email

  def get_short_name(self):
    return self.name

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True

  @property
  def is_staff(self):
    return self.is_admin
	
class Relation(models.Model):
	me=models.ForeignKey(User)
	friend=models.ForeignKey(User,related_name='relation_friend')

	

class TalkMsg(models.Model):
	user=models.ForeignKey(User)
	img_url=models.CharField(max_length=128)
	content=models.CharField(max_length=128)
	address=models.CharField(max_length=128,null=True)
	device=models.CharField(max_length=128,null=True)
	src=models.CharField(max_length=128,null=True)
	date = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.content


class Comment(models.Model):
	talkmsg = models.ForeignKey(TalkMsg)
	friend=models.ForeignKey(User)
	comment_content=models.CharField(max_length=128)
	date = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.friend.name
		
class Praise(models.Model):
	talkmsg = models.ForeignKey(TalkMsg)
	friend=models.ForeignKey(User)
	date = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.friend.name
		
class Blog(models.Model):
	name=models.CharField(max_length=100)
	tagline=models.TextField()
	def __str__(self):
		return self.name
class Author(models.Model):
	name=models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Entry(models.Model):
	blog=models.ForeignKey(Blog)
	headline=models.CharField(max_length=255)
	body_text=models.TextField()
	authors=models.ManyToManyField(Author)
	n_comments=models.IntegerField()
	n_pingbacks=models.IntegerField()
	def __str__(self):
		return self.headline

