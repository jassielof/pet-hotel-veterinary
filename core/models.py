# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# import uuid
from datetime import date
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField
from django.core.exceptions import ValidationError


def validatePastDate(value):
    if value > date.today():
        raise ValidationError("La fecha no puede ser futura.")

class CalendarioVacuna(models.Model):
    codigo_mascota = models.ForeignKey('Mascota', models.DO_NOTHING, db_column='codigo_mascota')
    fecha_vacunacion = models.DateField(default=date.today, validators=[validatePastDate])
    cantidad_aplicada = models.IntegerField(default=1)
    vacuna = models.ForeignKey('Vacuna', models.DO_NOTHING, db_column='vacuna')

    def __str__(self):
        return f"({self.fecha_vacunacion}; {self.codigo_mascota}): {self.vacuna}, {self.cantidad_aplicada}"

    class Meta:
        managed = False
        db_table = 'calendario_vacuna'
        unique_together = (('codigo_mascota', 'fecha_vacunacion', 'vacuna'),)

class Cliente(models.Model):
    LISTA_BANCOS = [
        ('ganadero', 'Banco Ganadero'),
        ('sol', 'Banco Sol'),
        ('nacional', 'Banco Nacional de Bolivia'),
        ('mercantil_santa_cruz', 'Banco Mercantil Santa Cruz'),
        ('bisa', 'Banco BISA'),
        ('credito_bcp', 'Banco de Crédito BCP'),
        ('fie', 'Banco FIE'),
        ('union', 'Banco Unión'),
        ['otro', 'Otro']
    ]

    codigo_cliente = models.CharField(primary_key=True, editable=False)
    apellido_paterno = models.CharField(max_length=50)
    cuenta_bancaria = models.CharField("Número de cuenta bancaria", max_length=25)
    banco = models.CharField(choices=LISTA_BANCOS)
    direccion = models.CharField(max_length=100)
    telefono = PhoneNumberField(region='BO')
    correo_electronico = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.codigo_cliente:
            count = Cliente.objects.count() + 1
            self.codigo_cliente = f"CLI-{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cliente {self.apellido_paterno} - {self.codigo_cliente}, Teléfono: {self.telefono}, Correo-E: {self.correo_electronico}"

    class Meta:
        managed = False
        db_table = 'cliente'


class Persona(models.Model):
    LISTA_RELACIONES = [
        ('cliente', 'Cliente mismo'),
        ('padre', 'Padre'),
        ('madre', 'Madre'),
        ('hermano', 'Hermano'),
        ('hermana', 'Hermana'),
        ('tio', 'Tío'),
        ('tia', 'Tía'),
        ('abuelo', 'Abuelo'),
        ('abuela', 'Abuela'),
        ('primo', 'Primo'),
        ('prima', 'Prima'),
        ('amigo', 'Amigo'),
        ('amiga', 'Amiga'),
        ('vecino', 'Vecino'),
        ('vecina', 'Vecina'),
        ('conocido', 'Conocido'),
        ('conocida', 'Conocida'),
        ('otro', 'Otro')
    ]

    codigo_persona = models.CharField("Carnet de Identidad", primary_key=True, max_length=15)
    nombre = models.CharField()
    relacion_cliente = models.CharField("Relación con el cliente", choices=LISTA_RELACIONES, default='cliente')
    telefono = PhoneNumberField()
    direccion = models.CharField(blank=True, null=True)
    correo_electronico = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Persona: {self.nombre} - {self.codigo_persona}, Relación: {self.relacion_cliente}, {self.telefono}, {self.direccion}, {self.correo_electronico}"

    class Meta:
        managed = False
        db_table = 'persona'


class Encargado(models.Model):
    codigo_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='codigo_cliente')
    codigo_persona = models.ForeignKey('Persona', models.DO_NOTHING, db_column='codigo_persona')

    def __str__(self):
        return f"Cliente: {self.codigo_cliente.codigo_cliente} - {self.codigo_cliente.apellido_paterno}, con persona: {self.codigo_persona.codigo_persona} - {self.codigo_persona.nombre}"

    class Meta:
        managed = False
        db_table = 'encargado'
        unique_together = (('codigo_cliente', 'codigo_persona'),)


