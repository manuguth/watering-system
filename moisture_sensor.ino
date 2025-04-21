//Wet: (430 350]
//Water: (350 260]
#include <SPI.h>  // include libraries
#include <Wire.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>


////////////////////// Moisture Sensors //////////////////////
const int AirValue = 560;
const int WaterValue = 215;
int soilMoistureValue = 0;
int soilMoistureValue_2 = 0;
int soilMoistureValue_3 = 0;
int soilmoisturepercent_1 = 0;
int soilmoisturepercent_2 = 0;
int soilmoisturepercent_3 = 0;
int counter = 0;

int moisturesensor = A0;    // moisture sensor is connected with the analog pin A0 of the Arduino
int moisturesensor_2 = A1;  // 2nd moisture sensor is connected with the analog pin A1 of the Arduino
int moisturesensor_3 = A2;  // 3rd moisture sensor is connected with the analog pin A2 of the Arduino
////////////////////// Temperature & air humidity //////////////////////
#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE    DHT22     // DHT 22 (AM2302)

DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t delayMS;


void setup() {
  ////////////////////// General Setup //////////////////////
  Serial.begin(9600);
  ////////////////////// Moisture Sensors //////////////////////
  pinMode(moisturesensor, INPUT);
  pinMode(moisturesensor_2, INPUT);
  pinMode(moisturesensor_3, INPUT);
  ////////////////////// Temperature & air humidity //////////////////////
  // Initialize device.
  dht.begin();
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  // Set delay between sensor readings based on sensor details.
  // commented to use one global delay
  // delayMS = sensor.min_delay / 100;
}
void loop() {

////////////////////// Moisture Sensors //////////////////////
  soilMoistureValue = analogRead(moisturesensor);
  soilMoistureValue_2 = analogRead(moisturesensor_2);
  soilMoistureValue_3 = analogRead(moisturesensor_3);
  // Serial.println(soilMoistureValue);
  soilmoisturepercent_1 = map(soilMoistureValue, AirValue, WaterValue, 0, 100);
  soilmoisturepercent_2 = map(soilMoistureValue_2, AirValue, WaterValue, 0, 100);
  soilmoisturepercent_3 = map(soilMoistureValue_3, AirValue, WaterValue, 0, 100);

////////////////////// Temperature & air humidity //////////////////////
  // delay(delayMS);
  // Get temperature event and print its value.
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  float temperature = event.temperature;
  dht.humidity().getEvent(&event);
  float humidity = event.relative_humidity;

  char tempStr[10];
  char humStr[10];

  // Convert floating-point numbers to strings
  dtostrf(temperature, 4, 2, tempStr);
  dtostrf(humidity, 4, 2, humStr);

  // serial output in form of
  // {sensor_1:soilmoisturepercent_1,sensor_2:soilmoisturepercent_2}
  // Buffer to hold the formatted string
  char rasp_output[512];

  // Format the string
  sprintf(rasp_output, "{'measurement':{'sensor_1':%d,'sensor_2':%d,'sensor_3':%d, 'temperature':%s, 'humidity':%s}, 'counter':%i}",
          soilmoisturepercent_1,
          soilmoisturepercent_2,
          soilmoisturepercent_3,
          tempStr,
          humStr,
          counter);
  Serial.println(rasp_output);


  counter++;
  delay(1000);
}