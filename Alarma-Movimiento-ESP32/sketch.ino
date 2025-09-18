#include <WiFi.h>
#include <HTTPClient.h>

// Credenciales de la red Wi-Fi
const char* ssid = "Wokwi-GUEST"; // SSID de la red - Wokwi-GUEST es el wifi de prueba de Wokwi
const char* password = ""; // Contraseña de la conexión WiFi

const int pirPin = 13; // Pin donde está conectado el sensor PIR
const int buzzerPin = 14; // Pin donde está conectado el zumbador

unsigned long previousMillis = 0; // Almacena el tiempo de la última actualización
const long interval = 5000; // Intervalo para simular detección de movimiento (5 segundos)

void setup() {
  Serial.begin(115200);
  pinMode(pirPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  
  // Conecta a Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a WiFi");
}

void loop() {
  unsigned long currentMillis = millis();

  // Simula detección de movimiento cada 2 segundos
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    int pirState = HIGH; // Simula que se detectó movimiento
    Serial.println("Movimiento detectado!");

    digitalWrite(buzzerPin, HIGH); // Activa el zumbador
    sendMovementData(); // Envía la notificación
    delay(5000); // Espera 5 segundos antes de desactivar el zumbador
    digitalWrite(buzzerPin, LOW); // Desactiva el zumbador
  }

  /* Código para el ESP32 sin necesidad de simular el movimiento
  int pirState = digitalRead(pirPin);
  if (pirState == HIGH) {
    Serial.println("Movimiento detectado!");
    digitalWrite(buzzerPin, HIGH); // Activa el zumbador
    sendMovementData(); // Envía la notificación
    delay(5000); // Espera 5 segundos antes de desactivar el zumbador
    digitalWrite(buzzerPin, LOW); // Desactiva el zumbador
  }
  */
}

void sendMovementData() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient httpSQL, httpNotification;

    // URL del endpoint para guardar en SQL
    String sqlUrl = "https://mchelom.pythonanywhere.com/insert";
    // URL del endpoint para enviar la notificación
    String notificationUrl = "https://jsonplaceholder.typicode.com/posts"; //Este es un endpoint de prueba que ofrece wokwi para enviar peticiones 

    // Crea el JSON para el registro en la base de datos
    String jsonSQLData = "{\"descripcion\": \"Movimiento detectado\"}";
    // Crea el JSON para la notificación
    String jsonNotificationData = "{\"title\": \"Movimiento detectado\", \"body\": \"Se ha detectado movimiento en el sensor.\"}";

    // Configura el HTTP para la inserción en SQL
    httpSQL.begin(sqlUrl); 
    httpSQL.addHeader("Content-Type", "application/json");

    // Configura el HTTP para la notificación
    httpNotification.begin(notificationUrl);
    httpNotification.addHeader("Content-Type", "application/json");

    // Envia ambas solicitudes en paralelo
    int sqlResponseCode = httpSQL.POST(jsonSQLData);
    int notificationResponseCode = httpNotification.POST(jsonNotificationData);

    // Procesa la respuesta del guardado en base de datos
    if (sqlResponseCode > 0) {
      String sqlResponse = httpSQL.getString();
      Serial.println("Guardado en base de datos: ");
      Serial.println(sqlResponseCode);
      Serial.println(sqlResponse);
    } else {
      Serial.print("Error al guardar en la base de datos: ");
      Serial.println(sqlResponseCode);
    }

    // Procesa la respuesta de la notificación
    if (notificationResponseCode > 0) {
      String notificationResponse = httpNotification.getString();
      Serial.println("Notificación enviada: ");
      Serial.println(notificationResponseCode);
      Serial.println(notificationResponse);
    } else {
      Serial.print("Error al enviar la notificación: ");
      Serial.println(notificationResponseCode);
    }

    // Finaliza ambas conexiones
    httpSQL.end();
    httpNotification.end();
    
  } else {
    Serial.println("Error en la conexión WiFi");
  }
}