#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <Wire.h>
#include <BH1750.h>

// LCD and sensors
LiquidCrystal_I2C lcd(0x27, 20, 4);
#define DHTPIN 6
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
#define FAN 5
BH1750 lightMeter;
#define PH_PIN A0
#define SOIL_PIN A1

void setup() {
  Serial.begin(9600);
  dht.begin();
  Wire.begin();
  lightMeter.begin();
  pinMode(FAN, OUTPUT);
  digitalWrite(FAN, HIGH);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0); lcd.print("  Welcome  ");
  delay(2000);
  lcd.clear();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  float lux = lightMeter.readLightLevel();
  int soilVal = analogRead(SOIL_PIN);
  int phRaw = analogRead(PH_PIN);
  float phValue = map(phRaw, 0, 1023, 0, 14);

  // Fan control
  digitalWrite(FAN, temperature > 28 ? LOW : HIGH);

  // Display
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print("Temp:"); lcd.print(temperature); lcd.print("C");
  lcd.setCursor(0, 1); lcd.print("Humidity:"); lcd.print((int)humidity); lcd.print("%");
  lcd.setCursor(0, 2); lcd.print("PH:"); lcd.print(phValue);
  lcd.setCursor(0, 3); lcd.print("Soil:"); lcd.print(soilVal); lcd.print(" Lux:"); lcd.print(lux);

  // Send via Serial
  Serial.print(temperature); Serial.print(",");
  Serial.print(humidity); Serial.print(",");
  Serial.print(phValue); Serial.print(",");
  Serial.print(soilVal); Serial.print(",");
  Serial.println(lux);

  delay(3000);
}
