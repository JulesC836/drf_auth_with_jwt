from django.contrib.auth.models import Group
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, GroupSerializer
from .models import User

# Create your views here.

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            user_instance = serializer.save()

            response_data = {
                "success": 1,
                "message": "Utilisateur créé avec succès",
                "user": UserSerializer(user_instance, context={'request': request}).data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            
            return Response({"succes":0,"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)
        
        jwt_tokens = serializer.validated_data

        user = serializer.user

        response_data = {
            "succes":1,
            "message": "Connexion réussie",
            "access_token": jwt_tokens['access'],
            "refresh_token": jwt_tokens['refresh'],
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name":user.first_name,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "refresh token requis"}, status=400)
        RefreshToken(refresh_token).blacklist()
        return Response(status=205)

    ###### EXTRAS ########

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission = [permissions.IsAuthenticated]
