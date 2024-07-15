import http
import json

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        url = f"http://{settings.AUTH_API_HOST}:{settings.AUTH_API_PORT}/api/v1/auth/login"
        payload = {'login': username, 'password': password, 'agent': 'test'}
        try:
            response = requests.post(url, data=json.dumps(payload))
        except Exception:
            return None
        if response.ok:
            data = response.json()
        else:
            return None
        try:
            token = data['access_token']
        except:
            return None
        url = f"http://{settings.AUTH_API_HOST}:{settings.AUTH_API_PORT}/api/v1/user/token"
        try:
            response = requests.get(url, data=json.dumps(payload), headers={"Authorization": f"Bearer {token}"})
        except Exception:
            return None
        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()
        user = User.objects.filter(email=data['email'])
        if user.exists() == False and data.get('is_superuser') == True:
            user = User.objects.create_superuser(
                username = username,
                password=password
            )
        else:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
