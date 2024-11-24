# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class UserManager(BaseUserManager):
#     """
#     Custom manager for User model.
#     """
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')http://127.0.0.1:8000/auth/
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)  # Hash the password
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     """
#     Custom user model.
#     """
#     id = models.BigAutoField(primary_key=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     role = models.CharField(max_length=20, blank=True, null=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def __str__(self) -> str:
#         # Ensure we return a string that is meaningful and valid
#         return f"{self.first_name} {self.last_name} <{self.email}>"


# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     id = models.BigAutoField(primary_key=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     role = models.CharField(max_length=20, blank=True, null=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_groups',  # Unique related name
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_permissions',  # Unique related name
#         blank=True
#     )

#     def __str__(self) -> str:
#         return f"{self.first_name} {self.last_name} <{self.email}>"
    
   

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    
    # Define the roles
    KICD_OFFICIAL = 'kicd_official'
    FACILITATOR = 'facilitator'
    TEACHER = 'teacher'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (KICD_OFFICIAL, 'Kicd Official'),
        (FACILITATOR, 'Facilitator'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=TEACHER)

    email = models.EmailField(unique=True)
    # user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)

    REGISTERED_VIA_CHOICES = [
        ('kicd Official', 'Kicd API'),
        ('Facilitator', 'Facilitator API'),
        ('teacher', 'Teacher API'),
        ('admin', 'Admin Dashboard'),
    ]

    # Other metadata
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']



    def clean(self):
        if self.role == self.ADMIN and not self.is_superuser:
            raise ValidationError(_('Admin role can only be assigned to superusers.'))
        if self.is_superuser and self.role != self.ADMIN:
            raise ValidationError(_('Superusers must have the admin role.'))

    # Properties for role checks
    @property
    def is_kicd_official(self):
        return self.role == self.KICD_OFFICIAL

    @property
    def is_facilitator(self):
        return self.role == self.FACILITATOR

    @property
    def is_teacher(self):
        return self.role == self.TEACHER

    @property
    def is_admin(self):
        return self.role == self.ADMIN


# Login model to track user logins
class Login(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
