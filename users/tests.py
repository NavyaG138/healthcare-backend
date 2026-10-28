from django.urls import reverse
from rest_framework.test import APITestCase

from .models import User


class AuthTests(APITestCase):
    def test_register_and_login(self):
        payload = {"name": "Asha", "email": "Asha@Example.com", "password": "Str0ngPass!23"}
        res = self.client.post(reverse("register"), payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertNotIn("password", res.data)
        self.assertTrue(User.objects.filter(email="asha@example.com").exists())

        res = self.client.post(
            reverse("login"),
            {"email": "asha@example.com", "password": "Str0ngPass!23"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)

    def test_duplicate_email_rejected(self):
        User.objects.create_user(email="a@b.com", password="x", name="A")
        res = self.client.post(
            reverse("register"),
            {"name": "B", "email": "a@b.com", "password": "Str0ngPass!23"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)

    def test_wrong_password(self):
        User.objects.create_user(email="a@b.com", password="rightpass123", name="A")
        res = self.client.post(reverse("login"), {"email": "a@b.com", "password": "nope"}, format="json")
        self.assertEqual(res.status_code, 401)

    def test_duplicate_email_different_case_rejected(self):
        self.client.post(
            reverse("register"),
            {"name": "A", "email": "asha@example.com", "password": "Str0ngPass!23"},
            format="json",
        )
        res = self.client.post(
            reverse("register"),
            {"name": "A2", "email": "ASHA@Example.COM", "password": "Str0ngPass!23"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_password_is_hashed(self):
        self.client.post(
            reverse("register"),
            {"name": "A", "email": "a@b.com", "password": "Str0ngPass!23"},
            format="json",
        )
        user = User.objects.get(email="a@b.com")
        self.assertNotEqual(user.password, "Str0ngPass!23")
        self.assertTrue(user.check_password("Str0ngPass!23"))

    def test_weak_password_rejected(self):
        res = self.client.post(
            reverse("register"),
            {"name": "A", "email": "a@b.com", "password": "12345678"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)


    def test_blank_name_rejected(self):
        res = self.client.post(
            reverse("register"),
            {
                "name": "",
                "email": "blankname@example.com",
                "password": "Str0ngPass!23",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 400)