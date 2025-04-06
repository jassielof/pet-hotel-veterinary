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


-- DML testing
INSERT INTO persona (codigo_persona, nombre, relacion_cliente, telefono, direccion, correo_electronico)
VALUES
  ('BP001', 'Juan Perez', 'Cliente', '+59112345678', 'Calle 1, La Paz', 'juan.perez@email.com'),
  ('BP002', 'Maria Lopez', 'Proveedor', '+59198765432', 'Avenida 2, Cochabamba', 'maria.lopez@email.com'),
  ('BP003', 'Carlos Rodriguez', 'Cliente', '+59155555555', 'Calle 3, Santa Cruz', 'carlos.rodriguez@email.com'),
  ('BP004', 'Ana Gutierrez', 'Cliente', '+59133333333', 'Calle 4, Sucre', 'ana.gutierrez@email.com'),
  ('BP005', 'Jorge Mendoza', 'Proveedor', '+59199999999', 'Avenida 5, Potosi', 'jorge.mendoza@email.com'),
  ('BP006', 'Laura Fernandez', 'Cliente', '+59177777777', 'Calle 6, Tarija', 'laura.fernandez@email.com'),
  ('BP007', 'Raul Chavez', 'Proveedor', '+59188888888', 'Avenida 7, Oruro', 'raul.chavez@email.com'),
  ('BP008', 'Marta Vargas', 'Cliente', '+59144444444', 'Calle 8, Trinidad', 'marta.vargas@email.com'),
  ('BP009', 'Pedro Romero', 'Cliente', '+59166666666', 'Calle 9, Cobija', 'pedro.romero@email.com'),
  ('BP010', 'Gabriela Torres', 'Proveedor', '+59122222222', 'Avenida 10, Montero', 'gabriela.torres@email.com'),
  ('BP011', 'Luisa Soto', 'Cliente', '+59111111111', 'Calle 11, Quillacollo', 'luisa.soto@email.com'),
  ('BP012', 'Hugo Medina', 'Cliente', '+59177777777', 'Calle 12, El Alto', 'hugo.medina@email.com'),
  ('BP013', 'Silvia Rodriguez', 'Proveedor', '+59199999999', 'Avenida 13, Riberalta', 'silvia.rodriguez@email.com'),
  ('BP014', 'Diego Fernandez', 'Cliente', '+59144444444', 'Calle 14, Warnes', 'diego.fernandez@email.com'),
  ('BP015', 'Eva Morales', 'Proveedor', '+59133333333', 'Avenida 15, Yacuiba', 'eva.morales@email.com'),
  ('BP016', 'Oscar Velasco', 'Cliente', '+59155555555', 'Calle 16, Villa Montes', 'oscar.velasco@email.com'),
  ('BP017', 'Natalia Arce', 'Proveedor', '+59188888888', 'Avenida 17, Camiri', 'natalia.arce@email.com'),
  ('BP018', 'Ricardo Sandoval', 'Cliente', '+59166666666', 'Calle 18, Puerto Suarez', 'ricardo.sandoval@email.com'),
  ('BP019', 'Isabel Castro', 'Cliente', '+59122222222', 'Calle 19, Riberalta', 'isabel.castro@email.com'),
  ('BP020', 'Alejandro Rojas', 'Proveedor', '+59111111111', 'Avenida 20, Villamontes', 'alejandro.rojas@email.com');

INSERT INTO servicio (codigo_servicio, tipo, precio_currency, precio, detalle)
VALUES
  ('SAL001', 'alimentación', 'BOB', 20.50, 'Comida premium para perros'),
  ('SAS002', 'aseo', 'BOB', 35.75, 'Baño y cepillado para gatos'),
  ('SME003', 'médico', 'BOB', 80.00, 'Consulta veterinaria general'),
  ('SOT004', 'otros', 'BOB', 15.25, 'Juguetes para pájaros'),
  ('SEX005', 'extras', 'BOB', 10.00, 'Paseo adicional para perros'),
  ('SAL006', 'alimentación', 'BOB', 15.80, 'Comida balanceada para gatos'),
  ('SAS007', 'aseo', 'BOB', 25.40, 'Corte de uñas para perros'),
  ('SME008', 'médico', 'BOB', 120.30, 'Vacunación completa para gatos'),
  ('SOT009', 'otros', 'BOB', 8.90, 'Hueso masticable para perros'),
  ('SEX010', 'extras', 'BOB', 12.50, 'Juego interactivo para mascotas'),
  ('SAL011', 'alimentación', 'BOB', 18.60, 'Snacks saludables para perros'),
  ('SAS012', 'aseo', 'BOB', 30.00, 'Baño de garrapatas para gatos'),
  ('SME013', 'médico', 'BOB', 90.25, 'Análisis de sangre para perros'),
  ('SOT014', 'otros', 'BOB', 7.80, 'Collar antipulgas para gatos'),
  ('SEX015', 'extras', 'BOB', 15.00, 'Entrenamiento básico para cachorros'),
  ('SAL016', 'alimentación', 'BOB', 22.30, 'Comida dietética para gatos'),
  ('SAS017', 'aseo', 'BOB', 28.75, 'Corte de pelo para perros'),
  ('SME018', 'médico', 'BOB', 100.50, 'Ecografía para gatas preñadas'),
  ('SOT019', 'otros', 'BOB', 9.50, 'Juguete de peluche para perros'),
  ('SEX020', 'extras', 'BOB', 18.00, 'Servicio de pet-sitting para un día');

INSERT INTO habitacion (codigo_habitacion, precio_currency, precio)
VALUES
  ('HAB001', 'BOB', 150.00),
  ('HAB002', 'BOB', 120.50),
  ('HAB003', 'BOB', 200.25),
  ('HAB004', 'BOB', 180.00),
  ('HAB005', 'BOB', 250.75),
  ('HAB006', 'BOB', 130.80),
  ('HAB007', 'BOB', 190.00),
  ('HAB008', 'BOB', 170.60),
  ('HAB009', 'BOB', 220.30),
  ('HAB010', 'BOB', 160.00),
  ('HAB011', 'BOB', 140.25),
  ('HAB012', 'BOB', 210.50),
  ('HAB013', 'BOB', 230.75),
  ('HAB014', 'BOB', 145.90),
  ('HAB015', 'BOB', 205.00),
  ('HAB016', 'BOB', 125.60),
  ('HAB017', 'BOB', 195.40),
  ('HAB018', 'BOB', 180.25),
  ('HAB019', 'BOB', 240.90),
  ('HAB020', 'BOB', 155.00);