class Habitacion(models.Model):
    codigo_habitacion = models.CharField(primary_key=True, max_length=5)
    precio = MoneyField(max_digits=24, decimal_places=4, default_currency='BOB')

    def clean(self):
        if self.precio.amount <= 0:
            raise ValidationError("El precio no debe ser negativo.")

    def __str__(self):
        return f"{self.codigo_habitacion}: {self.precio}"

    class Meta:
        managed = False
        db_table = 'habitacion'

class EstadiaManager(models.Manager):
    def filter_by_date_range(self, start_date, end_date):
        return self.filter(fecha_registro__range=[start_date, end_date], fecha_fin__range=[start_date, end_date])

class Estadia(models.Model):
    codigo_mascota = models.ForeignKey('Mascota', models.DO_NOTHING, db_column='codigo_mascota')
    codigo_habitacion = models.ForeignKey('Habitacion', models.DO_NOTHING, db_column='codigo_habitacion')
    fecha_registro = models.DateField(default=date.today)
    fecha_fin = models.DateField(null=True, blank=True)

    DisplayFields = ['codigo_mascota', 'codigo_habitacion', 'fecha_registro', 'fecha_fin']
    SearchableFields = ['codigo_mascota', 'codigo_habitacion', 'fecha_registro', 'fecha_fin']
    FilterFields = ['fecha_registro', 'fecha_fin']

    @property
    def dias_estadia(self):
        if self.fecha_registro and self.fecha_fin:
            return self.fecha_fin - self.fecha_registro
        return None

    def save(self, *args, **kwargs):
        super(Estadia, self).save(*args, **kwargs)

    # def clean(self):
    #     if self.fecha_fin < self.fecha_registro and self.fecha_fin:
    #         raise ValidationError("La fecha de salida (fín) debe ser mayor o igual a la fecha de entrada (registro).")

    def __str__(self):
        return f"{self.codigo_habitacion}, {self.codigo_mascota}: ({self.fecha_registro}, {self.fecha_fin}), {self.dias_estadia}"

    class Meta:
        managed = False
        db_table = 'estadia'
        unique_together = (('codigo_mascota', 'codigo_habitacion', 'fecha_registro'),)


class HistorialMedico(models.Model):
    fecha_consulta = models.DateField(default=date.today, validators=[validatePastDate])
    codigo_mascota = models.ForeignKey('Mascota', models.DO_NOTHING, db_column='codigo_mascota')
    enfermedad = models.CharField()
    detalle_diagnostico = models.CharField()
    fecha_enfermedad = models.DateField(blank=True, null=True, default=date.today)
    detalle_tratamiento = models.TextField(blank=True, null=True)

    def clean(self):
        if self.fecha_enfermedad > self.fecha_consulta:
            raise ValidationError("La fecha de enfermedad no puede ser mayor a la fecha de consulta.")

    def __str__(self):
        return f"Fecha: {self.fecha_consulta}, Mascota {self.codigo_mascota.codigo_mascota} de {self.codigo_mascota.codigo_cliente.apellido_paterno}."

    class Meta:
        managed = False
        db_table = 'historial_medico'
        unique_together = (('codigo_mascota', 'fecha_consulta'),)


def validateNonNegative(value):
    if value <= 0:
        raise ValidationError("El peso no puede ser negativo.")

class HistorialPeso(models.Model):
    fecha_registro = models.DateField(default=date.today)
    codigo_mascota = models.ForeignKey('Mascota', models.DO_NOTHING, db_column='codigo_mascota')
    peso_kg = models.FloatField(verbose_name="Peso en kilogramos", validators=[validateNonNegative])

    def __str__(self):
        return f"Fecha: {self.fecha_registro} - Código Mascota: ({self.codigo_mascota.codigo_mascota}) - Peso: {self.peso_kg} Kg"

    class Meta:
        managed = False
        db_table = 'historial_peso'
        unique_together = (('fecha_registro', 'codigo_mascota'),)

