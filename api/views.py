import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from api.serializers import RegisterSerializer
from api.serializers import LoginSerializer


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

class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)  # Adjust as needed

            if user:
                auth_login(request, user)
                
                # Log the login event
                Login.objects.create(user=user)  # Store login event

                response_data = {
                    'message': 'Login successful',
                    'user': {
                        # 'user_id': user.user_id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'role': user.role,
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)

            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    