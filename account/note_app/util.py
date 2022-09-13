import json
import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from note_app.redis_service import RedisCode
from user.models import User
from user.util import EncodeDecode


class Cache:
    def __init__(self):
        self.cache = RedisCode()

    def get_note(self, user_id):
        """
        for geting note from catch
        :param user_id: user_id of the person
        :return: user_id
        """
        try:
            notes = self.cache.extract(str(user_id))
            if notes is not None:
                return json.loads(notes)
            return {}

        except Exception as e:
            raise e

    def add_note(self, user_id, note):
        """
        for adding the note in catch
        :param user_id: user_id of the person
        :param note: note details
        :return: id and data
        """
        try:
            note_dict = self.get_note(user_id)
            note_dict.update({note.get('id'): note})
            self.cache.save(str(user_id), json.dumps(note_dict))
        except Exception as e:
            logging.error(e)

    def delete_note(self, user_id, note_id):
        """
        deleting the note from the memory
        """
        try:
            note_dict = self.get_note(user_id)
            note_dict.pop(str(note_id))

            self.cache.save(str(user_id), json.dumps(note_dict))

        except Exception as error:
            logging.exception(error)


def verifying_token(function):
    def wrapper(*args, **kwargs):
        request = list(filter(lambda x: isinstance(x, Request), args))[0]

        token = request.headers.get('Token')
        d_token = EncodeDecode.decode_token(token)
        if not d_token:
            raise Exception('user not found')

        user = User.objects.get(id=d_token.get('user_id'))
        if not user:
            return Response({'message': 'unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        request.data.update({'user_id': user.id})
        return function(*args, **kwargs)

    return wrapper
