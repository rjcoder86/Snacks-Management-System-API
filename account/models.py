import re

from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from rest_framework.exceptions import ValidationError

class UserManager(BaseUserManager):
  def create_user(self, email, first_name,last_name, user_type,phoneno, password=None, password2=None):
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          first_name=first_name,
          last_name=last_name,
          phoneno=phoneno,
          user_type=user_type
      )
      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, first_name, phoneno, password=None):
      user = self.create_user(
          email,
          password=password,
          first_name=first_name,
          phoneno=phoneno,
          last_name='',
          user_type='admin'
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#validation function for phone no
def mobile_no(value):
  mobile = str(value)
  if len(mobile) != 10:
    raise ValidationError("Mobile Number Should 10 digit")

# def email_val(value):
#   e = str(value)
#   regex = r'\b[A-Za-z0-9._%+-]+@weagile+\.net\b'
#   if (re.fullmatch(regex, e)):
#     raise ValidationError("Please enter valid email ID")


class User(AbstractBaseUser):
  email = models.EmailField(verbose_name='Email',max_length=255,unique=True)
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200,default='')
  phoneno = models.PositiveBigIntegerField(default=000)
  is_active = models.BooleanField(default=True)
  user_type=models.CharField(max_length=30,default='')
  is_admin = models.BooleanField(default=False)
  is_verified = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'phoneno']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin




