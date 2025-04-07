from django.db import models
from django.core.exceptions import ValidationError
from djmoney.models.fields import MoneyField
from core.models.accommodation import Stay
from core.choices import SERVICES


class Service(models.Model):

    id = models.CharField(primary_key=True, max_length=10)
    type = models.CharField(max_length=100, choices=SERVICES)
    price = MoneyField(max_digits=24, decimal_places=4, default_currency="BOB")
    details = models.TextField(blank=True, null=True)

    def clean(self):
        if self.price.amount <= 0:
            raise ValidationError("El precio no puede ser negativo.")

    # def __str__(self):
    #     return f"{self.id} - {self.type}"


class ServiceRequest(models.Model):
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE)
    detalle = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return f"({self.stay.pet_id}, {self.stay.roomt_id}, {self.service_id}): {self.amount}"

    # class Meta:
    # unique_together = (('codigo_mascota', 'codigo_habitacion', 'codigo_servicio', 'fecha_registro'),)
