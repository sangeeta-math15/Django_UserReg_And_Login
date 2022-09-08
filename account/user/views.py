from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer

import logging
logging.basicConfig(filename="view.log", filemode="w")


class UserRegisterView(APIView):

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
            return Response({"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):

    def post(self, request):
        """
        Checks whether username and password exist in our database and logs in
        :param request:
        :return: response
        """
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user:
                return Response(
                    {
                        "message": "logged in successfully",
                    }, status=status.HTTP_202_ACCEPTED)

            # Login failed
            return Response({"message": "Login failed!"},
                            status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            logging.error(e)
            return Response({"Exception: Authentication failed.."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error(e)
            return Response({'Exception': str(e)}, status=status.HTTP_400_BAD_REQUEST)
