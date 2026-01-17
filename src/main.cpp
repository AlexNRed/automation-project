#include <Arduino.h>
#include <DHT.h>
#include <LiquidCrystal.h>

#define DHTPin 2
#define DHTType DHT11

#define redPin 10
#define greenPin 9
#define bluePin 8

// LCD Pins (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(12, 11, 6, 5, 4, 3);
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
  
  // initialize the LCD
  lcd.begin(16, 2); // Initialize a 16x2 LCD
  lcd.clear();
  // displays the startup message
  lcd.setCursor(0, 0);
  lcd.print("Temp & Humidity Monitor");
  lcd.setCursor(0,1); 
  lcd.print("Starting..");

  delay(2000);
  Serial.println("DHT11 Sensor Started");
}

void loop() {
  float temperature = dhtSensor.readTemperature(true);
  float humidity = dhtSensor.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("ERROR: Failed to read sensor");

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error");

    delay(2000);
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °F, Humidity: ");
  Serial.print(humidity);
  Serial.println("%");

  lcd.clear();

  // Line 1: Temperature
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperature, 1);  // Show 1 decimal place
  lcd.print((char)223);       // Degree symbol
  lcd.print("F");
  
  // Line 2: Humidity
  lcd.setCursor(0, 1);
  lcd.print("Humidity: ");
  lcd.print(humidity, 0);     // Show 0 decimal places
  lcd.print("%");

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

