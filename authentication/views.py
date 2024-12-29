from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group, Permission
from .models import CustomUser
from .serializers import (
    RegisterSerializer, LoginSerializer, UserProfileSerializer,
    ChangePasswordSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer
)

#class RegisterView(generics.CreateAPIView):
#   queryset = CustomUser.objects.all()
#    serializer_class = RegisterSerializer
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            # Returning custom error messages in response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data['old_password']):
                return Response({"error": "Wrong old password"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordRequestView(APIView):
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                otp = "123456"  # Generate OTP (For simplicity, hardcoded here)
                send_mail('Reset Password OTP', f'Your OTP is {otp}', 'no-reply@myproject.com', [email])
                return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Validate OTP (In real implementation, this should be checked)
            if serializer.data['otp'] == "123456":  # Simulate OTP verification
                request.user.set_password(serializer.data['new_password'])
                request.user.save()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# Admin and Staff Permissions for creating users and assigning roles
class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAdminUser]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    permission_classes = [IsAdminUser]
