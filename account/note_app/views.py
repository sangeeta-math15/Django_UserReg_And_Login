import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.models import User
from .serializer import NoteSerializer
from .models import Notes
import logging
from .util import verifying_token

logging.basicConfig(filename="view.log", filemode="w")


class NotesCRUD(APIView):
    @verifying_token
    def post(self, request):

        """
        this method is created for inserting the data
        :param request: format of the request
        :return: Response
        """
        #verifying_token(request)

        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    "message": "Data store successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)

            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def get(self, request):
        """
        this method is created for inserting the data
        :param request: format of the request
        :return: Response
        """
        try:
            notes = Notes.objects.filter(user_id=request.data.get('user_id'))
            serializer = NoteSerializer(notes, many=True)
            return Response(
                {
                    "message": "Here your Note",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "No notes for you"
                },
                status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def put(self, request):
        """
        this method is created for update the data
        :param request: format of the request
        :return: Response
        """
        try:
            note = Notes.objects.get(id=request.data.get("id"))
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "Data updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            logging.error(e)
            return Response(
                {
                    "message": "Data not updated"
                },
                status=status.HTTP_400_BAD_REQUEST)
    @verifying_token
    def delete(self, request):
        """
        this method is created for delete the note
        :param request:format of the request
        :return: response
        """
        try:
            note = Notes.objects.get(id=request.data.get("id"))
            note.delete()
            return Response(
                {
                    "message": "Data deleted"
                },
                status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Data not deleted"
                },
                status=status.HTTP_400_BAD_REQUEST)