#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";

//Datos HiveMQ
const char* mqttServer = "fab3aac0cefa411c98a7ebdf5a256479.s1.eu.hivemq.cloud"; // tu URL
const int mqttPort = 8883;                // puerto TLS (seguro)
const char* mqttUser = "mchelom";       // el usuario que creaste en HiveMQ
const char* mqttPassword = "Cm+2458739150"; // la contraseña que creaste
const char* topic = "alarma/movimiento";          // el tópico que elegiste

WiFiClientSecure espClient;
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

  espClient.setInsecure(); // Para pruebas HiveMQ
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
    if (client.connect("ESP32Client", mqttUser, mqttPassword)) {
      Serial.println("MQTT conectado");
    } else {
      Serial.print("Error MQTT, rc=");
      Serial.println(client.state());
      delay(2000);
    }
  }
}
