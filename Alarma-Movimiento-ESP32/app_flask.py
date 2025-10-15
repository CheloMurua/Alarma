from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import pytz
import threading
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
CORS(app)

# -----------------------------
# Conexión a MySQL
# -----------------------------
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="tu_host_mysql",      # Cambiar por host de PythonAnywhere
            user="tu_usuario_mysql",   # Usuario MySQL
            password="tu_contraseña_mysql", # Contraseña MySQL
            database="alarma"          # Nombre de DB
        )
        return connection
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# -----------------------------
# Callback MQTT: guarda mensajes en MySQL
# -----------------------------
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        descripcion = data.get("descripcion", "Movimiento detectado")

        tz_argentina = pytz.timezone('America/Argentina/Buenos_Aires')
        argentina_time = datetime.now(tz_argentina)

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO movimientos (timestamp, descripcion) VALUES (%s, %s)",
                (argentina_time, descripcion)
            )
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Guardado en DB: {descripcion}")
    except Exception as e:
        print(f"Error al procesar MQTT: {e}")

# -----------------------------
# Inicializar cliente MQTT en hilo separado
# -----------------------------
def start_mqtt():
    client = mqtt.Client()
    client.username_pw_set("tu_usuario_hivemq", "tu_contraseña_hivemq")
    client.tls_set()  # TLS/SSL
    client.on_message = on_message
    client.connect("fab3aac0cefa411c98a7ebdf5a256479.s1.eu.hivemq.cloud", 8883)
    client.subscribe("alarma/movimiento")
    client.loop_forever()

mqtt_thread = threading.Thread(target=start_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

# -----------------------------
# Rutas Flask
# -----------------------------
@app.route('/records', methods=['GET', 'POST'])
def show_records():
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            query = "SELECT id, timestamp, descripcion FROM movimientos"
            params = []

            if start_date and end_date:
                query += " WHERE timestamp BETWEEN %s AND %s"
                params = [start_date + " 00:00:00", end_date + " 23:59:59"]

            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            formatted_records = [
                (r[0], r[1].strftime('%d/%m/%Y %H:%M:%S'), r[2])
                for r in records
            ]

            html_template = ''' 
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Registros de Movimientos</title>
            </head>
            <body>
                <h2>Registros de Movimientos</h2>
                <table border="1">
                    <tr><th>ID</th><th>Timestamp</th><th>Descripcion</th></tr>
                    {% for record in records %}
                        <tr>
                            <td>{{ record[0] }}</td>
                            <td>{{ record[1] }}</td>
                            <td>{{ record[2] }}</td>
                        </tr>
                    {% endfor %}
                </table>
            </body>
            </html>
            '''
            return render_template_string(html_template, records=formatted_records, request=request)
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/records', methods=['GET'])
def get_records_json():
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, descripcion FROM movimientos")
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            json_records = [
                {"id": r[0], "timestamp": r[1].strftime('%d/%m/%Y %H:%M:%S'), "descripcion": r[2]}
                for r in records
            ]
            return jsonify({"status": "success", "records": json_records})
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# -----------------------------
# Ejecutar Flask (PythonAnywhere no necesita __main__)
# -----------------------------
# -----------------------------
# Iniciar la aplicación Flask
# -----------------------------
#if __name__ == '__main__':
#    app.run(debug=True)
