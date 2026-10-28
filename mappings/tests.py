from django.urls import reverse
from rest_framework.test import APITestCase

from doctors.models import Doctor
from patients.models import Patient
from users.models import User

from .models import PatientDoctorMapping


class MappingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="u1@test.com", password="pass12345", name="U1")
        self.other = User.objects.create_user(email="u2@test.com", password="pass12345", name="U2")
        self.patient = Patient.objects.create(name="P", age=20, gender="F", created_by=self.user)
        self.doctor = Doctor.objects.create(
            name="D", specialization="Cardiology", email="d@test.com", created_by=self.other
        )
        self.client.force_authenticate(self.user)

    def test_assign_and_duplicate(self):
        data = {"patient": self.patient.id, "doctor": self.doctor.id}
        self.assertEqual(self.client.post(reverse("mapping-list"), data, format="json").status_code, 201)
        self.assertEqual(self.client.post(reverse("mapping-list"), data, format="json").status_code, 400)

    def test_cannot_assign_to_foreign_patient(self):
        foreign = Patient.objects.create(name="X", age=50, gender="M", created_by=self.other)
        res = self.client.post(
            reverse("mapping-list"), {"patient": foreign.id, "doctor": self.doctor.id}, format="json"
        )
        self.assertEqual(res.status_code, 400)

    def test_list_for_patient_and_delete(self):
        m = PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        res = self.client.get(reverse("mapping-detail", args=[self.patient.id]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        res = self.client.delete(reverse("mapping-detail", args=[m.id]))
        self.assertEqual(res.status_code, 204)
        self.assertFalse(PatientDoctorMapping.objects.exists())

    def test_cannot_delete_someone_elses_mapping(self):
        foreign = Patient.objects.create(name="X", age=50, gender="M", created_by=self.other)
        m = PatientDoctorMapping.objects.create(patient=foreign, doctor=self.doctor)
        res = self.client.delete(reverse("mapping-detail", args=[m.id]))
        self.assertEqual(res.status_code, 404)
        self.assertTrue(PatientDoctorMapping.objects.filter(id=m.id).exists())

    def test_cannot_view_doctors_of_someone_elses_patient(self):
        foreign = Patient.objects.create(name="X", age=50, gender="M", created_by=self.other)
        res = self.client.get(reverse("mapping-detail", args=[foreign.id]))
        self.assertEqual(res.status_code, 404)

    def test_mapping_list_only_shows_own_patients(self):
        foreign = Patient.objects.create(name="X", age=50, gender="M", created_by=self.other)
        PatientDoctorMapping.objects.create(patient=foreign, doctor=self.doctor)
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        res = self.client.get(reverse("mapping-list"))
        self.assertEqual(len(res.data), 1)



    def test_mapping_list_requires_authentication(self):
        self.client.force_authenticate(None)
        res = self.client.get(reverse("mapping-list"))
        self.assertEqual(res.status_code, 401)


    

    def test_nonexistent_patient_or_doctor_rejected(self):
        missing_patient = self.client.post(
            reverse("mapping-list"),
            {"patient": 999999, "doctor": self.doctor.id},
            format="json",
        )
        self.assertEqual(missing_patient.status_code, 400)

        missing_doctor = self.client.post(
            reverse("mapping-list"),
            {"patient": self.patient.id, "doctor": 999999},
            format="json",
        )
        self.assertEqual(missing_doctor.status_code, 400)


    

    def test_deleting_patient_removes_mapping(self):
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor,
        )

        self.patient.delete()

        self.assertFalse(
            PatientDoctorMapping.objects.filter(id=mapping.id).exists()
        )


    def test_deleting_doctor_removes_mapping(self):
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor,
        )

        self.doctor.delete()

        self.assertFalse(
            PatientDoctorMapping.objects.filter(id=mapping.id).exists()
        )