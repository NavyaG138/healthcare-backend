import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("doctors", "0001_initial"),
        ("patients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientDoctorMapping",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("doctor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="mappings", to="doctors.doctor")),
                ("patient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="mappings", to="patients.patient")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="patientdoctormapping",
            constraint=models.UniqueConstraint(fields=("patient", "doctor"), name="unique_patient_doctor"),
        ),
    ]
