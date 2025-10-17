from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timezone
import pytz  # Librería para manejo de zonas horarias

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas de la aplicación

# Función para crear la conexión a la base de datos
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="mchelom.mysql.pythonanywhere-services.com",
            user="mchelom",
            password="Cmsam+2458739150",
            database="mchelom$alarma-esp32"
        )
        return connection
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Ruta para insertar datos en la base de datos
@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    descripcion = data.get('descripcion')

    if descripcion:
        try:
            # Hora actual en la zona horaria de Argentina
            tz_argentina = pytz.timezone('America/Argentina/Buenos_Aires')
            argentina_time = datetime.now(tz_argentina)

            # Crea conexión a la base de datos
            connection = create_connection()
            if connection and connection.is_connected():
                cursor = connection.cursor()
                sql_query = "INSERT INTO movimientos (timestamp, descripcion) VALUES (%s, %s)"
                cursor.execute(sql_query, (argentina_time, descripcion))
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({"status": "success", "message": "Movimiento registrado"}), 200
        except Error as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Datos inválidos"}), 400

# Ruta para mostrar los registros en formato HTML con tabla, CSS y filtro de fechas
@app.route('/records', methods=['GET', 'POST'])
def show_records():
    try:
        connection = create_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()

            # Filtro de fechas basado en la solicitud POST (si existe)
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
            connection.close()

            # Formatea los registros
            formatted_records = []
            for record in records:
                formatted_timestamp = record[1].strftime('%d/%m/%Y %H:%M:%S')
                formatted_records.append((record[0], formatted_timestamp, record[2]))

            # HTML para mostrar la tabla con filtro de fechas y actualización en tiempo real
            html_template = '''
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Registros de Movimientos</title>
                <style>
                    body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; padding: 20px; }
                    table { width: 100%; border-collapse: collapse; font-size: 18px; box-shadow: 0 2px 3px rgba(0,0,0,0.1); }
                    th, td { padding: 12px; border-bottom: 1px solid #ddd; }
                    th { background-color: #333; color: #fff; cursor: pointer; }
                    tr:nth-child(even) { background-color: #f2f2f2; }
                    .filter-form { display: flex; justify-content: center; margin-bottom: 20px; }
                    .filter-form input[type="date"] { margin-right: 10px; }
                </style>
            </head>
            <body>
                <h2>Registros de Movimientos</h2>

                <!-- Formulario de filtro de fechas -->
                <form class="filter-form" method="POST" action="/records">
                    <input type="date" name="start_date" required max="{{ current_date }}" value="{{ request.form.get('start_date', '') }}">
                    <input type="date" name="end_date" required max="{{ current_date }}" value="{{ request.form.get('end_date', '') }}">
                    <button type="submit">Filtrar</button>
                </form>

                <table>
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)">ID</th>
                            <th onclick="sortTable(1)">Fecha y Hora</th>
                            <th onclick="sortTable(2)">Descripción</th>
                        </tr>
                    </thead>
                    <tbody id="records-body">
                        {% for record in records %}
                        <tr>
                            <td>{{ record[0] }}</td>
                            <td>{{ record[1] }}</td>
                            <td>{{ record[2] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>

                <script>
                    let previousData = null;

                    function requestNotificationPermission() {
                        if (Notification.permission !== "granted") {
                            Notification.requestPermission().then(permission => {
                                if (permission === "granted") {
                                    console.log("Permiso de notificación concedido.");
                                }
                            });
                        }
                    }

                    function showNotification() {
                        if (Notification.permission === "granted") {
                            new Notification("Nuevo Movimiento Detectado", {
                                body: "¡Se ha detectado un nuevo movimiento en el sistema!",
                                icon: "https://example.com/icon.png"
                            });
                        }
                    }

                    function fetchData() {
                        fetch('/api/records')
                            .then(response => response.json())
                            .then(data => {
                                if (data.status === 'success') {
                                    const newData = JSON.stringify(data.records);
                                    if (previousData && previousData !== newData) {
                                        showNotification();
                                    }
                                    previousData = newData;
                                }
                            })
                            .catch(error => console.error('Error al obtener datos:', error));
                    }

                    setInterval(fetchData, 5000);
                    requestNotificationPermission();

                    function sortTable(columnIndex) {
                        const table = document.querySelector('table');
                        const tbody = table.querySelector('tbody');
                        const rows = Array.from(tbody.querySelectorAll('tr'));
                        let isAscending = table.dataset.sortDirection === 'ascending';

                        if (table.dataset.sortDirection === undefined) {
                            isAscending = false;
                            table.dataset.sortDirection = 'descending';
                        }

                        rows.sort((rowA, rowB) => {
                            const cellA = rowA.querySelectorAll('td')[columnIndex].textContent.trim();
                            const cellB = rowB.querySelectorAll('td')[columnIndex].textContent.trim();

                            if (columnIndex === 1) {
                                const [dateA, timeA] = cellA.split(' ');
                                const [dateB, timeB] = cellB.split(' ');
                                const [dayA, monthA, yearA] = dateA.split('/').map(Number);
                                const [dayB, monthB, yearB] = dateB.split('/').map(Number);
                                const [hoursA, minutesA] = timeA.split(':').map(Number);
                                const [hoursB, minutesB] = timeB.split(':').map(Number);
                                const dateTimeA = new Date(yearA, monthA - 1, dayA, hoursA, minutesA);
                                const dateTimeB = new Date(yearB, monthB - 1, dayB, hoursB, minutesB);
                                return isAscending ? dateTimeA - dateTimeB : dateTimeB - dateTimeA;
                            } else {
                                return isAscending
                                    ? cellA.localeCompare(cellB, 'es', { numeric: true })
                                    : cellB.localeCompare(cellA, 'es', { numeric: true });
                            }
                        });

                        rows.forEach(row => tbody.appendChild(row));
                        table.dataset.sortDirection = isAscending ? 'descending' : 'ascending';
                    }

                    document.addEventListener('DOMContentLoaded', () => {
                        sortTable(1);
                    });

                    document.querySelector('input[name="start_date"]').max = document.querySelector('input[name="end_date"]').max = new Date().toISOString().split("T")[0];
                </script>
            </body>
            </html>
            '''

            return render_template_string(html_template, records=formatted_records, request=request), 200

    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint para obtener registros en formato JSON
