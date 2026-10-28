from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User

from .models import Doctor


class DoctorTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(email="o@test.com", password="pass12345", name="O")
        self.viewer = User.objects.create_user(email="v@test.com", password="pass12345", name="V")
        self.doctor = Doctor.objects.create(
            name="Meera", specialization="ENT", email="m@test.com", created_by=self.owner
        )

    def test_everyone_can_see_all_doctors(self):
        self.client.force_authenticate(self.viewer)
        res = self.client.get(reverse("doctor-list"))
        self.assertEqual(len(res.data), 1)

    def test_only_creator_can_edit_or_delete(self):
        url = reverse("doctor-detail", args=[self.doctor.id])
        self.client.force_authenticate(self.viewer)
        self.assertEqual(self.client.put(url, {"name": "x", "specialization": "y", "email": "m@test.com"}, format="json").status_code, 403)
        self.assertEqual(self.client.delete(url).status_code, 403)
        self.client.force_authenticate(self.owner)
        self.assertEqual(self.client.delete(url).status_code, 204)


    def test_blank_doctor_name_rejected(self):
        self.client.force_authenticate(self.owner)
        res = self.client.post(
            reverse("doctor-list"),
            {
                "name": "   ",
                "specialization": "Cardiology",
                "experience_years": 5,
                "email": "blankname@test.com",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 400)


    def test_blank_specialization_rejected(self):
        self.client.force_authenticate(self.owner)
        res = self.client.post(
            reverse("doctor-list"),
            {
                "name": "Anita",
                "specialization": "   ",
                "experience_years": 5,
                "email": "blankspecialization@test.com",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 400)

    

    
    def test_owner_can_update_doctor(self):
        self.client.force_authenticate(self.owner)
        url = reverse("doctor-detail", args=[self.doctor.id])

        res = self.client.patch(
            url,
            {"name": "Meera Sharma"},
            format="json",
        )

        self.assertEqual(res.status_code, 200)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.name, "Meera Sharma")

    def test_viewer_can_retrieve_another_users_doctor(self):
        self.client.force_authenticate(self.viewer)
        url = reverse("doctor-detail", args=[self.doctor.id])

        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], "Meera")


    
    
    def test_duplicate_doctor_email_rejected(self):
        self.client.force_authenticate(self.owner)

        res = self.client.post(
            reverse("doctor-list"),
            {
                "name": "Another Doctor",
                "specialization": "Cardiology",
                "experience_years": 5,
                "email": "m@test.com",
            },
            format="json",
        )

        self.assertEqual(res.status_code, 400)

    def test_experience_above_70_rejected(self):
        self.client.force_authenticate(self.owner)

        res = self.client.post(
            reverse("doctor-list"),
            {
                "name": "Experienced Doctor",
                "specialization": "Cardiology",
                "experience_years": 71,
                "email": "experienced@test.com",
            },
            format="json",
        )

        self.assertEqual(res.status_code, 400)

