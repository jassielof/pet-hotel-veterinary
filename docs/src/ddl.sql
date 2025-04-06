-- DDL: Data Definition Language
-- Creación de la base de datos en PostgreSQL bajo 'template1'
CREATE DATABASE veterinaria
WITH OWNER = jassiel
ENCODING = 'UTF8'
LC_COLLATE = 'es_BO.UTF-8'
LC_CTYPE = 'es_BO.UTF-8'
TEMPLATE = template1
TABLESPACE = pg_default connection
LIMIT = - 1;

-- Tablas primarias:
CREATE TABLE cliente(
  codigo_cliente text,
  apellido_paterno text NOT NULL,
  cuenta_bancaria text NOT NULL,
  banco text NOT NULL,
  direccion text NOT NULL,
  telefono text NOT NULL,
  correo_electronico text,
  CONSTRAINT PK_cliente PRIMARY KEY (codigo_cliente)
);

CREATE TABLE persona(
  codigo_persona text,
  nombre text NOT NULL,
  relacion_cliente text NOT NULL,
  telefono text NOT NULL,
  direccion text,
  correo_electronico text,
  CONSTRAINT PK_persona PRIMARY KEY (codigo_persona)
);

CREATE TABLE encargado(
  -- Por fines de compatibilidad con django, se hace uso de la columna id,
  -- ya que django no tiene un buen soporte de modelos-tablas sin llaves primarias,
  -- o tablas con llaves primarias compuestas,
  -- para las compuestas se hacen restricciones únicas.
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  codigo_cliente text,
  codigo_persona text,
  CONSTRAINT PK_encargado PRIMARY KEY (id),
  CONSTRAINT UQ_encargado UNIQUE (codigo_cliente, codigo_persona),
  CONSTRAINT FK_encargado_cliente FOREIGN KEY (codigo_cliente) REFERENCES cliente(codigo_cliente) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT FK_encargado_persona FOREIGN KEY (codigo_persona) REFERENCES persona(codigo_persona) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE mascota(
  codigo_mascota text,
  codigo_cliente text,
  alias text DEFAULT 'sin nombre',
  especie text NOT NULL,
  sexo char(1) NOT NULL CHECK (sexo IN ('M', 'F', 'O')),
  raza text DEFAULT 'desconocida',
  peso_actual_kg real NOT NULL CHECK (peso_actual_kg > 0::real),
  fecha_nacimiento date CHECK (fecha_nacimiento <= CURRENT_DATE),
  CONSTRAINT PK_mascota PRIMARY KEY (codigo_mascota),
  CONSTRAINT FK_mascota_cliente FOREIGN KEY (codigo_cliente) REFERENCES cliente(codigo_cliente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE historial_peso(
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  fecha_registro date,
  codigo_mascota text,
  peso_kg real NOT NULL CHECK (peso_kg > 0::real),
  CONSTRAINT PK_historial_peso PRIMARY KEY (id),
  CONSTRAINT UQ_historial_peso UNIQUE (fecha_registro, codigo_mascota),
  CONSTRAINT FK_historial_peso_mascota FOREIGN KEY (codigo_mascota) REFERENCES mascota(codigo_mascota) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE historial_medico(
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  codigo_mascota text,
  fecha_consulta date,
  enfermedad text NOT NULL DEFAULT 'sin enfermedad',
  detalle_diagnostico text NOT NULL DEFAULT 'sin diagnostico',
  fecha_enfermedad date CHECK (fecha_enfermedad <= fecha_consulta),
  detalle_tratamiento text DEFAULT 'sin tratamiento',
  CONSTRAINT PK_historial_medico PRIMARY KEY (id),
  CONSTRAINT UQ_historial_medico UNIQUE (codigo_mascota, fecha_consulta),
  CONSTRAINT FK_historial_medico_mascota FOREIGN KEY (codigo_mascota) REFERENCES mascota(codigo_mascota) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE vacuna(
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  tipo text NOT NULL,
  fabricante text NOT NULL,
  -- Dado que se usa en models.py la clase MoneyField, se necesitan dos columnas para el precio.
  precio_currency varchar(3) NOT NULL,
  precio numeric(24, 4) NOT NULL CHECK (precio >= 0),
  CONSTRAINT PK_vacuna PRIMARY KEY (id),
  CONSTRAINT UQ_vacuna UNIQUE (tipo, fabricante)
);

CREATE TABLE calendario_vacuna(
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  codigo_mascota text NOT NULL,
  fecha_vacunacion date NOT NULL DEFAULT CURRENT_DATE,
  cantidad_aplicada int NOT NULL DEFAULT 1 CHECK (cantidad_aplicada > 0),
  vacuna bigint NOT NULL,
  CONSTRAINT PK_calendario_vacunas PRIMARY KEY (id),
  CONSTRAINT UQ_calendario_vacuna UNIQUE (codigo_mascota, fecha_vacunacion, vacuna),
  CONSTRAINT FK_calendario_vacunas_mascota FOREIGN KEY (codigo_mascota) REFERENCES mascota(codigo_mascota) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT FK_calendario_vacuna_vacuna FOREIGN KEY (vacuna) REFERENCES vacuna(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE habitacion(
  codigo_habitacion text,
  precio_currency varchar(3) NOT NULL,
  precio numeric(24, 4) NOT NULL,
  CONSTRAINT PK_habitacion PRIMARY KEY (codigo_habitacion)
);

CREATE TABLE estadia(
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  codigo_mascota text,
  codigo_habitacion text,
  fecha_registro date DEFAULT CURRENT_DATE,
  fecha_fin date DEFAULT NULL,
  dias_estadia int,
  CONSTRAINT PK_estadia PRIMARY KEY (id),
  CONSTRAINT UQ_estadia UNIQUE (codigo_mascota, codigo_habitacion, fecha_registro),
  CONSTRAINT FK_estadia_mascota FOREIGN KEY (codigo_mascota) REFERENCES mascota(codigo_mascota) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT FK_estadia_habitacion FOREIGN KEY (codigo_habitacion) REFERENCES habitacion(codigo_habitacion) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE servicio(
  codigo_servicio text,
  tipo text NOT NULL CHECK (tipo IN ('alimentación', 'aseo', 'médico', 'otros', 'extras')),
  precio_currency varchar(3) NOT NULL,
  precio numeric(24, 4) NOT NULL CHECK (precio >= 0),
  detalle text DEFAULT 'sin detalle',
  CONSTRAINT PK_servicio PRIMARY KEY (codigo_servicio)
);

CREATE TABLE requerimiento(
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  codigo_servicio text NOT NULL,
  estadia bigint NOT NULL,
  detalle text DEFAULT 'sin detalle',
  cantidad int NOT NULL DEFAULT 1 CHECK (cantidad > 0),
  CONSTRAINT PK_requerimiento PRIMARY KEY (id),
  CONSTRAINT FK_requerimiento_servicio FOREIGN KEY (codigo_servicio) REFERENCES servicio(codigo_servicio) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT FK_requerimiento_estadia FOREIGN KEY (estadia) REFERENCES estadia(id) ON DELETE CASCADE ON UPDATE CASCADE
);

