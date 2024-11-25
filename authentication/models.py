# from django.contrib.auth.models import AbstractUser
# from django.db import models
# import logging

# logger = logging.getLogger(__name__)

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True, help_text='User email address, must be unique.')
#     first_name = models.CharField(max_length=30, blank=True, help_text='User’s first name.')
#     last_name = models.CharField(max_length=30, blank=True, help_text='User’s last name.')
#     kicd_number = models.CharField(max_length=50, blank=True, help_text=" User's kicd number")

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='auth_customuser_groups',  
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='auth_customuser_permissions',  
#         blank=True
#     )

#     def __str__(self):
#         full_name = f"{self.first_name} {self.last_name}".strip()
#         if not full_name:
#             full_name = self.email  

#         logger.debug('Generating string representation of user: %s', full_name)
#         return full_name

#     def save(self, *args, **kwargs):
#         logger.info('Saving user instance: %s', self.username)
#         super().save(*args, **kwargs)
#         logger.info('User instance saved successfully: %s', self.username)

#     class Meta:
#         verbose_name = 'Custom User'
#         verbose_name_plural = 'Custom Users'






        