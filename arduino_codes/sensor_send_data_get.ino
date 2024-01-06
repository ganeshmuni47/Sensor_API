#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

const char* ssid = "KKHOME";
const char* password = "drstrange626";
const char* sensor_type = "test_sensor";
String base_url = "http://192.168.31.71:8008/send_data/";

String server_path = base_url + sensor_type + "/?data=";

float get_sensordata() {
  float sensor_value = random(20,100);
  return sensor_value;
}
/* ---------------------------------------- Setup ---------------------------------------- */
void setup() {
  Serial.begin(115200); 
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}
/* ---------------------------------------- Loop ---------------------------------------- */
void loop() {
  if(WiFi.status()== WL_CONNECTED){
    WiFiClient client;
    HTTPClient http;

    String payload = "{%22value%22:"+ String(get_sensordata()) +"}";
    
    // Your Domain name with URL path or IP address with path
    String server_send_url = server_path + payload;
    Serial.println(server_send_url);
    http.begin(client, server_send_url.c_str());

    // Send HTTP GET request
    int httpResponseCode = http.GET();
    
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Free resources
    http.end();
  }
  else {
    Serial.println("WiFi Disconnected");
  }
  delay(10000);
}
