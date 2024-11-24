from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
   
 class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'role']




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'role']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', User.KICD_OFFICIAL),  # Default role
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)