from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core.choices import BANKS, RELATIONSHIPS


class Client(models.Model):
    codigo_cliente = models.CharField(primary_key=True, editable=False)
    apellido_paterno = models.CharField(max_length=50)
    cuenta_bancaria = models.CharField("Número de cuenta bancaria", max_length=25)
    banco = models.CharField(choices=BANKS)
    direccion = models.CharField(max_length=100)
    telefono = PhoneNumberField(region="BO")
    correo_electronico = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.codigo_cliente:
            count = Client.objects.count() + 1
            self.codigo_cliente = f"CLI-{count}"
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"Cliente {self.apellido_paterno} - {self.codigo_cliente}, Teléfono: {self.telefono}, Correo-E: {self.correo_electronico}"


class Person(models.Model):
    id = models.CharField("Carnet de Identidad", primary_key=True, max_length=15)
    name = models.CharField()
    relacion_cliente = models.CharField(
        "Relación con el cliente", choices=RELATIONSHIPS, default="cliente"
    )
    phone = PhoneNumberField()
    address = models.CharField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # def __str__(self):
    #     return f"Persona: {self.name} - {self.id}, Relación: {self.relacion_cliente}, {self.phone}, {self.address}, {self.email}"


class Caretaker(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"Cliente: {self.client_id.codigo_cliente} - {self.client_id.apellido_paterno}, con persona: {self.person_id.codigo_persona} - {self.person_id.nombre}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["client_id", "person_id"],
                name="unique_caretaker_client_person",
            )
        ]
