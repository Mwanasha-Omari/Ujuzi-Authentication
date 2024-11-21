from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'password', 'email', 'role']

    # def create(self, validated_data):
    #     user = User(**validated_data)
    #     user.set_password(validated_data['password'])  # Hash the password before saving
    #     user.save()
    #     return user
