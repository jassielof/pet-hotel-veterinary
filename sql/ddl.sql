-- DDL: Data Definition Language
-- Creación de la base de datos en PostgreSQL bajo 'template0'
-- create database veterinaria
--   with owner = postgres
--   encoding = 'UTF8'
--   lc_collate = 'es_BO.UTF-8'
--   lc_ctype = 'es_BO.UTF-8'
--   template = template1
--   tablespace = pg_default
--   connection limit = -1;

-- Tablas primarias:
CREATE TABLE cliente( -- Revisado
  codigo_cliente text,
    apellido_paterno text NOT NULL,
  cuenta_bancaria text NOT NULL,
  banco text NOT NULL,
  direccion text NOT NULL,
  telefono text NOT NULL,
  correo_electronico text,

  CONSTRAINT PK_cliente PRIMARY KEY (codigo_cliente)
);

CREATE TABLE persona( -- Revisado
  codigo_persona text,
  nombre text NOT NULL,
  relacion_cliente text not null,
  telefono text not null,
  direccion text,
  correo_electronico text,

  CONSTRAINT PK_persona PRIMARY KEY (codigo_persona)
);

CREATE TABLE encargado( -- Revisado
  id BIGINT GENERATED ALWAYS AS IDENTITY not null,
  codigo_cliente text,
  codigo_persona text,
  CONSTRAINT PK_encargado PRIMARY KEY (id),
  CONSTRAINT UQ_encargado UNIQUE (codigo_cliente, codigo_persona),
  CONSTRAINT FK_encargado_cliente FOREIGN KEY (codigo_cliente) REFERENCES cliente(codigo_cliente) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT FK_encargado_persona FOREIGN KEY (codigo_persona) REFERENCES persona(codigo_persona) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE mascota( -- Revisado
  codigo_mascota text,

  codigo_cliente text,

  alias text default 'sin nombre',
  especie text NOT NULL,
  sexo char(1) NOT NULL CHECK (sexo IN ('M', 'F', 'O')),
  raza text default 'desconocida',
  peso_actual_kg real NOT NULL check (peso_actual_kg > 0::real),
  fecha_nacimiento date check (fecha_nacimiento <= CURRENT_DATE),

  CONSTRAINT PK_mascota PRIMARY KEY (codigo_mascota),

  CONSTRAINT FK_mascota_cliente FOREIGN KEY (codigo_cliente) REFERENCES cliente(codigo_cliente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE historial_peso( -- Revisado
  id BIGINT generated always as IDENTITY not null,
  fecha_registro date,

  codigo_mascota text,

  peso_kg real NOT NULL CHECK (peso_kg > 0::real),

  CONSTRAINT PK_historial_peso PRIMARY KEY (id),

  CONSTRAINT UQ_historial_peso UNIQUE (fecha_registro, codigo_mascota),

  CONSTRAINT FK_historial_peso_mascota FOREIGN KEY (codigo_mascota) REFERENCES mascota(codigo_mascota) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE historial_medico( -- Revisado
  id BIGINT GENERATED ALWAYS as IDENTITY not null,

  codigo_mascota text,

  fecha_consulta date,
  enfermedad text NOT NULL default 'sin enfermedad',
  detalle_diagnostico text NOT NULL default 'sin diagnostico',
  fecha_enfermedad date check (fecha_enfermedad <= fecha_consulta),
  detalle_tratamiento text default 'sin tratamiento',

  CONSTRAINT PK_historial_medico PRIMARY KEY (id),

  CONSTRAINT UQ_historial_medico UNIQUE (codigo_mascota, fecha_consulta),

  CONSTRAINT FK_historial_medico_mascota FOREIGN KEY (codigo_mascota) REFERENCES mascota(codigo_mascota) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE vacuna( -- Revisado
  id BIGINT GENERATED ALWAYS AS IDENTITY not null,

  tipo text not null,
  fabricante text not null,
  precio_currency varchar(3) not null,
  precio numeric(24, 4) not null check (precio >= 0),

  CONSTRAINT PK_vacuna PRIMARY KEY (id),

  CONSTRAINT UQ_vacuna UNIQUE (tipo, fabricante)
);

CREATE TABLE calendario_vacuna( -- Revisado
  id BIGINT GENERATED ALWAYS AS IDENTITY not null,

  codigo_mascota text not null,

  fecha_vacunacion date not null default CURRENT_DATE,
  cantidad_aplicada int not null DEFAULT 1 CHECK (cantidad_aplicada > 0),
  vacuna bigint not null,

  CONSTRAINT PK_calendario_vacunas PRIMARY KEY (id),

  constraint UQ_calendario_vacuna UNIQUE (codigo_mascota, fecha_vacunacion, vacuna),

  CONSTRAINT FK_calendario_vacunas_mascota FOREIGN KEY (codigo_mascota) REFERENCES mascota(codigo_mascota) ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT FK_calendario_vacuna_vacuna FOREIGN key (vacuna) REFERENCES vacuna(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE habitacion( -- Revisado
  codigo_habitacion text,

  precio_currency varchar(3) not null,
  precio numeric(24, 4) not null,

  CONSTRAINT PK_habitacion PRIMARY KEY (codigo_habitacion)
);

CREATE TABLE estadia( -- Revisado
  id BIGINT GENERATED ALWAYS AS IDENTITY not null,

  codigo_mascota text,
  codigo_habitacion text,
  fecha_registro date DEFAULT CURRENT_DATE,
  fecha_fin date default null,
  dias_estadia int,

  CONSTRAINT PK_estadia PRIMARY KEY (id),

  CONSTRAINT UQ_estadia UNIQUE (codigo_mascota, codigo_habitacion, fecha_registro),

  CONSTRAINT FK_estadia_mascota FOREIGN KEY (codigo_mascota) REFERENCES mascota(codigo_mascota) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT FK_estadia_habitacion FOREIGN KEY (codigo_habitacion) REFERENCES habitacion(codigo_habitacion) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE servicio( -- Revisado
  codigo_servicio text,

  tipo text NOT NULL CHECK (tipo IN ('alimentación', 'aseo', 'médico', 'otros', 'extras')),
  precio_currency varchar(3) not null,
  precio numeric(24, 4) not null check (precio >= 0),
  detalle text default 'sin detalle',

  CONSTRAINT PK_servicio PRIMARY KEY (codigo_servicio)
);

CREATE TABLE requerimiento( -- Revisado
  id BIGINT GENERATED ALWAYS AS IDENTITY not null,

  codigo_servicio text not null,
  estadia bigint not null,
  detalle text default 'sin detalle',
  cantidad int NOT NULL default 1 CHECK (cantidad > 0),
  CONSTRAINT PK_requerimiento PRIMARY KEY (id),

  CONSTRAINT FK_requerimiento_servicio FOREIGN KEY (codigo_servicio) REFERENCES servicio(codigo_servicio) ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT FK_requerimiento_estadia FOREIGN Key (estadia) REFERENCES estadia(id) ON DELETE CASCADE ON UPDATE CASCADE
);
