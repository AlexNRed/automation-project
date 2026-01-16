#include <Arduino.h>
#include <DHT.h>

#define DHTPin 2
#define DHTType DHT11

DHT dhtSensor(DHTPin, DHTType);

void setup() {
  Serial.begin(9600);
  dhtSensor.begin();

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
  
}

