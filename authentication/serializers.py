from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'password2', 'is_staff', 'is_admin']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    # def validate(self, data):
    #         if not data.get('email'):
    #             raise serializers.ValidationError({"email": "This field is required."})
    #         if not data.get('first_name'):
    #             raise serializers.ValidationError({"first_name": "This field is required."})
    #         if not data.get('last_name'):
    #             raise serializers.ValidationError({"last_name": "This field is required."})
    #         if not data.get('password'):
    #             raise serializers.ValidationError({"password": "This field is required."})

    #         return data

    # def create(self, validated_data):
    #     validated_data.pop('password2')
    #     user = CustomUser.objects.create_user(**validated_data)
    #     return user

    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #         password=validated_data['password'],
    #     )
    #     return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'created_at', 'updated_at']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
