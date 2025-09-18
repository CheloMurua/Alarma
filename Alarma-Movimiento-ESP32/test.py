import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        conn = mysql.connector.connect(
            host="mchelom.mysql.pythonanywhere-services.com",
            user="",
            password="",
            database="mchelom$alarma-esp32"
        )

        if conn.is_connected():
            print("Conexión exitosa a la base de datos!")
        else:
            print("No se pudo conectar a la base de datos.")

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    test_connection()
