from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User


class UnauthenticatedAccessTests(APITestCase):
    """Every endpoint except register/login must reject requests without a token."""

    def test_protected_endpoints_return_401(self):
        urls = [
            reverse("patient-list"),
            reverse("patient-detail", args=[1]),
            reverse("doctor-list"),
            reverse("doctor-detail", args=[1]),
            reverse("mapping-list"),
            reverse("mapping-detail", args=[1]),
        ]
        for url in urls:
            for method in ("get", "post", "put", "patch", "delete"):
                res = getattr(self.client, method)(url)
                self.assertEqual(res.status_code, 401, f"{method.upper()} {url}")



class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="jwt@test.com",
            password="StrongPass!123",
            name="JWT Test User",
        )

    def test_valid_access_token_allows_protected_request(self):
        login_response = self.client.post(
            reverse("login"),
            {
                "email": "jwt@test.com",
                "password": "StrongPass!123",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, 200)
        access_token = login_response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        response = self.client.get(reverse("patient-list"))

        self.assertEqual(response.status_code, 200)

    def test_invalid_access_token_is_rejected(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer invalid.token.value"
        )
        response = self.client.get(reverse("patient-list"))

        self.assertEqual(response.status_code, 401)