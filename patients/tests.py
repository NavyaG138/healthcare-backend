from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User

from .models import Patient


class PatientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="u1@test.com", password="pass12345", name="U1")
        self.other = User.objects.create_user(email="u2@test.com", password="pass12345", name="U2")
        self.client.force_authenticate(self.user)

    def test_requires_auth(self):
        self.client.force_authenticate(None)
        res = self.client.get(reverse("patient-list"))
        self.assertEqual(res.status_code, 401)

    def test_create_and_list_only_own(self):
        Patient.objects.create(name="Not mine", age=40, gender="M", created_by=self.other)
        res = self.client.post(
            reverse("patient-list"), {"name": "Ravi", "age": 30, "gender": "M"}, format="json"
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.get(reverse("patient-list"))
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Ravi")

    def test_cannot_touch_someone_elses_patient(self):
        p = Patient.objects.create(name="Not mine", age=40, gender="M", created_by=self.other)
        url = reverse("patient-detail", args=[p.id])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)


    def test_cannot_update_someone_elses_patient(self):
        p = Patient.objects.create(
            name="Not mine",
            age=40,
            gender="M",
            created_by=self.other,
        )
        url = reverse("patient-detail", args=[p.id])

        res = self.client.patch(
            url,
            {"name": "Changed name"},
            format="json",
        )

        self.assertEqual(res.status_code, 404)
        p.refresh_from_db()
        self.assertEqual(p.name, "Not mine")

    def test_invalid_age(self):
        res = self.client.post(
            reverse("patient-list"), {"name": "X", "age": 500, "gender": "F"}, format="json"
        )
        self.assertEqual(res.status_code, 400)

    
    def test_age_boundary(self):
        too_old = self.client.post(
            reverse("patient-list"),
            {"name": "Older patient", "age": 121, "gender": "F"},
            format="json",
        )
        self.assertEqual(too_old.status_code, 400)

        zero_age = self.client.post(
            reverse("patient-list"),
            {"name": "Newborn", "age": 0, "gender": "F"},
            format="json",
        )
        self.assertEqual(zero_age.status_code, 201)
