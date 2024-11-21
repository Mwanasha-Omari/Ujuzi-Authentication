import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

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
