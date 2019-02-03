#include <DHTesp.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
 
#define ssid       "YourSSID"
#define password      "YourPassword"
const char* mqttServer = "MQTT_SERVER";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
const int delayTime = 29 * 60 * 1000;
const char* deviceName = "Czujnik Temperatury Testowy";
DHTesp dht;
uint8_t LED_Pin = D0;
 
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
 
  Serial.begin(115200);
  Serial.println();
  dht.setup(D1, DHTesp::DHT11);
  pinMode(LED_Pin, OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  digitalWrite(LED_Pin, HIGH);
  delay(1000);                
  digitalWrite(LED_Pin, LOW);
  delay(1000);                
  mqttConnection();
}
void getTemperature() {
  delay(dht.getMinimumSamplingPeriod()); /* Delay of amount equal to sampling period */
  float humidity = dht.getHumidity();/* Get humidity value */
  float temperature = dht.getTemperature();/* Get temperature value */
  Serial.print(dht.getStatusString());/* Print status of communication */
  Serial.print("\t");
  Serial.print(humidity, 1);
  Serial.print("\t\t");
  Serial.print(temperature, 1);
  Serial.print("\t\t");
  StaticJsonBuffer<100> JSONbuffer;
  JsonObject& JSONencoder = JSONbuffer.createObject();
  JSONencoder["temperature"] = temperature;
  JSONencoder["humidity"] = humidity;
  JSONencoder["id"] = deviceName;
  char JSONmessageBuffer[100];
  JSONencoder.printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  Serial.println("Sending message to MQTT topic..");
  Serial.println(JSONmessageBuffer);
  if (client.publish("sensors/temperature", JSONmessageBuffer) == true) {
    Serial.println("Success sending temperatures");
  } else {
    Serial.println("Error sending temperatures");
  }
}

 void mqttConnection() {
  client.setServer(mqttServer, mqttPort);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect(deviceName, mqttUser, mqttPassword )) {
      Serial.println("connected");
      registerDevice();
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(5000);
    }
  }
 }
void registerDevice() {
  StaticJsonBuffer<100> JSONbuffer;
  JsonObject& JSONencoder = JSONbuffer.createObject();
  JSONencoder["id"] = deviceName;
  JSONencoder["type"] = "temperature";
  char JSONmessageBuffer[100];
  JSONencoder.printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  Serial.println("Sending message to MQTT topic..");
  Serial.println(JSONmessageBuffer);
  if (client.publish("register", JSONmessageBuffer) == true) {
    Serial.println("Success sending message");
  } else {
    Serial.println("Error sending message");
    mqttConnection();
  }
}
void loop() {
  if (!client.connected()) {
    mqttConnection();
  }
  digitalWrite(LED_Pin, HIGH);
  getTemperature();
  Serial.println("-------------");
  digitalWrite(LED_Pin, LOW);
  delay(delayTime);
  client.loop();
}