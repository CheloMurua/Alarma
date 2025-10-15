#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Datos del broker público HiveMQ (sin usuario/contraseña)
const char* mqttServer = "broker.hivemq.com";
const int mqttPort = 1883;                // puerto TCP sin TLS
const char* mqttUser = "";                 // vacío
const char* mqttPassword = "";             // vacío
const char* topic = "alarma/movimiento";  // el tópico que elegiste

WiFiClient espClient;          
PubSubClient client(espClient);

const int pirPin = 13;
const int buzzerPin = 14;
unsigned long previousMillis = 0;
const long interval = 5000;

void setup() {
  Serial.begin(115200);
  pinMode(pirPin, INPUT);
  pinMode(buzzerPin, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("WiFi conectado");

  client.setServer(mqttServer, mqttPort);
}

void loop() {
  if (!client.connected()) { reconnect(); }
  client.loop();

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    int pirState = HIGH; // Simulación
    if (pirState == HIGH) {
      digitalWrite(buzzerPin, HIGH);
      client.publish(topic, "{\"descripcion\":\"Movimiento detectado\"}");
      delay(5000);
      digitalWrite(buzzerPin, LOW);
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client")) { // Broker público no requiere auth
      Serial.println("MQTT conectado");
    } else {
      Serial.print("Error MQTT, rc=");
      Serial.println(client.state());
      delay(2000);
    }
  }
}
