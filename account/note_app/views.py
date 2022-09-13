from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.models import User
from .serializer import NoteSerializer
from .models import Notes
import logging
from .util import verifying_token, Cache

logging.basicConfig(filename="view.log", filemode="w")


class NotesCRUD(APIView):
    @verifying_token
    def post(self, request):
        """
        this method is created for inserting the data
        :param request: format of the request
        :return: Response
        """
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            Cache().add_note(request.data.get("user_id"), serializer.data)
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
            note = Cache().get_note(user_id=request.data.get("user_id"))
            return Response(
                {
                    "message": "Here your Note",
                    "data": note.values()
                })
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": str(e)
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
            Cache().add_note(request.data.get("user_id"), serializer.data)
            return Response(
                {
                    "message": "Data updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": str(e)
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
            Cache().delete_note(request.data.get("user_id"), request.data.get("id"))
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
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)