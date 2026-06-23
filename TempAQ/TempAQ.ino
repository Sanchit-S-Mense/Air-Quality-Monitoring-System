#include "MQ135.h"  // The math library for the sensor
#include "DHT.h"

#define DHTPIN 2      // Pin where the sensor is connected
#define DHTTYPE DHT11 // Sensor type

DHT dht(DHTPIN, DHTTYPE);

const int SENSOR_PIN = 0; 
MQ135 gasSensor = MQ135(SENSOR_PIN); 

void setup() {
  Serial.begin(9600); // Initialize the serial monitor
  delay(60000);// Time for sensor to warm
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();           // Read humidity
  float temperatureC = dht.readTemperature();   // Temperature in Celsius

  if (isnan(humidity) || isnan(temperatureC)) {
    Serial.println("Error reading data!");
    return;
  }

  // Output data to the serial monitor
  Serial.print(temperatureC);
  Serial.print(" , ");
  Serial.print(humidity);
  Serial.print(" , ");
  float ppmValue = gasSensor.getPPM(); 
  Serial.print(ppmValue);
  Serial.print("  ");
  delay(30000); //wait for 30s before looping back
}
