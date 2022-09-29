from django.db.models import Q
from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import NoteSerializer, CollaboratorSerializer, LabelsSerializer, NoteLabelsSerializer
from .models import Notes, Labels
import logging
from .util import verifying_token
from django.db import connections

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
         filter by note collaborators OR user collaborators
        """
        try:
            data = Q(collaborator__id=request.data.get('user_id')) | Q(user_id__id=request.data.get('user_id')) | \
                   Q(labels__id=request.data.get('user_id'))
            n_collaborator = Notes.objects.filter(data).distinct('id')
            serializer = NoteSerializer(n_collaborator, many=True)
            return Response(
                {
                    "message": "Here your Note",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
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


class CollaboratorView(APIView):
    @verifying_token
    def post(self, request):
        # note = Notes.objects.get(pk=request.data.get('id'))
        # print(note)
        #
        # coll = request.data.get('collaborator')
        # note.collaborator.set(coll)
        # data = note.collaborator.all()

        note = Notes.objects.get(id=request.data.get('id'))
        serializer = CollaboratorSerializer(note, data=request.data,
                                            context={"user_id": request.data.get('user_id') or note.user_id.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "successfully  Added Collaborator", "data": serializer.data},
                        status=status.HTTP_201_CREATED)

    @verifying_token
    def delete(self, request):
        try:
            note = Notes.objects.get(id=request.data.get('id'))
            note.collaborator.remove(*request.data.get('collaborator'))
            return Response({"message": "Collaborator deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class LabelsView(APIView):
    @verifying_token
    def post(self, request):
        try:
            serializer = LabelsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label is Created", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def get(self, request):
        try:
            labels = Labels.objects.filter(user_id=request.data.get('user_id'))
            print(labels)
            serializer = LabelsSerializer(labels, many=True)
            return Response({"data": serializer.data})
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def put(self, request):
        try:
            labels = Labels.objects.get(id=request.data.get('id'))
            serializer = LabelsSerializer(labels, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "label updated successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def delete(self, request):
        try:
            labels = Labels.objects.get(id=request.data.get('id'))
            labels.delete()
            return Response({"message": "Label deleted successfully"})
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddLabelNotes(APIView):
    @verifying_token
    def post(self, request):
        try:
            note = Notes.objects.get(id=request.data.get('id'))
            serializer = NoteLabelsSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "added Label to the Note successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def delete(self, request):
        try:
            note = Notes.objects.get(id=request.data.get('id'))
            note.labels.remove(*request.data.get('labels'))
            return Response({"message": "Label deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NoteRawQuery(APIView):
    @verifying_token
    def post(self, request):
        try:
            cursor = connections['default'].cursor()
            cursor.execute("INSERT INTO note_app_notes (title, description, user_id_id) VALUES( %s , %s , %s)",
                           [request.data.get('title'),
                            request.data.get('description'),
                            request.data.get('user_id')])
            cursor.execute('select * from note_app_notes order by id desc limit 1')
            columns = [col[0] for col in cursor.description]
            response = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return Response({"message": " Note successfully added", "data": response})
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def get(self, request):
        try:
            n = Notes.objects.raw('SELECT * FROM note_app_notes where user_id_id = %s',
                                  [request.data.get('user_id')])
            n_data = [model_to_dict(x, ['id', 'title', 'description', 'user_id']) for x in n]

            return Response({"message": "Data Retrieved", "data": n_data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def put(self, request):
        try:
            cursor = connections['default'].cursor()
            cursor.execute('UPDATE note_app_notes set title = %s, description = %s WHERE id = %s and user_id_id=%s',
                           [request.data.get('title'), request.data.get('description'), request.data.get('id'),
                            request.data.get('user_id')])
            cursor.execute('select * from note_app_notes order by id')
            columns = [col[0] for col in cursor.description]
            response = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return Response({"message": " Note successfully updated", "data": response})
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verifying_token
    def delete(self, request):
        try:
            cursor = connections['default'].cursor()
            cursor.execute('DELETE from note_app_notes WHERE id = %s and user_id_id=%s',
                           [request.data.get('id'),
                            request.data.get('user_id')])
            return Response({"message": "deleted note successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
