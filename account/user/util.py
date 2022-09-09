import jwt
from django.conf import settings
from rest_framework.response import Response
from logging import getLogger

# Logger configuration
logger = getLogger()


def encode_token(payload):
    """
        This method is used to encode the token.
        :param request: It accepts userid,username as parameter.
        :return: It returns the encoded token.
    """
    try:
        if not isinstance(payload, dict):
            return Response({"message": "payload should be dict"})

        encoded_token_id = jwt.encode(payload, key=settings.SECRET_KEY,
                                      algorithm='HS256')
        return encoded_token_id
    except Exception as e:
        logger.exception(e)
        return Response({"message": str(e)})


def decode_token(encoded_token_id):
    """
        This method is used to decode the token.
        :param request: It accepts encoded token as parameter.
        :return: It returns the decoded token.
    """
    try:
        decoded_token = jwt.decode(encoded_token_id, key=settings.SECRET_KEY, algorithms=["HS256"])
        print(decoded_token)
        return decoded_token
    except Exception as e:
        logger.exception(e)
        return Response({"message": str(e)})
