from .task import send_email_task
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from account import settings
from .serializer import UserSerializer
from .models import User
import logging

from .util import EncodeDecode

logging.basicConfig(filename="view.log", filemode="w")


class UserRegisterView(APIView):

    def post(self, request):
        """
        Register user with given details
        :param request:
        :return: response
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user_name = serializer.data.get('username')
            user_id = serializer.data.get('id')
            send_email_task.delay(userid=user_id, to=serializer.data['email'], username=user_name),
            return Response({"message": "CHECK EMAIL for verification"})
        except ValueError as e:
            logging.exception(e)
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            logging.exception(e)
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.exception(e)
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
            if user is not None:
                token = EncodeDecode.encode_token(payload={'user_id': user.id})
                return Response(
                    {
                        "message": "logged in successfully",
                        "data": {"token": token}
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


class VerifyToken(APIView):
    def get(self, request, token=None):
        try:
            d_token = EncodeDecode.decode_token(token)
            user_id = d_token.get("user_id")
            username = d_token.get("username")

            u_ = User.objects.get(id=user_id, username=username)
            if u_ is not None:
                u_.is_verified = True
                u_.save()
                return Response({"message": "Email Verified and Registered successfully"})
            return Response({"message": "Try Again......Wrong credentials"})
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)})