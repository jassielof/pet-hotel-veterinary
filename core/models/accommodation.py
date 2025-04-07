from django.db import models
from djmoney.models.fields import MoneyField
from django.core.exceptions import ValidationError
from datetime import date


class Room(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    price = MoneyField(max_digits=24, decimal_places=4, default_currency="BOB")

    def clean(self):
        if self.price.amount <= 0:
            raise ValidationError("El precio no debe ser negativo.")

    # def __str__(self):
    #     return f"{self.id}: {self.price}"


class StayManager(models.Manager):
    def filter_by_date_range(self, start_date, end_date):
        return self.filter(
            fecha_registro__range=[start_date, end_date],
            fecha_fin__range=[start_date, end_date],
        )


class Stay(models.Model):
    pet_id = models.ForeignKey("Pet", models.CASCADE)
    roomt_id = models.ForeignKey(
        Room,on_delete= models.CASCADE
    )
    check_in_date = models.DateField(default=date.today)
    check_out_date = models.DateField(null=True, blank=True)

    DisplayFields = [
        "codigo_mascota",
        "codigo_habitacion",
        "fecha_registro",
        "fecha_fin",
    ]
    SearchableFields = [
        "codigo_mascota",
        "codigo_habitacion",
        "fecha_registro",
        "fecha_fin",
    ]
    FilterFields = ["fecha_registro", "fecha_fin"]

    @property
    def dias_estadia(self):
        if self.check_in_date and self.check_out_date:
            return self.check_out_date - self.check_in_date
        return None

    def save(self, *args, **kwargs):
        super(Stay, self).save(*args, **kwargs)

    # def clean(self):
    #     if self.fecha_fin < self.fecha_registro and self.fecha_fin:
    #         raise ValidationError("La fecha de salida (fín) debe ser mayor o igual a la fecha de entrada (registro).")

    # def __str__(self):
    #     return f"{self.roomt_id}, {self.pet_id}: ({self.check_in_date}, {self.check_out_date}), {self.dias_estadia}"

    class Meta:
        models.UniqueConstraint(
            fields=["pet_id", "room_id", "check_in_date"],
            name="unique_stay_pet_room",
        )
