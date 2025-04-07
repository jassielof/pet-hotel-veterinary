from djmoney.models.fields import MoneyField
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from core.models.pet import Pet
from core.validators import validateNonNegative

from core.validators import validatePastDate


class Vaccine(models.Model):
    type = models.CharField(max_length=100)
    manufacturer = models.CharField()
    price = MoneyField(max_digits=24, decimal_places=2, default_currency="BOB")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "manufacturer"], name="unique_vaccine_type_manufacturer"
            )
        ]


class VaccinationSchedule(models.Model):
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
    fecha_vacunacion = models.DateField(
        default=date.today, validators=[validatePastDate]
    )
    doses_administered = models.IntegerField(default=1)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pet_id", "fecha_vacunacion", "vaccine"],
                name="unique_vaccine_schedule",
            )
        ]


class PetMedicalRecord(models.Model):
    consultation_date = models.DateField(
        default=date.today, validators=[validatePastDate]
    )
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
    medical_condition = models.CharField()
    diagnosis_details = models.CharField()
    disease_onset_date = models.DateField(blank=True, null=True, default=date.today)
    treatment_details = models.TextField(blank=True, null=True)

    def clean(self):
        if self.disease_onset_date > self.consultation_date:
            raise ValidationError(
                "La fecha de enfermedad no puede ser mayor a la fecha de consulta."
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pet_id", "consultation_date"],
                name="unique_medical_record",
            )
        ]


class PetWeightRecord(models.Model):
    registration_date = models.DateField(default=date.today)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
    weight_kg = models.FloatField(
        verbose_name="Peso en kilogramos", validators=[validateNonNegative]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pet_id", "registration_date"],
                name="unique_weight_record",
            )
        ]
