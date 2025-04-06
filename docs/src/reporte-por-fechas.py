import psycopg2
from tabulate import tabulate

fecha_a = input("Fecha A de la forma 2023-12-30: ")
fecha_b = input("Fecha B de la forma 2023-12-30: ")

conn = psycopg2.connect(
    database="final_veterinaria",
    user="jassiel",
    password="08112002",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

query = f"""
WITH EstadiaStatus AS (
  SELECT
    id,
    codigo_mascota,
    codigo_habitacion,
    fecha_registro,
    fecha_fin--,
  FROM estadia
  WHERE
    (fecha_fin IS NULL AND fecha_registro <= '{fecha_b}')
    OR (fecha_fin IS NOT NULL AND fecha_registro <= '{fecha_b}' AND fecha_fin >= '{fecha_a}')
)
SELECT
  id,
  codigo_mascota,
  codigo_habitacion,
  fecha_registro,
  fecha_fin,
  CASE
    WHEN fecha_fin IS NULL THEN 'Huésped aun en el hotel'
    ELSE 'Huésped salió el ' || fecha_fin::text
  END AS estado,
  COUNT(*) FILTER (WHERE fecha_fin IS NULL) OVER () AS cantidad_en_hotel,
  COUNT(*) FILTER (WHERE fecha_fin IS NOT NULL) OVER () AS cantidad_atendida
FROM EstadiaStatus;
"""

cursor.execute(query)

result = cursor.fetchall()
headers = [desc[0] for desc in cursor.description]
print(tabulate(result, headers=headers, tablefmt='psql'))

cursor.close()
conn.close()