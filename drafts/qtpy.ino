#include <WiFi.h>
#include <WiFiUdp.h>

#define PACKET_SIZE 600
const char* ssid = "SETUP-B73B";
const char* password = "allow0284folded";

WiFiUDP udp;
const int localPort = 4210;  // Port to listen on

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  udp.begin(localPort);
  Serial.printf("Listening for UDP packets on port %d\n", localPort);
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    char incomingPacket[PACKET_SIZE];
    int len = udp.read(incomingPacket, PACKET_SIZE);
    if (len > 0) {
      incomingPacket[len] = 0;  // Null-terminate
    }

    for (int i = 0; i < len; i++) {
      Serial.printf("%02X ", incomingPacket[i]);
    }
    Serial.println();
    
//    Serial.printf("Received UDP packet from %s:%d\n", udp.remoteIP().toString().c_str(), udp.remotePort());
//    Serial.printf("Data: %s\n", incomingPacket);

    // TODO: Parse/use the data here
  }
}


//////////////
#include <WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_NeoPixel.h>

#define PACKET_SIZE 600
const char* ssid = "SETUP-B73B";
const char* password = "allow0284folded";

WiFiUDP udp;
const int localPort = 4210;  // Port to listen on

#define NEOPIXEL_PIN 43
Adafruit_NeoPixel onboard(1, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  udp.begin(localPort);
  Serial.printf("Listening for UDP packets on port %d\n", localPort);

  onboard.begin();
  onboard.show();  // Turn off LED initially
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize == PACKET_SIZE) {
    uint8_t incomingPacket[PACKET_SIZE];
    int len = udp.read(incomingPacket, PACKET_SIZE);

    Serial.printf("Received %d bytes\n", len);
    for (int i = 0; i < len; i++) {
      Serial.printf("%02X ", incomingPacket[i]);
    }
    Serial.println();

    // Update onboard LED to match LED 100's RGB (starts at byte 300)
    uint8_t r = incomingPacket[300];
    uint8_t g = incomingPacket[301];
    uint8_t b = incomingPacket[302];
    onboard.setPixelColor(0, onboard.Color(r, g, b));
    onboard.show();
  } else if (packetSize > 0) {
    Serial.printf("Unexpected packet size: %d bytes\n", packetSize);
    udp.flush();  // Flush bad packet
  }
}
