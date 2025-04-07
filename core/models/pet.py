from django.db import models
from core.choices import SEXES

from core.models.client import Client
from core.validators import validateNonNegative, validatePastDate


class Pet(models.Model):
    client_id = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(blank=True, null=True)
    species = models.CharField()
    sex = models.CharField(max_length=1, choices=SEXES)
    breed = models.CharField(blank=True, null=True)
    peso_actual_kg = models.FloatField(
        "Peso en kilogramos", validators=[validateNonNegative]
    )
    fecha_nacimiento = models.DateField(
        blank=True, null=True, validators=[validatePastDate]
    )

    def save(self, *args, **kwargs):
        if not self.id:
            count = Pet.objects.filter(codigo_cliente=self.client_id).count() + 1
            self.id = f"{self.client_id.codigo_cliente}-M{count}"
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return (
    #         f"Mascota: {self.id} - '{self.name}', de {self.client_id.apellido_paterno}"
    #     )
