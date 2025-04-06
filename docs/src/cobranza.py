import psycopg2
from tabulate import tabulate
from datetime import datetime

# Parámetros de la conexión a la base de datos.
db_params = {
    'user': 'jassiel',
    'password': '08112002',
    'database': 'final_veterinaria',
    'host': 'localhost'
}

def connect_to_database():
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except Exception as e:
        print(f"Error conectándose a la base de datos: {e}")
        return None

def fetch_pending_estadias(connection):
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT e.id, e.fecha_registro, m.codigo_mascota
            FROM estadia e
            JOIN mascota m ON e.codigo_mascota = m.codigo_mascota
            WHERE e.fecha_fin IS NULL
            """
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error buscando estadías pendientes: {e}")
        return None

def display_estadias(estadias):
    headers = ["Estadía ID", "Fecha Registro", "Mascota Codigo"]
    print(tabulate(estadias, headers=headers, tablefmt="fancy_grid"))

def fetch_services_for_estadia(connection, estadia_id):
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT r.id, s.codigo_servicio, s.tipo, s.precio, r.cantidad
            FROM requerimiento r
            JOIN servicio s ON r.codigo_servicio = s.codigo_servicio
            WHERE r.estadia = %s
            """
            cursor.execute(query, (estadia_id,))
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error al buscar servicio para la estadía '{estadia_id}': {e}")
        return None

def calculate_total_price(services, habitacion_price, estadia_days):
    total_price = 0
    
    # Revisar si el precio de la habitación no es nulo
    if habitacion_price is not None:
        total_price += habitacion_price * estadia_days if estadia_days is not None else 0

    for service in services:
        # Revisar si el precio y la cantidad no son nulos.
        price = service[3]
        quantity = service[4]
        if price is not None and quantity is not None:
            total_price += price * quantity  # Price * Quantity

    return total_price


def update_estadia_fin_date(connection, estadia_id):
    try:
        with connection.cursor() as cursor:
            query = "UPDATE estadia SET fecha_fin = CURRENT_DATE WHERE id = %s"
            print("Consulta:", cursor.mogrify(query, (estadia_id,)))

            cursor.execute(query, (estadia_id,))
            connection.commit()
    except Exception as e:
        print(f"Error al actualizar la fecha de salida de estadía '{estadia_id}': {e}")

def main():
    connection = connect_to_database()
    
    if connection:
        estadias = fetch_pending_estadias(connection)

        if estadias:
            display_estadias(estadias)

            estadia_id_input = input("Ingrese la ID de la estadía a procesar: ")

            try:
                estadia_id = int(estadia_id_input)
            except ValueError:
                print("Opción inválida, ingrese una ID válida.")
                return

            services = fetch_services_for_estadia(connection, estadia_id)
            
            if services:
                habitacion_price_query = "SELECT precio FROM habitacion WHERE codigo_habitacion = (SELECT codigo_habitacion FROM estadia WHERE id = %s)"
                with connection.cursor() as cursor:
                    cursor.execute(habitacion_price_query, (estadia_id,))
                    habitacion_price = cursor.fetchone()[0]

                estadia_days_query = "SELECT dias_estadia FROM estadia WHERE id = %s"
                with connection.cursor() as cursor:
                    cursor.execute(estadia_days_query, (estadia_id,))
                    estadia_days = cursor.fetchone()[0]

                total_price = calculate_total_price(services, habitacion_price, estadia_days)

                update_estadia_fin_date(connection, estadia_id)

                print("\nRecibo:")
                print("Información de la mascota:")

                print("Servicio (basada en los requerimientos):")
                headers = ["Servicio", "Tipo", "Cobranza"]
                services_data = [(s[1], s[2], s[3] * s[4]) for s in services]
                print(tabulate(services_data, headers=headers, tablefmt="fancy_grid"))
                print("Habitación:")
                habitacion_data = [("Dias Estadía", "Cobranza")]
                habitacion_data.append((estadia_days, habitacion_price))
                print(tabulate(habitacion_data, tablefmt="fancy_grid"))
                print(f"Total: {total_price:.2f}")

            else:
                print("Sin servicio en la estadía.")
                print("Actualizando la fecha de salida...")
                update_estadia_fin_date(connection, estadia_id)

        else:
            print("Sin estadías pendientes.")

        connection.close()

if __name__ == "__main__":
    main()
