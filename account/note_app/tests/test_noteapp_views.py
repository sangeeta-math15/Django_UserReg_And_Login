import pytest
import json
from django.urls import reverse

@pytest.fixture
def get_token_header(django_user_model, client):
    user = django_user_model.objects.create_user(username='suma', password='1234')
    user.save()
    # login user
    url = reverse('user_login')
    data = {'username': 'suma', 'password': '1234'}
    response = client.post(url, data)
    json_data = json.loads(response.content)
    token = json_data['data']['token']
    header = {'HTTP_TOKEN': token, "content_type": "application/json"}
    return user, header

class TestNotesAPI:
    """
        Test Notes API
    """
    @pytest.mark.django_db
    def test_response_as_create_notes_successfully(self, client, get_token_header):
        # Create user
        user, header = get_token_header

        # Create notes
        url = reverse('NotesCRUD')
        data = {'title': 'Python programming', 'description': 'Python is the most popular language now days.',
                'user_id': user.id}
        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 201
        assert json_data['data']['title'] == 'Python programming'

    @pytest.mark.django_db
    def test_response_as_validation_error_while_create_notes(self, client, get_token_header):
        user, header = get_token_header
        # Create notes
        url = reverse('NotesCRUD')
        data = {'title': '', 'description': '', 'user_id': user.id}
        response = client.post(url, data, **header)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_get_notes_successfully(self, client, get_token_header):
        user, header = get_token_header
        # Create notes
        url = reverse('NotesCRUD')
        data = {'title': 'Python programming', 'description': 'Python is the most popular language now days.',
                'user_id': user.id}
        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 201
        assert json_data['data']['title'] == 'Python programming'

        # Get notes
        user_data = {'user_id': user.id}
        url = reverse('NotesCRUD')
        response = client.get(url, user_data, **header)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_response_as_update_notes_successfully(self, client, get_token_header):
        user, header = get_token_header
        # create note
        url = reverse('NotesCRUD')
        data = {'title': 'Python programming', 'description': 'Python is the most popular language now days.',
                'user_id': user.id}
        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        note_id = json_data['data']['id']
        assert response.status_code == 201
        assert json_data['data']['title'] == 'Python programming'

        # Update notes
        url = reverse('NotesCRUD')
        data = json.dumps(
            {'id': note_id, 'title': 'Django', 'description': 'Django is the most popular framework now days.',
             'user_id': user.id})

        response = client.put(url, data, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_response_as_delete_notes_successfully(self, client, get_token_header):
        user, header = get_token_header

        # Create notes
        url = reverse('NotesCRUD')
        data = {'title': 'Python programming', 'description': 'Python is the most popular language now days.',
                'user_id': user.id}

        response = client.post(url, data, **header)
        json_data = json.loads(response.content)

        assert response.status_code == 201
        assert json_data['data']['title'] == 'Python programming'

        # Delete notes
        note_id = json_data['data']['id']
        url = reverse('NotesCRUD')
        data = {'id': note_id}
        data = json.dumps(data)
        response = client.delete(url, data, **header)
        assert response.status_code == 204
