from django.urls import reverse
from rest_framework.test import APITestCase


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
            for method in ("get", "post", "put", "delete"):
                res = getattr(self.client, method)(url)
                self.assertEqual(res.status_code, 401, f"{method.upper()} {url}")
