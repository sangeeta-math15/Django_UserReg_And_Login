from rest_framework.views import APIView
from .models import User
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
import logging


class UserRegister(APIView):

    def post(self, request):
        """
        Register user with given details
        :param request:
        :return: response
        """
        try:
            user_dict = UserSerializer(data=request.data)
            user_dict.is_valid(raise_exception=True)
            user_dict.save()
            return Response({"message": "User successfully registered", "data": user_dict.data},
                            status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"message": e.detail})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)})


class UserLogin(APIView):

    def post(self, request):
        """
        Checks whether username and password exist in our database and logs in
        :param request:
        :return: http response
        """
        try:
            user_dict = UserSerializer(data=request.data, many=True)
            if User.objects.filter(username=user_dict.initial_data.get("username"),
                                   password=user_dict.initial_data.get("password")).exists():
                return Response({"message": "Successfully logged in"},  status=status.HTTP_200_OK)
            return Response({"message": "Invalid Credentials"},  status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)})
