#define BLYNK_TEMPLATE_ID "TMPL3hECXonZR"
#define BLYNK_TEMPLATE_NAME "Night Patrol Robot"
#define BLYNK_AUTH_TOKEN "7lRfLjWxDb_NZV29Y_YIR6veiZNFl1LP"

#define BLYNK_PRINT Serial
#include<Wire.h>

#define motor11 13
#define motor12 12
#define motor21 14
#define motor22 27

#define soundSensor 26
#define buzzer 25

#define trigPin 18
#define echoPin 19

long duration;
int distanceCm;

#include <SoftwareSerial.h>
#include <TinyGPS++.h>
bool status = false;
TinyGPSPlus gps;
SoftwareSerial GPS(22, 23);

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>



char ssid[] = "OMS";
char pass[] = "12345670";
String textMessage;

String predefined = "http://maps.google.com/maps?q=loc:";
String Message;
String deviceId = "v68D031970D7F7DB";
const char* logServer = "api.pushingbox.com";

const char* ssid1 = "OMS";
const char* password1 = "12345670";



BlynkTimer timer;

BLYNK_WRITE(V0)
{
  int pinValue = param.asInt();
  if (pinValue == 1){
    digitalWrite(motor11, HIGH);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, HIGH);
    digitalWrite(motor22, LOW);
  }
  else{
    digitalWrite(motor11, LOW);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, LOW);
    digitalWrite(motor22, LOW);
  }
}
BLYNK_WRITE(V1)
{
  int pinValue = param.asInt();
  if (pinValue == 1){
    digitalWrite(motor11, LOW);
    digitalWrite(motor12, HIGH);
    digitalWrite(motor21, LOW);
    digitalWrite(motor22, HIGH);
  }
  else{
    digitalWrite(motor11, LOW);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, LOW);
    digitalWrite(motor22, LOW);
  }
 
}
BLYNK_WRITE(V2)
{
  int pinValue = param.asInt();
  if (pinValue == 1){
    digitalWrite(motor11, LOW);
    digitalWrite(motor12, HIGH);
    digitalWrite(motor21, HIGH);
    digitalWrite(motor22, LOW);
  }
  else{
    digitalWrite(motor11, LOW);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, LOW);
    digitalWrite(motor22, LOW);
  }
 
}
BLYNK_WRITE(V3)
{
  int pinValue = param.asInt();
  if (pinValue == 1){
    digitalWrite(motor11, HIGH);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, LOW);
    digitalWrite(motor22, HIGH);
  }
  else{
    digitalWrite(motor11, LOW);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, LOW);
    digitalWrite(motor22, LOW);
  }
 
}
BLYNK_WRITE(V4)
{
  int pinValue = param.asInt();
  if (pinValue == 1){
    //manual
    status = true;
  }
  else{
    //automatic
    status = false;
  }
 
}
void setup() {
  Serial.begin(115200);
   pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
 pinMode(soundSensor, INPUT_PULLUP);
 pinMode(buzzer, OUTPUT);
 pinMode(motor11, OUTPUT);
 pinMode(motor12, OUTPUT);
 pinMode(motor21, OUTPUT);
 pinMode(motor22, OUTPUT);
 
 digitalWrite(buzzer, LOW);
 GPS.begin(9600);
 
 Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

 Message = predefined + String(gps.location.lat(), 8) + ","+ String(gps.location.lng(), 8);
}

void sendNotification(String message){

  Serial.println("- connecting to Home Router SID: " + String(ssid));
 
  WiFi.begin(ssid1, password1);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println();
  Serial.println("- succesfully connected");
  Serial.println("- starting client");
 
  WiFiClient client;

  Serial.println("- connecting to pushing server: " + String(logServer));
  if (client.connect(logServer, 80)) {
    Serial.println("- succesfully connected");
   
    String postStr = "devid=";
    postStr += String(deviceId);
    postStr += "&message_parameter=";
    postStr += String(message);
    postStr += "\r\n\r\n";
   
    Serial.println("- sending data...");
   
    client.print("POST /pushingbox HTTP/1.1\n");
    client.print("Host: api.pushingbox.com\n");
    client.print("Connection: close\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(postStr.length());
    client.print("\n\n");
    client.print(postStr);
  }
  delay(50);
  client.stop();
  Serial.println("- stopping the client");
}

void loop() {
  Blynk.run();
 
  while (GPS.available() > 0){
    gps.encode(GPS.read());
    Message = predefined + String(gps.location.lat(), 8) + ","+ String(gps.location.lng(), 8);
  }
  int soundSensor_status = digitalRead(soundSensor);
if (soundSensor_status == 0)
{
     digitalWrite(buzzer, HIGH);
    digitalWrite(motor11, LOW);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, LOW);
    digitalWrite(motor22, LOW);
    Blynk.logEvent("alert_notify", Message);
    delay(100);
     Blynk.logEvent("alert_notify", "Emergency - Need Help.");
  sendNotification("Emergency - Need Help.");
  sendNotification(Message);
  digitalWrite(buzzer, LOW);`
}
if (status ==true){
 
}
else{
 
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distanceCm= duration*0.034/2;

Serial.println(distanceCm);
if (distanceCm < 15)
{
  Serial.println("Obstacle");
    digitalWrite(motor11, LOW);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, LOW);
    digitalWrite(motor22, LOW);
    delay(1000);
    digitalWrite(motor11, HIGH);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, LOW);
    digitalWrite(motor22, HIGH);
    delay(1000);
}
else{
  Serial.println("Forward");
    digitalWrite(motor11, HIGH);
    digitalWrite(motor12, LOW);
    digitalWrite(motor21, HIGH);
    digitalWrite(motor22, LOW);
}
}
}