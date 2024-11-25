from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from users.models import Login, User

class UserModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': User.TEACHER
        }
        
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.role, User.TEACHER)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_create_user_without_email(self):
        """Test creating a user without email raises error"""
        self.user_data['email'] = ''
        with self.assertRaises(ValueError):
            User.objects.create_user(**self.user_data)

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(**{**self.user_data, 'email': 'super@example.com'})
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, User.TEACHER)

    def test_user_roles(self):
        """Test user role properties"""
        # Test KICD Official
        user = User.objects.create_user(**{
            **self.user_data, 
            'email': 'kicd@example.com',
            'role': User.KICD_OFFICIAL
        })
        self.assertTrue(user.is_kicd_official)
        self.assertFalse(user.is_teacher)
        
        # Test Facilitator
        user = User.objects.create_user(**{
            **self.user_data,
            'email': 'facilitator@example.com',
            'role': User.FACILITATOR
        })
        self.assertTrue(user.is_facilitator)
        self.assertFalse(user.is_teacher)
        
        # Test Teacher
        user = User.objects.create_user(**{
            **self.user_data,
            'email': 'teacher@example.com',
            'role': User.TEACHER
        })
        self.assertTrue(user.is_teacher)
        self.assertFalse(user.is_facilitator)
        
        # Test Admin
        admin_data = {
            **self.user_data,
            'email': 'admin@example.com',
            'role': User.ADMIN
        }
        user = User.objects.create_superuser(**admin_data)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_superuser)

    def test_email_normalization(self):
        """Test email normalization"""
        email = 'test@EXAMPLE.com'
        user = User.objects.create_user(**{
            **self.user_data,
            'email': email
        })
        self.assertEqual(user.email, email.lower())

    def test_admin_role_validation(self):
        """Test admin role validation rules"""
        # Test non-superuser cannot be admin
        user = User.objects.create_user(**{
            **self.user_data,
            'email': 'test1@example.com'
        })
        user.role = User.ADMIN
        with self.assertRaises(ValidationError):
            user.clean()

        # Test superuser must be admin
        user = User.objects.create_superuser(**{
            **self.user_data,
            'email': 'test2@example.com'
        })
        user.role = User.TEACHER
        with self.assertRaises(ValidationError):
            user.clean()

    def test_str_representation(self):
        """Test string representation of user"""
        user = User.objects.create_user(**{
            **self.user_data,
            'email': 'str_test@example.com'
        })
        self.assertEqual(str(user), 'str_test@example.com')

class LoginModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_login_creation(self):
        """Test creating a login record"""
        login = Login.objects.create(user=self.user)
        self.assertEqual(login.user, self.user)
        self.assertIsInstance(login.timestamp, datetime)
        self.assertLess(timezone.now() - login.timestamp, timedelta(seconds=1))
        
    def test_login_str_representation(self):
        """Test string representation of login"""
        login = Login.objects.create(user=self.user)
        expected_str = f"{self.user.email} logged in at {login.timestamp}"
        self.assertEqual(str(login), expected_str)

    def test_multiple_logins(self):
        """Test multiple login records for the same user"""
        # Create multiple login records
        login1 = Login.objects.create(user=self.user)
        login2 = Login.objects.create(user=self.user)
        
        # Get all logins for the user
        user_logins = Login.objects.filter(user=self.user)
        self.assertEqual(user_logins.count(), 2)
        
        # Verify timestamps are different
        self.assertNotEqual(login1.timestamp, login2.timestamp)

    def test_login_table_name(self):
        """Test that the login table name is set correctly"""
        self.assertEqual(Login._meta.db_table, 'users_login')

    def test_cascade_delete(self):
        """Test that login records are deleted when user is deleted"""
        # Create login records
        login1 = Login.objects.create(user=self.user)
        login2 = Login.objects.create(user=self.user)
        
        # Verify initial count
        self.assertEqual(Login.objects.count(), 2)
        
        # Delete user and verify cascade
        self.user.delete()
        self.assertEqual(Login.objects.count(), 0)