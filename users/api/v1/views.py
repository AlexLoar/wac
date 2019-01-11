from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from .permissions import IsOwner
from .serializers import TokenSerializer, CustomUserSerializer


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        token_serializer = TokenSerializer(data=request.data)
        if token_serializer.is_valid():
            token, _ = Token.objects.get_or_create(user=token_serializer.user)
            return Response({'token': token.key, 'user': token.user.id},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': token_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserDetail(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, IsOwner)
