#include <Arduino.h>

namespace {
constexpr unsigned long BAUD = 115200;
constexpr uint8_t LED_PIN = LED_BUILTIN;
constexpr size_t MAX_LINE = 180;
String line;

String extractId(const String& input) {
  const int key = input.indexOf("\"id\"");
  if (key < 0) return "null";
  const int colon = input.indexOf(':', key);
  if (colon < 0) return "null";
  int end = input.indexOf(',', colon + 1);
  if (end < 0) end = input.indexOf('}', colon + 1);
  if (end < 0) return "null";
  String id = input.substring(colon + 1, end);
  id.trim();
  return id;
}

void respond(const String& id, const String& result) {
  Serial.print("{\"id\":");
  Serial.print(id);
  Serial.print(",\"ok\":true,\"result\":");
  Serial.print(result);
  Serial.println('}');
}

void errorResponse(const String& id, const char* error) {
  Serial.print("{\"id\":");
  Serial.print(id);
  Serial.print(",\"ok\":false,\"error\":\"");
  Serial.print(error);
  Serial.println("\"}");
}

void handleCommand(const String& input) {
  const String id = extractId(input);

  if (input.indexOf("\"cmd\":\"ping\"") >= 0) {
    respond(id, "{\"pong\":true}");
    return;
  }

  if (input.indexOf("\"cmd\":\"status\"") >= 0) {
    respond(id, "{\"device\":\"neomind-v1\",\"mcu\":\"ATmega328P\"}");
    return;
  }

  if (input.indexOf("\"cmd\":\"set_led\"") >= 0) {
    const bool on = input.indexOf("\"value\":1") >= 0 ||
                    input.indexOf("\"value\":true") >= 0;
    digitalWrite(LED_PIN, on ? HIGH : LOW);
    respond(id, on ? "{\"led\":1}" : "{\"led\":0}");
    return;
  }

  errorResponse(id, "unsupported_command");
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
      if (line.length() > 0) handleCommand(line);
      line = "";
    } else if (c != '\r') {
      if (line.length() < MAX_LINE) {
        line += c;
      } else {
        line = "";
        errorResponse("null", "request_too_large");
      }
    }
  }
}
