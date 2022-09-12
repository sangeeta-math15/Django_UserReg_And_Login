from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from user.models import User
from user.util import EncodeDecode


def verifying_token(function):
    def wrapper(self, *args, **kwargs):
        request = list(filter(lambda x: isinstance(x, Request), args))[0]

        token = request.headers.get('Token')
        d_token = EncodeDecode.decode_token(token)

        if not d_token:
            raise Exception('user not found')

        user = User.objects.get(id=d_token.get('user_id'))
        if not user:
            return Response({'message': 'unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        request.data.update({'user_id': user.id})
        return function(self, *args, **kwargs)
    return wrapper

