#include <Arduino.h>

namespace {
constexpr unsigned long BAUD = 115200;
constexpr uint8_t LED_PIN = LED_BUILTIN;
String line;

void respond(const String& body) {
  Serial.println(body);
}

void handleCommand(const String& input) {
  // Small parser for the constrained ATmega328P target.
  if (input.indexOf("\"cmd\":\"ping\"") >= 0) {
    respond("{\"id\":1,\"ok\":true,\"result\":{\"pong\":true}}");
    return;
  }

  if (input.indexOf("\"cmd\":\"status\"") >= 0) {
    respond("{\"id\":1,\"ok\":true,\"result\":{\"device\":\"neomind-v1\",\"mcu\":\"ATmega328P\"}}");
    return;
  }

  if (input.indexOf("\"cmd\":\"set_led\"") >= 0) {
    const bool on = input.indexOf("\"value\":1") >= 0 ||
                   input.indexOf("\"value\":true") >= 0;
    digitalWrite(LED_PIN, on ? HIGH : LOW);
    respond(on
      ? "{\"id\":1,\"ok\":true,\"result\":{\"led\":1}}"
      : "{\"id\":1,\"ok\":true,\"result\":{\"led\":0}}");
    return;
  }

  respond("{\"id\":0,\"ok\":false,\"error\":\"unsupported_command\"}");
}
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(BAUD);
}

void loop() {
  while (Serial.available()) {
    const char c = static_cast<char>(Serial.read());

    if (c == '\n') {
      line.trim();
      if (line.length() > 0) {
        handleCommand(line);
      }
      line = "";
    } else if (c != '\r' && line.length() < 180) {
      line += c;
    } else if (line.length() >= 180) {
      line = "";
      respond("{\"id\":0,\"ok\":false,\"error\":\"request_too_large\"}");
    }
  }
}