def discard_old_records(sender, instance, **kwargs):
    max_records = 10
    records_to_keep = HistorialPeso.objects.filter(
        codigo_mascota=instance.codigo_mascota
    ).order_by('-fecha_registro')[:max_records]

    # Delete records beyond the maximum allowed
    HistorialPeso.objects.filter(
        codigo_mascota=instance.codigo_mascota
    ).exclude(
        fecha_registro__in=[record.fecha_registro for record in records_to_keep]
    ).delete()

@receiver(signals.post_save, sender=HistorialPeso)
def keep_latest_records(sender, instance, **kwargs):
    # Call the discard_old_records function after a new record is saved
    discard_old_records(sender, instance, **kwargs)

class Mascota(models.Model):
    LISTA_SEXO = [
        ('M', 'Macho'),
        ('F', 'Hembra'),
        ('O', 'Indefinido')
    ]

    codigo_mascota = models.CharField(primary_key=True, editable=False)
    codigo_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='codigo_cliente', blank=True, null=True)
    alias = models.CharField(blank=True, null=True)
    especie = models.CharField()
    sexo = models.CharField(max_length=1, choices=LISTA_SEXO)
    raza = models.CharField(blank=True, null=True)
    peso_actual_kg = models.FloatField("Peso en kilogramos", validators=[validateNonNegative])
    fecha_nacimiento = models.DateField(blank=True, null=True, default=date.today, validators=[validatePastDate])

    def save(self, *args, **kwargs):
        if not self.codigo_mascota:
            count = Mascota.objects.filter(codigo_cliente=self.codigo_cliente).count() + 1
            self.codigo_mascota = f"{self.codigo_cliente.codigo_cliente}-M{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Mascota: {self.codigo_mascota} - '{self.alias}', de {self.codigo_cliente.apellido_paterno}"

    class Meta:
        managed = False
        db_table = 'mascota'



class Requerimiento(models.Model):
    codigo_servicio = models.ForeignKey('Servicio', models.DO_NOTHING, db_column='codigo_servicio')
    cantidad = models.IntegerField()
    estadia = models.ForeignKey(Estadia, models.DO_NOTHING, db_column='estadia')
    detalle = models.TextField(blank=True, null=True)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a cero.")

    def __str__(self):
        return f"({self.estadia.codigo_mascota}, {self.estadia.codigo_habitacion}, {self.codigo_servicio}): {self.cantidad}"

    class Meta:
        managed = False
        db_table = 'requerimiento'
        # unique_together = (('codigo_mascota', 'codigo_habitacion', 'codigo_servicio', 'fecha_registro'),)


class Servicio(models.Model):
    LISTA_SERVICIO = [
        ('alimentación', 'Alimentación'),
        ('aseo', 'Aseo'),
        ('médico', 'Médico'),
        ('otros', 'Otros'),
        ('extras', 'Extras')
    ]

    codigo_servicio = models.CharField(primary_key=True, max_length=10)
    tipo = models.CharField(max_length=100, choices=LISTA_SERVICIO)
    precio = MoneyField(max_digits=24, decimal_places=2, default_currency='BOB')
    detalle = models.TextField(blank=True, null=True)

    def clean(self):
        if self.precio.amount <= 0:
            raise ValidationError("El precio no puede ser negativo.")

    def __str__(self):
        return f"{self.codigo_servicio} - {self.tipo}"

    class Meta:
        managed = False
        db_table = 'servicio'



class Vacuna(models.Model):
    tipo = models.CharField(max_length=100)
    fabricante = models.CharField()
    precio = MoneyField(max_digits=24, decimal_places=2, default_currency='BOB')

    def __str__(self):
        return f"{self.tipo}: {self.fabricante}, {self.precio}"

    class Meta:
        managed = False
        db_table = 'vacuna'
        unique_together = (('tipo', 'fabricante'),)
