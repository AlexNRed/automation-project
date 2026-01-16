#include <Arduino.h>
#include <DHT.h>

#define DHTPin 2
#define DHTType DHT11

#define redPin 10
#define greenPin 9
#define bluePin 8

DHT dhtSensor(DHTPin, DHTType);

void setup() {
  Serial.begin(9600);
  dhtSensor.begin();

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  digitalWrite(redPin, LOW);
  digitalWrite(greenPin, LOW);
  digitalWrite(bluePin, LOW);

  delay(1000);
  Serial.println("DHT11 Sensor Started");
}

void loop() {
  float temperature = dhtSensor.readTemperature(true);
  float humidity = dhtSensor.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("ERROR: Failed to read sensor");
    delay(2000);
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °F, Humidity: ");
  Serial.print(humidity);
  Serial.println("%");

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove any whitespace
    
    // Turn off all LEDs first
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin, LOW);
    digitalWrite(bluePin, LOW);
    
    // Turn on the appropriate LED based on command
    if (command == "LED_RED") {
      digitalWrite(redPin, HIGH);
      Serial.println("Red LED ON");
    }
    else if (command == "LED_GREEN") {
      digitalWrite(greenPin, HIGH);
      Serial.println("Green LED ON");
    }
    else if (command == "LED_BLUE") {
      digitalWrite(bluePin, HIGH);
      Serial.println("Blue LED ON");
    }
    else {
      Serial.println("Unknown command: " + command);
    }
  }
  
  delay(2000);
  
}

