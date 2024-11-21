from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def assign_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            """Add the superuser to the admin group"""
            admin_group, created = Group.objects.get_or_create(name="Admin")
            instance.groups.add(admin_group)
            """ Assign admin permissions"""
            admin_permissions = Permission.objects.filter(
                codename__in=[
                    "view_portal",
                    "manage_users",
                    "view_statistics",
                    "edit_system_settings",
                    "manage_assessments",
                    "manage_resources",
                    "manage_trainers",
                    "manage_teachers",
                ]
            )
            instance.user_permissions.set(admin_permissions)
        elif instance.role == "teacher":
            """Assign teacher group and permissions"""
            teacher_group, created = Group.objects.get_or_create(name="Teacher")
            instance.groups.add(teacher_group)
            teacher_permissions = Permission.objects.filter(
                codename__in=[
                    "view_assessments",
                    "do_assessments",
                    "view_resources",
                ]
            )
            instance.user_permissions.set(teacher_permissions)
        elif instance.role == "trainer":
            """Assign trainer group and permissions"""
            trainer_group, created = Group.objects.get_or_create(name="Trainer")
            instance.groups.add(trainer_group)
            trainer_permissions = Permission.objects.filter(
                codename__in=[
                    "view_assessments",
                    "create_assessments",
                    "edit_assessments",
                    "view_resources",
                    "view_statistics",
                ]
            )
            instance.user_permissions.set(trainer_permissions)
        elif instance.role == "kicd_official":
            """Assign KICD official group and permissions"""
            kicd_group, created = Group.objects.get_or_create(name="KICD Official")
            instance.groups.add(kicd_group)
            kicd_permissions = Permission.objects.filter(
                codename__in=[
                    "view_assessments",
                    "allocate_teachers_to_trainers",
                    "view_progress",
                ]
            )
            instance.user_permissions.set(kicd_permissions)
        else:
            """Default user with read-only access"""
            default_group, created = Group.objects.get_or_create(name="Default User")
            instance.groups.add(default_group)
            default_permissions = Permission.objects.filter(codename="view_portal")
            instance.user_permissions.set(default_permissions)
        
        instance.save()