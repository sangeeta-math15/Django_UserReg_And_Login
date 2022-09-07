from rest_framework import serializers
from .models import Notes


# Notes Serializer
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'user_id']