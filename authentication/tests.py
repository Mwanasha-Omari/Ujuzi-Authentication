# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from django.db import IntegrityError
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

# class CustomUserTests(TestCase):
#     def setUp(self):
#         """Set up test data"""
#         self.User = get_user_model()
#         self.test_data = {
#             'username': 'testuser',
#             'email': 'test@example.com',
#             'password': 'testpass123',
#             'first_name': 'Test',
#             'last_name': 'User',
#             'kicd_number': 'UN123'
#         }

#     # Happy Path Tests
#     def test_create_user_successful(self):
#         """Test successful user creation with all fields"""
#         user = self.User.objects.create_user(**self.test_data)
        
#         self.assertEqual(user.username, self.test_data['username'])
#         self.assertEqual(user.email, self.test_data['email'])
#         self.assertEqual(user.first_name, self.test_data['first_name'])
#         self.assertEqual(user.last_name, self.test_data['last_name'])
#         self.assertEqual(user.kicd_number, self.test_data['kicd_number'])
#         self.assertTrue(user.check_password(self.test_data['password']))

#     def test_create_user_minimal_fields(self):
#         """Test user creation with only required fields"""
#         minimal_data = {
#             'username': 'minimaluser',
#             'email': 'minimal@example.com',
#             'password': 'minimal123'
#         }
#         user = self.User.objects.create_user(**minimal_data)
        
#         self.assertEqual(user.username, minimal_data['username'])
#         self.assertEqual(user.email, minimal_data['email'])
#         self.assertEqual(user.first_name, '')
#         self.assertEqual(user.last_name, '')
#         self.assertEqual(user.kicd_number, '')

#     def test_user_string_representation_full_name(self):
#         """Test string representation with full name"""
#         user = self.User.objects.create_user(**self.test_data)
#         expected_str = f"{self.test_data['first_name']} {self.test_data['last_name']}"
#         self.assertEqual(str(user), expected_str)

#     def test_user_string_representation_email_fallback(self):
#         """Test string representation fallback to email"""
#         data = self.test_data.copy()
#         data['first_name'] = ''
#         data['last_name'] = ''
#         user = self.User.objects.create_user(**data)
#         self.assertEqual(str(user), data['email'])

#     def test_add_group_to_user(self):
#         """Test adding group to user"""
#         user = self.User.objects.create_user(**self.test_data)
#         group = Group.objects.create(name='TestGroup')
#         user.groups.add(group)
        
#         self.assertIn(group, user.groups.all())

#     def test_add_permission_to_user(self):
#         """Test adding permission to user"""
#         user = self.User.objects.create_user(**self.test_data)
#         content_type = ContentType.objects.get_for_model(self.User)
#         permission = Permission.objects.create(
#             codename='can_test',
#             name='Can Test',
#             content_type=content_type
#         )
#         user.user_permissions.add(permission)
        
#         self.assertIn(permission, user.user_permissions.all())

#     # Unhappy Path Tests
#     def test_create_user_duplicate_email(self):
#         """Test user creation with duplicate email"""
#         self.User.objects.create_user(**self.test_data)
#         duplicate_data = self.test_data.copy()
#         duplicate_data['username'] = 'another_user'

#         with self.assertRaises(IntegrityError):
#             self.User.objects.create_user(**duplicate_data)

#     def test_create_user_duplicate_username(self):
#         """Test user creation with duplicate username"""
#         self.User.objects.create_user(**self.test_data)
#         duplicate_data = self.test_data.copy()
#         duplicate_data['email'] = 'another@example.com'

#         with self.assertRaises(IntegrityError):
#             self.User.objects.create_user(**duplicate_data)

#     def test_create_user_invalid_email(self):
#         """Test user creation with invalid email"""
#         invalid_data = self.test_data.copy()
#         invalid_data['email'] = 'notanemail'

#         with self.assertRaises(ValidationError):
#             user = self.User.objects.create_user(**invalid_data)
#             user.full_clean()

#     def test_create_user_blank_email(self):
#         """Test user creation with blank email"""
#         invalid_data = self.test_data.copy()
#         invalid_data['email'] = ''

#         with self.assertRaises(ValidationError):
#             user = self.User.objects.create_user(**invalid_data)
#             user.full_clean()

#     def test_create_user_long_names(self):
#         """Test user creation with names exceeding max length"""
#         invalid_data = self.test_data.copy()
#         invalid_data['first_name'] = 'A' * 31  # Max length is 30
#         invalid_data['last_name'] = 'B' * 31   # Max length is 30

#         with self.assertRaises(ValidationError):
#             user = self.User.objects.create_user(**invalid_data)
#             user.full_clean()

#     def test_add_invalid_group(self):
#         """Test adding non-existent group"""
#         user = self.User.objects.create_user(**self.test_data)
        
#         with self.assertRaises(ValueError):
#             user.groups.add(None)

#     def test_save_without_username(self):
#         """Test saving user without username"""
#         invalid_data = self.test_data.copy()
#         del invalid_data['username']

#         with self.assertRaises(TypeError):
#             self.User.objects.create_user(**invalid_data)

#     def test_kicd_number_max_length(self):
#         """Test kicd_number exceeding max length"""
#         invalid_data = self.test_data.copy()
#         invalid_data['kicd_number'] = 'A' * 51  # Max length is 50

#         with self.assertRaises(ValidationError):
#             user = self.User.objects.create_user(**invalid_data)
#             user.full_clean()