import json
import pytest
from rest_framework.reverse import reverse


class TestUserLoginAPI:
    """
    Test User API
    """
    @pytest.mark.django_db
    def test_response_as_registration_successful(self, client, django_user_model):
        # Create user

        url = reverse('user_registration')
        # Registration succesfull
        data = {'first_name': 'shree', 'last_name': 'math',
                'username': 'shree@123', 'password': '1234',
                'phone': '+91-9876567891', 'email': 'shree@gmail.com'}
        response = client.post(url, data)
        assert response.status_code == 201
        json_data = json.loads(response.content)
        assert json_data['data']['username'] == 'shree@123'

    @pytest.mark.django_db
    def test_response_as_invalid_userinput(self, client, django_user_model):
        user = django_user_model.objects.create_user(first_name='shree', last_name='math',
                                                     username='shree@123', password='1234',
                                                     phone='+91-9876567891', email='shree@gmal.com')
        url = reverse('user_registration')
        # invalid input
        data = {
            "username": "shree",
            "phone": "+91-9876567891",
            "email": "shree@gmal.com"
        }
        response = client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_username_is_already_exist(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username="shree", password="shree@123",
                                                     phone="+91-9876567891", email="shree@gmal.com")

        url = reverse("user_registration")
        # Username is already taken
        data = {
            "username": "shree",
            "phone": "+91-9876567891",
            "password": "shree@123",
            "email": "shree@gmal.com"
        }
        response = client.post(url, data)
        assert response.status_code == 400

    """
        Test Login API
    """
    @pytest.mark.django_db
    def test_response_as_login_succssful(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='shree', password='7777')
        url = reverse('user_login')
        # Login successful
        data = {'username':'shree', 'password':'7777'}
        response = client.post(url, data)
        assert response.status_code == 202


    @pytest.mark.django_db
    def test_response_as_login_failed(self, client, django_user_model):
        #create user
        user = django_user_model.objects.create_user(username='shree', password='7777')
        url = reverse('user_login')
        #login successful
        data = {'username':'shree', 'password':'1234'}
        response = client.post(url, data)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_response_as_authentication(self, client, django_user_model):
        # create user
        user = django_user_model.objects.create_user(username='shree', password='7777')
        url = reverse('user_login')
        # login successful
        data = {'username': 'shre', 'password': ''}
        response = client.post(url, data)
        assert response.status_code == 401