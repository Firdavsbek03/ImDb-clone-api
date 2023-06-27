from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        user_serialized=UserSerializer(data=request.data)
        data={}
        if user_serialized.is_valid():

            user=user_serialized.save()
            # refresh=RefreshToken.for_user(user=user)
            token=Token.objects.get(user=user)

            data['username']=user.username
            data['email']=user.email
            data['token']=token.key
            # data['token']={
            #     "refresh":str(refresh),
            #     "access":str(refresh.access_token),
            # }
            data['message']="Registration Successful"

            return Response(data=data,status=status.HTTP_201_CREATED)

        data=user_serialized.errors
        return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
