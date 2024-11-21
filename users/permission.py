from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsAuthenticatedAndHasPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm("view_portal")

class HasTeacherPermissions(BasePermission):
    """
    Custom permission for teachers.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "teacher":
            teacher_permissions = [
                "view_assessments",
                "do_assessments",
                "view_resources",
            ]
            return all(request.user.has_perm(perm) for perm in teacher_permissions)
        return False

class HasTrainerPermissions(BasePermission):
    """
    Custom permission for trainers.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "trainer":
            trainer_permissions = [
                "view_assessments",
                "create_assessments",
                "edit_assessments",
                "view_resources",
                "view_statistics",
            ]
            return all(request.user.has_perm(perm) for perm in trainer_permissions)
        return False

class HasAdminPermissions(BasePermission):
    """
    Custom permission for admin users with full access.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "admin":
            admin_permissions = [
                "view_portal",
                "manage_users",
                "view_statistics",
                "edit_system_settings",
                "manage_assessments",
                "manage_resources",
                "manage_trainers",
                "manage_teachers",
            ]
            return all(request.user.has_perm(perm) for perm in admin_permissions)
        return False

class HasKICDOfficialPermissions(BasePermission):
    """
    Custom permission for KICD officials.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "kicd_official":
            kicd_permissions = [
                "view_assessments",
                "allocate_teachers",
                "view_progress",
            ]
            return all(request.user.has_perm(perm) for perm in kicd_permissions)
        return False

class ReadOnlyAccess(BasePermission):
    """
    Custom permission to allow read-only access for authenticated users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in SAFE_METHODS