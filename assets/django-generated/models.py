# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CalendarioVacunas(models.Model):
    codigo_mascota = models.OneToOneField('Mascota', models.DO_NOTHING, db_column='codigo_mascota', primary_key=True)
    fecha_vacunacion = models.DateField()
    tipo = models.ForeignKey('Vacuna', models.DO_NOTHING, db_column='tipo')
    fabricante = models.TextField()

    class Meta:
        managed = False
        db_table = 'calendario_vacunas'
        unique_together = (('codigo_mascota', 'fecha_vacunacion', 'tipo', 'fabricante'),)


class Cliente(models.Model):
    codigo_cliente = models.TextField(primary_key=True)
    apellido_paterno = models.TextField()
    cuenta_bancaria = models.TextField()
    direccion = models.TextField()
    telefono = models.TextField()

    class Meta:
        managed = False
        db_table = 'cliente'


class Encargado(models.Model):
    codigo_cliente = models.OneToOneField(Cliente, models.DO_NOTHING, db_column='codigo_cliente', primary_key=True)
    codigo_persona = models.ForeignKey('Persona', models.DO_NOTHING, db_column='codigo_persona')

    class Meta:
        managed = False
        db_table = 'encargado'
        unique_together = (('codigo_cliente', 'codigo_persona'),)


class Estadia(models.Model):
    codigo_mascota = models.OneToOneField('Mascota', models.DO_NOTHING, db_column='codigo_mascota', primary_key=True)
    codigo_habitacion = models.ForeignKey('Habitacion', models.DO_NOTHING, db_column='codigo_habitacion')
    fecha_registro = models.DateField()
    dias_estadia = models.FloatField()
    fecha_fin = models.DateField()
    precio_total = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'estadia'
        unique_together = (('codigo_mascota', 'codigo_habitacion', 'fecha_registro'),)


class Habitacion(models.Model):
    codigo_habitacion = models.TextField(primary_key=True)
    capacidad = models.IntegerField()
    precio = models.TextField()  # This field type is a guess.
    tipo = models.TextField()
    libre = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'habitacion'


class HistorialMedico(models.Model):
    codigo_mascota = models.OneToOneField('Mascota', models.DO_NOTHING, db_column='codigo_mascota', primary_key=True)
    fecha_consulta = models.DateField()
    enfermedad = models.TextField()
    detalle_diagnostico = models.TextField()
    fecha_enfermedad = models.DateField(blank=True, null=True)
    detalle_tratamiento = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historial_medico'
        unique_together = (('codigo_mascota', 'fecha_consulta'),)


class HistorialPeso(models.Model):
    fecha_registro = models.DateField(primary_key=True)
    codigo_mascota = models.ForeignKey('Mascota', models.DO_NOTHING, db_column='codigo_mascota')
    peso = models.FloatField()

    class Meta:
        managed = False
        db_table = 'historial_peso'
        unique_together = (('fecha_registro', 'codigo_mascota'),)


class Mascota(models.Model):
    codigo_mascota = models.TextField(primary_key=True)
    codigo_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='codigo_cliente', blank=True, null=True)
    alias = models.TextField(blank=True, null=True)
    especie = models.TextField()
    sexo = models.TextField()
    raza = models.TextField(blank=True, null=True)
    peso_actual = models.FloatField()
    edad_meses = models.FloatField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mascota'


class Persona(models.Model):
    codigo_persona = models.TextField(primary_key=True)
    nombre_persona = models.TextField()
    relacion = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persona'


class Requerimiento(models.Model):
    codigo_mascota = models.OneToOneField(Estadia, models.DO_NOTHING, db_column='codigo_mascota', primary_key=True)
    codigo_habitacion = models.TextField()
    codigo_servicio = models.ForeignKey('Servicio', models.DO_NOTHING, db_column='codigo_servicio')
    fecha_registro = models.DateField()
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'requerimiento'
        unique_together = (('codigo_mascota', 'codigo_habitacion', 'codigo_servicio', 'fecha_registro'),)


class Servicio(models.Model):
    codigo_servicio = models.TextField(primary_key=True)
    tipo = models.TextField()
    precio = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'servicio'


class Vacuna(models.Model):
    tipo = models.TextField(primary_key=True)
    fabricante = models.TextField()
    precio = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'vacuna'
        unique_together = (('tipo', 'fabricante'),)
