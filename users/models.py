from django.db import models
from myadmin.models import Department
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from Assessment.settings import AUTH_USER_MODEL

class AccountManager(BaseUserManager):
  def create_user(self,email,username ,phone_number, password=None,role=None,department=None,created_by=None):
    if not email:
      raise ValueError('Users must have an email address')

    if not phone_number:
      raise ValueError("User must have an Mobile Number")

    if not username:
        raise ValueError("User must have a name")   

    email = self.normalize_email(email)

    user = self.model(
      username  = username,email=email,
      phone_number=phone_number,role=role,
      department=department,
      created_by=created_by
    )
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self,username ,phone_number, email, password=None):
    user = self.create_user(
      username = username ,email =email,phone_number=phone_number,
    )
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user


class Accounts(AbstractBaseUser, PermissionsMixin):

   
    username =   models.CharField(max_length=120,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    phone_number =   models.CharField(max_length=50, unique=True)
    created_by =  models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,null=True )
    department = models.ForeignKey(Department,on_delete=models.PROTECT,null =True, related_name='department')
    role = models.CharField(max_length=255 , null =True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']

    def __str__(self):
        return self.username
    