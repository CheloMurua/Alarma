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
  
  // Conectar a Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a WiFi");
}

void loop() {
  unsigned long currentMillis = millis();

  // Simular detección de movimiento cada 2 segundos
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    int pirState = HIGH; // Simula que se detectó movimiento
    Serial.println("Movimiento detectado!");

    digitalWrite(buzzerPin, HIGH); // Activa el zumbador
    sendMovementData(); // Envía la notificación
    delay(5000); // Espera 5 segundos antes de desactivar el zumbador
    digitalWrite(buzzerPin, LOW); // Desactiva el zumbador
  }

  /* Este sería el código sin necesidad de simular el movimiento
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

    // Configurar el HTTP para la inserción en SQL
    httpSQL.begin(sqlUrl); 
    httpSQL.addHeader("Content-Type", "application/json");

    // Configurar el HTTP para la notificación
    httpNotification.begin(notificationUrl);
    httpNotification.addHeader("Content-Type", "application/json");

    // Enviar ambas solicitudes en paralelo
    int sqlResponseCode = httpSQL.POST(jsonSQLData);
    int notificationResponseCode = httpNotification.POST(jsonNotificationData);

    // Procesar la respuesta del guardado en base de datos
    if (sqlResponseCode > 0) {
      String sqlResponse = httpSQL.getString();
      Serial.println("Guardado en base de datos: ");
      Serial.println(sqlResponseCode);
      Serial.println(sqlResponse);
    } else {
      Serial.print("Error al guardar en la base de datos: ");
      Serial.println(sqlResponseCode);
    }

    // Procesar la respuesta de la notificación
    if (notificationResponseCode > 0) {
      String notificationResponse = httpNotification.getString();
      Serial.println("Notificación enviada: ");
      Serial.println(notificationResponseCode);
      Serial.println(notificationResponse);
    } else {
      Serial.print("Error al enviar la notificación: ");
      Serial.println(notificationResponseCode);
    }

    // Finalizar ambas conexiones
    httpSQL.end();
    httpNotification.end();
    
  } else {
    Serial.println("Error en la conexión WiFi");
  }
}

/*
 * Antes el sistema para enviar notificación y guardar los datos en una base de datos
 * necesitaban que se realice una acción para luego realizar la otra, al principio primero almacenaba
 * los datos en una base de datos y luego enviaba la notificación, luego probe enviando primero la notificación
 * pero luego investigando encontre esta solución que era mucho mejor porque permite enviar ambas
 * solicitudes HTTP casi en simultaneo, por lo que ahora el código practicamente guarda los datos 
 * y envía la notificación al mismo tiempo optimizando el flujo y permitiendo que se realicen
 * las 2 acciones sin demoras innecesarias entre ambas.

 * El endpoint que utilizo para tratar las notificaciones es un endpoint de prueba que ofrece Wokwi
 * y que estoy utilizando ya que no desarrolle una api para esa tarea.

 * Use WiFi porque ya estaba implementado en el proyecto original, pero MQTT o LoRa podrían haber 
 * sido una mejor opción porque MQTT es más eficiente para manejar redes con muchos dispositivos,
 * usa menos ancho de banda y es ideal para conexiones inestables. Además, tiene baja latencia,
 * lo que lo hace mejor para transmitir datos en tiempo real sin congestionar la red y sin dudas
 * se convierte en la mejor opción para proyectos IoT.
 * Mientras que LoRa ofrece un alcance mucho mayor que WiFi cubriendo grandes distancias y también
 * consume menos energía, lo que sería ideal si los sensores están distribuidos en áreas amplias 
 * (como un campo por ejemplo) y usan baterías.
 * En resumen, MQTT y LoRa, son más escalables y eficientes para grandes redes IoT que WiFi, 
 * aunque WiFi es más rápido y adecuado en redes pequeñas o ya existentes, cómo fue el caso en proyecto
 * que como se menciono antes, ya utilizaba WiFi

 En este link (https://github.com/geracatalas/wokwi_projects/tree/main) se encuentra el código fuente 
 del backend y también de la consulta SQL para crear la base de datos usada en este proyecto
*/