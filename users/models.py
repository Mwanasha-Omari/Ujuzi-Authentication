# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# # Custom User Manager
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
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_staff', True)
#         return self.create_user(email, password, **extra_fields)

# # Custom User Model
# class User(AbstractBaseUser, PermissionsMixin):
    
#     # Define the roles
#     KICD_OFFICIAL = 'kicd_official'
#     FACILITATOR = 'facilitator'
#     TEACHER = 'teacher'
#     ADMIN = 'admin'
    
#     ROLE_CHOICES = [
#         (KICD_OFFICIAL, 'Kicd Official'),
#         (FACILITATOR, 'Facilitator'),
#         (TEACHER, 'Teacher'),
#         (ADMIN, 'Admin'),
#     ]
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=TEACHER)

#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=100)

#     REGISTERED_VIA_CHOICES = [
#         ('kicd Official', 'Kicd API'),
#         ('Facilitator', 'Facilitator API'),
#         ('teacher', 'Teacher API'),
#         ('admin', 'Admin Dashboard'),
#     ]

#     # Other metadata
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']



#     def clean(self):
#         if self.role == self.ADMIN and not self.is_superuser:
#             raise ValidationError(_('Admin role can only be assigned to superusers.'))
#         if self.is_superuser and self.role != self.ADMIN:
#             raise ValidationError(_('Superusers must have the admin role.'))

#     # Properties for role checks
#     @property
#     def is_kicd_official(self):
#         return self.role == self.KICD_OFFICIAL

#     @property
#     def is_facilitator(self):
#         return self.role == self.FACILITATOR

#     @property
#     def is_teacher(self):
#         return self.role == self.TEACHER

#     @property
#     def is_admin(self):
#         return self.role == self.ADMIN


# # Login model to track user logins
# class Login(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
#     timestamp = models.DateTimeField(auto_now_add=True)






from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
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
    # Define roles
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=now)

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

    def __str__(self):
        return self.email

class Login(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} logged in at {self.timestamp}"

    class Meta:
        db_table = 'users_login'  # Explicitly set the table name




# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.utils.timezone import now
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# # Custom User Manager
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
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_staff', True)
#         return self.create_user(email, password, **extra_fields)

# # Custom User Model
# class User(AbstractBaseUser, PermissionsMixin):
#     # Define roles
#     KICD_OFFICIAL = 'kicd_official'
#     FACILITATOR = 'facilitator'
#     TEACHER = 'teacher'
#     ADMIN = 'admin'

#     ROLE_CHOICES = [
#         (KICD_OFFICIAL, 'Kicd Official'),
#         (FACILITATOR, 'Facilitator'),
#         (TEACHER, 'Teacher'),
#         (ADMIN, 'Admin'),
#     ]
    
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=TEACHER)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=100)
#     date_joined = models.DateTimeField(default=now)  # Explicitly added field

#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def clean(self):
#         if self.role == self.ADMIN and not self.is_superuser:
#             raise ValidationError(_('Admin role can only be assigned to superusers.'))
#         if self.is_superuser and self.role != self.ADMIN:
#             raise ValidationError(_('Superusers must have the admin role.'))

#     # Properties for role checks
#     @property
#     def is_kicd_official(self):
#         return self.role == self.KICD_OFFICIAL

#     @property
#     def is_facilitator(self):
#         return self.role == self.FACILITATOR

#     @property
#     def is_teacher(self):
#         return self.role == self.TEACHER

#     @property
#     def is_admin(self):
#         return self.role == self.ADMIN


# # Login model to track user logins
# # class Login(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
# #     timestamp = models.DateTimeField(auto_now_add=True)



# class Login(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} logged in at {self.timestamp}"






















# # from django.db import models
# # from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# # from django.core.exceptions import ValidationError
# # from django.utils.translation import gettext_lazy as _

# # # Custom User Manager
# # class UserManager(BaseUserManager):
# #     def create_user(self, email, password=None, **extra_fields):
# #         if not email:
# #             raise ValueError('The Email field must be set')
# #         email = self.normalize_email(email)
# #         user = self.model(email=email, **extra_fields)
# #         user.set_password(password)
# #         user.save(using=self._db)
# #         return user

# #     def create_superuser(self, email, password=None, **extra_fields):
# #         extra_fields.setdefault('is_superuser', True)
# #         extra_fields.setdefault('is_staff', True)
# #         return self.create_user(email, password, **extra_fields)

# # # Custom User Model
# # class User(AbstractBaseUser, PermissionsMixin):
    
# #     # Define the roles
# #     KICD_OFFICIAL = 'kicd_official'
# #     FACILITATOR = 'facilitator'
# #     TEACHER = 'teacher'
# #     ADMIN = 'admin'
    
# #     ROLE_CHOICES = [
# #         (KICD_OFFICIAL, 'Kicd Official'),
# #         (FACILITATOR, 'Facilitator'),
# #         (TEACHER, 'Teacher'),
# #         (ADMIN, 'Admin'),
# #     ]
# #     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=TEACHER)

# #     email = models.EmailField(unique=True)
# #     first_name = models.CharField(max_length=30)
# #     last_name = models.CharField(max_length=100)

# #     # User-specific fields based on role
# #     tsc_number = models.CharField(max_length=50, blank=True, null=True, help_text="Teacher's TSC Number")
# #     facilitator_number = models.CharField(max_length=50, blank=True, null=True, help_text="Facilitator's Number")
# #     kicd_number = models.CharField(max_length=50, blank=True, null=True, help_text="KICD Official's Number")

# #     # Other metadata
# #     is_staff = models.BooleanField(default=False)
# #     is_active = models.BooleanField(default=True)

# #     objects = UserManager()

# #     USERNAME_FIELD = 'email'
# #     REQUIRED_FIELDS = ['first_name', 'last_name']

# #     def clean(self):
# #         # Role-based validations
# #         if self.role == self.ADMIN and not self.is_superuser:
# #             raise ValidationError(_('Admin role can only be assigned to superusers.'))
# #         if self.is_superuser and self.role != self.ADMIN:
# #             raise ValidationError(_('Superusers must have the admin role.'))
        
# #         # Role-specific number validation
# #         if self.role == self.TEACHER and not self.tsc_number:
# #             raise ValidationError(_('TSC number must be provided for teachers.'))
# #         if self.role == self.FACILITATOR and not self.facilitator_number:
# #             raise ValidationError(_('Facilitator number must be provided for facilitators.'))
# #         if self.role == self.KICD_OFFICIAL and not self.kicd_number:
# #             raise ValidationError(_('KICD number must be provided for KICD officials.'))

# #     # Properties for role checks
# #     @property
# #     def is_kicd_official(self):
# #         return self.role == self.KICD_OFFICIAL

# #     @property
# #     def is_facilitator(self):
# #         return self.role == self.FACILITATOR

# #     @property
# #     def is_teacher(self):
# #         return self.role == self.TEACHER

# #     @property
# #     def is_admin(self):
# #         return self.role == self.ADMIN


# # # Login model to track user logins
# # class Login(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
# #     timestamp = models.DateTimeField(auto_now_add=True)