@app.route('/api/records', methods=['GET'])
def get_records_json():
    try:
        connection = create_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT id, timestamp, descripcion FROM movimientos")
            records = cursor.fetchall()
            cursor.close()
            connection.close()

            json_records = [
                {
                    "id": record[0],
                    "timestamp": record[1].astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "descripcion": record[2]
                }
                for record in records
            ]
            return jsonify({"status": "success", "records": json_records}), 200

    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ENDPOINTS para Grafana
@app.route('/', methods=['GET'])
def health_check():
    return 'OK', 200

@app.route('/search', methods=['POST'])
def search_grafana():
    return jsonify(['Movimiento Detectado'])

@app.route('/query', methods=['POST'])
def query_grafana():
    req = request.get_json()
    response_data = []

    for target in req.get('targets', []):
        metric_name = target.get('target')
        connection = create_connection()
        if not connection or not connection.is_connected():
            continue

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT timestamp, descripcion FROM movimientos")
            records = cursor.fetchall()
            cursor.close()
            connection.close()

            datapoints = []
            for record in records:
                ts_utc = record['timestamp'].astimezone(pytz.utc).timestamp() * 1000
                datapoints.append([1, int(ts_utc)])

            response_data.append({
                "target": metric_name,
                "datapoints": datapoints
            })

        except Exception as e:
            print(f"Error en /query: {e}")
            if connection and connection.is_connected():
                connection.close()
            continue

    return jsonify(response_data)

# Iniciar la aplicación
# if __name__ == '__main__':
#     app.run(debug=True)