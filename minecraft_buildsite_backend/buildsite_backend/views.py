from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics

from .models import UserProfile
from .serializers import RegisterSerializer, BaseUserProfileSerializer, PasswordChangeSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProtectedTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}!"}, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BaseUserProfileSerializer()

    def get_object(self):
        return self.request.user.profile

class PublicUserProfileView(generics.RetrieveAPIView):
    serializer_class = BaseUserProfileSerializer()
    queryset = UserProfile.objects.all()
    lookup_field = 'user__username'


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"message": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = serializer.validated_data['new_password']
        if len(new_password) < 8:
            return Response({"message": "Password must be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)
        if not any(char.isupper() for char in new_password):
            return Response({"message": "Password must contain at least one uppercase letter."}, status=status.HTTP_400_BAD_REQUEST)
        if not any(char.islower() for char in new_password):
            return Response({"message": "Password must contain at least one lowercase letter."}, status=status.HTTP_400_BAD_REQUEST)
        if not any(char.isdigit() for char in new_password) and not any(char in '@$!%*?&' for char in new_password):
            return Response({"message": "Password must contain at least one digit or special character."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)