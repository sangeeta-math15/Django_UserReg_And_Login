from rest_framework import serializers
from .models import Notes, Labels


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['id', 'title', 'color', 'font', 'user_id']


class NoteSerializer(serializers.ModelSerializer):
    labels = LabelsSerializer(many=True)

    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'user_id', 'collaborator', 'labels']
        read_only_fields = ['collaborator', 'labels']


class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'collaborator']

    def validate(self, attrs):
        # print(attrs)
        # print(self.context)
        user_id_list = list(map(lambda x: x.id, attrs.get('collaborator')))
        if self.context.get('user_id') in user_id_list:
            raise serializers.ValidationError('logged in user cannot be a collaborator')
        return attrs


class NoteLabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'labels']
