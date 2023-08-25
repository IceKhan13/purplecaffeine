"""Tests file."""
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

import json


class UnitTests(TestCase):
    """Unit tests."""

    def setUp(self) -> None:
        admin_username = "admin"
        admin_pass = "admin"
        User.objects.create_superuser(admin_username, "admin@admin.com", admin_pass)

    def get_token(self):
        """Get token."""

        data = {"username": f"admin", "password": f"admin"}

        url = reverse("token_obtain_pair")
        login = self.client.post(url, data=data, content_type="application/json")
        return json.loads(login.content)["access"]

    def test_get_token(self):
        """
        Ensure we can get a token.
        """

        data = {"username": "admin", "password": "admin"}

        url = reverse("token_obtain_pair")
        login = self.client.post(url, data=data, content_type="application/json")
        self.assertEquals(login.status_code, 200)

        token_refresh = json.loads(login.content)["refresh"]

        url = reverse("token_refresh")
        refresh = self.client.post(
            url, data={"refresh": f"{token_refresh}"}, content_type="application/json"
        )
        self.assertEquals(refresh.status_code, 200)

        token_access = json.loads(login.content)["access"]

        url = reverse("token_verify")
        verify = self.client.post(
            url, data={"token": f"{token_access}"}, content_type="application/json"
        )
        self.assertEquals(verify.status_code, 200)

    def test_get_swagger(self):
        """
        Ensure we can get a swagger.
        """

        url = reverse("swagger-ui")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_trials(self):
        """Tests getting trials."""

        data = {
            "name": "My super experiment",
            "description": "My super experiments desciption",
            "storage": {"__type__": "PurpleCaffeineBackend"},
            "metrics": [["nb_qubits", 2]],
            "parameters": [["OS", "ubuntu"]],
            "circuits": [],
            "operators": [],
            "artifacts": [],
            "texts": [],
            "arrays": [],
            "tags": [],
        }
        post = self.client.post(
            "/api/trials/",
            data=data,
            headers={"Authorization": f" Bearer {self.get_token()}"},
            content_type="application/json",
        )
        self.assertEquals(post.status_code, 201)

        get_all = self.client.get(
            "/api/trials/",
            headers={"Authorization": f" Bearer {self.get_token()}"},
            content_type="application/json",
        )
        self.assertEquals(get_all.status_code, 200)

        get_one = self.client.get(
            "/api/trials/",
            headers={"Authorization": f" Bearer {self.get_token()}"},
            content_type="application/json",
        )
        self.assertEquals(get_one.status_code, 200)

        delete = self.client.delete(
            "/api/trials/1/",
            headers={"Authorization": f" Bearer {self.get_token()}"},
            content_type="application/json",
        )
        self.assertEquals(delete.status_code, 204)
