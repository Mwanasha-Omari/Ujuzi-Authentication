import logging
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import get_user_model

from users.models import Login
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from api.serializers import RegisterSerializer
from api.serializers import LoginSerializer
from django.contrib.auth import login




# Set up logging
logger = logging.getLogger(__name__)

User = get_user_model()

class UserListView(generics.ListCreateAPIView):
    """
    Handle listing and creating users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        """
        Create a new user.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User created successfully: %s', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error('User creation failed: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handle user detail retrieval, update, and deletion.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk):
        """
        Retrieve a user by ID.
        """
        user = self.get_object()
        serializer = self.get_serializer(user)
        logger.info('User with ID %d retrieved successfully: %s', pk, serializer.data)
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Update a user by ID.
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info('User with ID %d updated successfully: %s', pk, serializer.data)
            return Response(serializer.data)
        else:
            logger.error('User update failed for ID %d: %s', pk, serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a user by ID.
        """
        user = self.get_object()
        user.delete()
        logger.info('User with ID %d deleted successfully.', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        registered_via = 'admin'  # Set the registration source to 'admin'

        # Check if a user with the provided email already exists
        if get_user_model().objects.filter(email=email).exists():
            return Response({'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

   

        # Serialize the request data
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user and set registered_from as 'admin'
            user = serializer.save(registered_from=registered_via)
            
        

            # Prepare response data
            response_data = {
                'message': f"{user.role.capitalize()} {user.first_name} {user.last_name} successfully created",
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role,
                   
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from django.contrib.auth import authenticate, login
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import serializers
# # from .models import Login



# class LoginUser(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
        
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']

#             # Authenticate user
#             user = authenticate(request, email=email, password=password)

#             if user is not None and user.is_active:
#                 login(request, user)

#                 # Generate token
#                 refresh = RefreshToken.for_user(user)
#                 access_token = str(refresh.access_token)

#                 # Log the login event
#                 Login.objects.create(user=user)

#                 # Prepare the response data
#                 response_data = {
#                     'message': 'Login successful',
#                     'token': access_token,  # Only sending access token
#                     'user': {
#                         'first_name': user.first_name,
#                         'last_name': user.last_name,
#                         'email': user.email,
#                         'role': user.role,
#                     }
#                 }
#                 return Response(response_data, status=status.HTTP_200_OK)
            
#             # If authentication failed
#             return Response(
#                 {'detail': 'Invalid credentials'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # If serializer validation failed
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # class LoginUser(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request, *args, **kwargs):
# #         serializer = LoginSerializer(data=request.data)
# #         if serializer.is_valid():
# #             email = serializer.validated_data['email']
# #             password = serializer.validated_data['password']

# #             # Authenticate using email as username (since you've set email as the USERNAME_FIELD)
# #             user = authenticate(request, username=email, password=password)

# #             if user:
# #                 login(request, user)

# #                 # Log the login event
# #                 Login.objects.create(user=user)  # Store login event

# #                 # Prepare the response data
# #                 response_data = {
# #                     'message': 'Login successful',
# #                     'user': {
# #                         'first_name': user.first_name,
# #                         'last_name': user.last_name,
# #                         'email': user.email,
# #                         'role': user.role,
# #                     }
# #                 }
# #                 return Response(response_data, status=status.HTTP_200_OK)

# #             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# # class LoginUser(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request, *args, **kwargs):
# #         serializer = LoginSerializer(data=request.data)
# #         if serializer.is_valid():
# #             email = serializer.validated_data['email']
# #             password = serializer.validated_data['password']
# #             user = authenticate(request, username=email, password=password)  # Adjust as needed

# #             if user:
# #                 auth_login(request, user)
                
# #                 # Log the login event
# #                 Login.objects.create(user=user)  # Store login event

# #                 response_data = {
# #                     'message': 'Login successful',
# #                     'user': {
# #                         'first_name': user.first_name,
# #                         'last_name': user.last_name,
# #                         'email': user.email,
# #                         'role': user.role,
# #                     }
# #                 }
# #                 return Response(response_data, status=status.HTTP_200_OK)

# #             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# import logging
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from django.contrib.auth import authenticate, login, get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.core.exceptions import ValidationError
# from users.models import Login
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# User = get_user_model()
# logger = logging.getLogger(__name__)

# @method_decorator(csrf_exempt, name='dispatch')
# class LoginUser(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []  # Disable authentication for login

#     def create_new_user(self, email, password):
#         """Create a new user with the given email and password"""
#         try:
#             user = User.objects.create_user(
#                 email=email,
#                 password=password,
#                 first_name="New",
#                 last_name="User",
#                 role="user",
#                 is_active=True  # Ensure the user is active
#             )
#             return user
#         except Exception as e:
#             logger.error(f"Error creating new user: {str(e)}")
#             raise

#     def post(self, request, *args, **kwargs):
#         try:
#             # Extract credentials
#             email = request.data.get('email')
#             password = request.data.get('password')

#             # Input validation
#             if not email or not password:
#                 return Response(
#                     {'detail': 'Email and password are required.'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Log authentication attempt
#             logger.info(f"Login/Registration attempt for email: {email}")

#             # Check if user exists
#             existing_user = User.objects.filter(email=email).first()
            
#             if existing_user:
#                 # Try to authenticate existing user
#                 user = authenticate(request, email=email, password=password)
#                 if not user:
#                     return Response(
#                         {'detail': 'Invalid password.'},
#                         status=status.HTTP_401_UNAUTHORIZED
#                     )
#             else:
#                 # Create new user
#                 try:
#                     user = self.create_new_user(email, password)
#                     # Authenticate the new user
#                     user = authenticate(request, email=email, password=password)
#                     logger.info(f"New user created with email: {email}")
#                 except Exception as e:
#                     logger.error(f"Failed to create new user: {str(e)}")
#                     return Response(
#                         {'detail': 'Failed to create new user.'},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )

#             if not user.is_active:
#                 logger.warning(f"Inactive user attempted login: {email}")
#                 return Response(
#                     {'detail': 'This account is inactive.'},
#                     status=status.HTTP_403_FORBIDDEN
#                 )

#             # Login user
#             login(request, user)

#             # Generate JWT tokens
#             refresh = RefreshToken.for_user(user)
#             tokens = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }

#             # Log successful login
#             Login.objects.create(user=user)
#             logger.info(f"Successful login for user: {email}")

#             # Prepare response
#             response_data = {
#                 'message': 'Login successful',
#                 'is_new_user': not existing_user,
#                 'tokens': tokens,
#                 'user': {
#                     'id': user.id,
#                     'first_name': user.first_name,
#                     'last_name': user.last_name,
#                     'email': user.email,
#                     'role': user.role,
#                 }
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         except ValidationError as e:
#             logger.error(f"Validation error during login: {str(e)}")
#             return Response(
#                 {'detail': str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             logger.error(f"Unexpected error during login: {str(e)}")
#             return Response(
#                 {'detail': 'An unexpected error occurred. Please try again.'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, get_user_model
from django.core.exceptions import ValidationError
from users.models import Login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

User = get_user_model()
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class LoginUser(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication for login

    def create_new_user(self, email, password):
        """Create a new user with the given email and password"""
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name="New",
                last_name="User",
                role="user",
                is_active=True  # Ensure the user is active
            )
            return user
        except Exception as e:
            logger.error(f"Error creating new user: {str(e)}")
            raise

    def post(self, request, *args, **kwargs):
        try:
            # Extract credentials
            email = request.data.get('email')
            password = request.data.get('password')

            # Input validation
            if not email or not password:
                return Response(
                    {'detail': 'Email and password are required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log authentication attempt
            logger.info(f"Login/Registration attempt for email: {email}")

            # Check if user exists
            existing_user = User.objects.filter(email=email).first()
            
            if existing_user:
                # Try to authenticate existing user
                user = authenticate(request, email=email, password=password)
                if not user:
                    return Response(
                        {'detail': 'Invalid password.'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                # Create new user
                try:
                    user = self.create_new_user(email, password)
                    # Authenticate the new user
                    user = authenticate(request, email=email, password=password)
                    logger.info(f"New user created with email: {email}")
                except Exception as e:
                    logger.error(f"Failed to create new user: {str(e)}")
                    return Response(
                        {'detail': 'Failed to create new user.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            if not user.is_active:
                logger.warning(f"Inactive user attempted login: {email}")
                return Response(
                    {'detail': 'This account is inactive.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Login user
            login(request, user)

            # Log successful login
            Login.objects.create(user=user)
            logger.info(f"Successful login for user: {email}")

            # Prepare response
            response_data = {
                'message': 'Login successful',
                'is_new_user': not existing_user,
                'user': {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role,
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ValidationError as e:
            logger.error(f"Validation error during login: {str(e)}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            return Response(
                {'detail': 'An unexpected error occurred. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



#     import logging
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from django.contrib.auth import authenticate, login, get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.core.exceptions import ValidationError
# from users.models import Login

# User = get_user_model()
# logger = logging.getLogger(__name__)

# class LoginUser(APIView):
#     permission_classes = [AllowAny]

#     def create_new_user(self, email, password):
#         """Create a new user with the given email and password"""
#         user = User.objects.create_user(
#             email=email,
#             password=password,
#             # Set default values for required fields
#             first_name="New",
#             last_name="User",
#             role="user"  # Set default role
#         )
#         return user

#     def post(self, request, *args, **kwargs):
#         try:
#             # Extract credentials
#             email = request.data.get('email')
#             password = request.data.get('password')

#             # Input validation
#             if not email or not password:
#                 return Response(
#                     {'detail': 'Email and password are required.'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Log authentication attempt
#             logger.info(f"Login/Registration attempt for email: {email}")

#             # Try to authenticate user
#             user = authenticate(request, email=email, password=password)

#             # If user doesn't exist, create new user
#             if not user:
#                 try:
#                     # Check if user exists but password is wrong
#                     existing_user = User.objects.filter(email=email).first()
#                     if existing_user:
#                         return Response(
#                             {'detail': 'Invalid password.'},
#                             status=status.HTTP_401_UNAUTHORIZED
#                         )
                    
#                     # Create new user
#                     user = self.create_new_user(email, password)
#                     logger.info(f"New user created with email: {email}")
#                 except Exception as e:
#                     logger.error(f"Failed to create new user: {str(e)}")
#                     return Response(
#                         {'detail': 'Failed to create new user.'},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )

#             # Check if user is active
#             if not user.is_active:
#                 logger.warning(f"Inactive user attempted login: {email}")
#                 return Response(
#                     {'detail': 'This account is inactive.'},
#                     status=status.HTTP_403_FORBIDDEN
#                 )

#             # Login user
#             login(request, user)

#             # Generate JWT tokens
#             refresh = RefreshToken.for_user(user)
#             tokens = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }

#             # Log successful login
#             Login.objects.create(user=user)
#             logger.info(f"Successful login for user: {email}")

#             # Prepare response
#             response_data = {
#                 'message': 'Login successful',
#                 'is_new_user': not bool(user.last_login),  # Check if this is first login
#                 'tokens': tokens,
#                 'user': {
#                     'id': user.id,
#                     'first_name': user.first_name,
#                     'last_name': user.last_name,
#                     'email': user.email,
#                     'role': user.role,
#                 }
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         except ValidationError as e:
#             logger.error(f"Validation error during login: {str(e)}")
#             return Response(
#                 {'detail': str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             logger.error(f"Unexpected error during login: {str(e)}")
#             return Response(
#                 {'detail': 'An unexpected error occurred. Please try again.'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )