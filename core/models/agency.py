import uuid
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password)
        user.is_admin = True
        user.email_verified = True
        user.save(using=self._db)
        return user


class TimeZone(models.Model):
    name = models.CharField(max_length=30, unique=True)
    value = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name


class Admin(AbstractBaseUser):

    '''Basic details of user.'''
    email = models.EmailField(null=True, blank=True, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    username = models.CharField(
        max_length=40, blank=True, null=True, default='')
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=15, blank=True)
    profile_image = models.CharField(null=True, blank=True, max_length=550)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Unique Id")
    time_zone=models.ForeignKey(TimeZone,on_delete=models.CASCADE,blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_forget=models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class ActivityTracking(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(blank=True,null=True)

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Address(models.Model):
    address=models.CharField(max_length=500,blank=True,null=True)
    state=models.ForeignKey(State,on_delete=models.CASCADE,blank=True,null=True)
    country=models.ForeignKey(Country,on_delete=models.CASCADE,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    zip_code=models.CharField(max_length=6,blank=True,null=True)

# Create your models here.


class AgencyUser(Admin):
    business_name = models.CharField(max_length=30, blank=True, null=True)
    business_email = models.EmailField(blank=True, null=True)
    business_phone_no = models.CharField(max_length=15, blank=True, null=True)
    whitelabeldomian = models.CharField(max_length=200, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    plan_duration = models.CharField(max_length=100, blank=True, null=True)
    account_sid = models.CharField(max_length=100, blank=True, null=True)
    auth_token = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='admin_user')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    support_email = models.EmailField(blank=True, null=True)
    host = models.ForeignKey("AgencyHostname", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name

class AgencyHostname(ActivityTracking):
    user = models.ForeignKey(AgencyUser, on_delete=models.SET_NULL, blank=True, null=True)
    host_id = models.CharField(max_length=250, blank=True, null=True)
    hostname = models.CharField(max_length=250, blank=True, null=True)
    response = models.JSONField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.hostname