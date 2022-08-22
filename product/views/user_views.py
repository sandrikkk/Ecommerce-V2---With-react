from rest_framework.views import APIView
from rest_framework.response import Response
from product.serializers import UserSerializer, UserSerializerWithToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v 

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                first_name = data['name'],
                username = data['email'],
                email = data['email'],
                password = make_password(data['password'])
            )
            serializer = UserSerializerWithToken(user, many = False)
            return Response(serializer.data)
        except:
            message = {'detail': 'User with this email already exist'}
            return Response(message, status = 400)

class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class GetUsers(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)