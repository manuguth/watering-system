//Wet: (430 350]
//Water: (350 260]
#include <SPI.h>  // include libraries
#include <Wire.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>


////////////////////// Moisture Sensors //////////////////////
const int AirValue = 420;
const int WaterValue = 195;
int soilMoistureValue_1 = 0;
int soilMoistureValue_2 = 0;
int soilMoistureValue_3 = 0;
int soilMoistureValue_4 = 0;
int soilMoistureValue_5 = 0;
int soilMoistureValue_6 = 0;
int soilmoisturepercent_1 = 0;
int soilmoisturepercent_2 = 0;
int soilmoisturepercent_3 = 0;
int soilmoisturepercent_4 = 0;
int soilmoisturepercent_5 = 0;
int soilmoisturepercent_6 = 0;
int counter = 0;

int moisturesensor_1 = A0;  // moisture sensor is connected with the analog pin A0 of the Arduino
int moisturesensor_2 = A1;  // 2nd moisture sensor is connected with the analog pin A1 of the Arduino
int moisturesensor_3 = A2;  // 3rd moisture sensor is connected with the analog pin A2 of the Arduino
int moisturesensor_4 = A3;  // 4th moisture sensor is connected with the analog pin A3 of the Arduino
int moisturesensor_5 = A4;  // 5th moisture sensor is connected with the analog pin A4 of the Arduino
int moisturesensor_6 = A5;  // 6th moisture sensor is connected with the analog pin A5 of the Arduino
////////////////////// Temperature & air humidity //////////////////////
#define DHTPIN 2       // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22  // DHT 22 (AM2302)

DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t delayMS;

// ultrasonic sensor JSN-SR04M
// Pin definition
const uint8_t echoPin = 12;  //D6
const uint8_t trigPin = 13;  //D7

// Variables
float duration, distance;


void setup() {
  ////////////////////// General Setup //////////////////////
  Serial.begin(9600);
  ////////////////////// Moisture Sensors //////////////////////
  pinMode(moisturesensor_1, INPUT);
  pinMode(moisturesensor_2, INPUT);
  pinMode(moisturesensor_3, INPUT);
  pinMode(moisturesensor_4, INPUT);
  pinMode(moisturesensor_5, INPUT);
  pinMode(moisturesensor_6, INPUT);
  ////////////////////// Temperature & air humidity //////////////////////
  // Initialize device.
  dht.begin();
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  // Set delay between sensor readings based on sensor details.
  // commented to use one global delay
  delayMS = sensor.min_delay / 100;
  ////////////////////// ultrasonic sensor //////////////////////
  // Define pin modes
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
}
void loop() {

  ////////////////////// Moisture Sensors //////////////////////
  soilMoistureValue_1 = analogRead(moisturesensor_1);
  soilMoistureValue_2 = analogRead(moisturesensor_2);
  soilMoistureValue_3 = analogRead(moisturesensor_3);
  soilMoistureValue_4 = analogRead(moisturesensor_4);
  soilMoistureValue_5 = analogRead(moisturesensor_5);
  soilMoistureValue_6 = analogRead(moisturesensor_6);
  // Serial.println(soilMoistureValue);
  soilmoisturepercent_1 = map(soilMoistureValue_1, AirValue, WaterValue, 0, 100);
  soilmoisturepercent_2 = map(soilMoistureValue_2, AirValue, WaterValue, 0, 100);
  soilmoisturepercent_3 = map(soilMoistureValue_3, AirValue, WaterValue, 0, 100);
  soilmoisturepercent_4 = map(soilMoistureValue_4, AirValue, WaterValue, 0, 100);
  soilmoisturepercent_5 = map(soilMoistureValue_5, AirValue, WaterValue, 0, 100);
  soilmoisturepercent_6 = map(soilMoistureValue_6, AirValue, WaterValue, 0, 100);

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
  // Check if temperature is NAN and set tempStr to "null" if true
  if (isnan(temperature)) {
    strcpy(tempStr, "null");
  } else {
    dtostrf(temperature, 4, 2, tempStr);
  }

  // Check if humidity is NAN and set humStr to "null" if true
  if (isnan(humidity)) {
    strcpy(humStr, "null");
  } else {
    dtostrf(humidity, 4, 2, humStr);
  }

  ////////////////////// ultrasonic sensor //////////////////////

  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);

  // Set the trigger pin HIGH for 20us
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(20);
  digitalWrite(trigPin, LOW);

  // Measure the time of the incoming pulse
  duration = pulseIn(echoPin, HIGH);

  //Calculate the distance
  distance = duration / 58;

  char diststr[10];
  dtostrf(distance, 4, 2, diststr);

  // serial output in form of
  // {sensor_1:soilmoisturepercent_1,sensor_2:soilmoisturepercent_2}
  // Buffer to hold the formatted string
  char rasp_output[512];

  // Format the string
  // sprintf(rasp_output, "{'measurement':{'sensor_1':%d, 'sensor_raw_1':%d}, 'counter':%i}",
  //         soilmoisturepercent_1,
  //         soilMoistureValue,
  //         soilmoisturepercent_2,
  //         soilmoisturepercent_3,
  //         tempStr,
  //         humStr,
  //         counter);
  sprintf(rasp_output, ("{'measurement':{'sensor_1':%d, 'sensor_raw_1':%d, 'sensor_2':%d, 'sensor_raw_2':%d,"
                        "'sensor_3':%d, 'sensor_raw_3':%d, 'sensor_4':%d, 'sensor_raw_4':%d,"
                        "'sensor_5':%d, 'sensor_raw_5':%d, 'sensor_6':%d, 'sensor_raw_6':%d,"
                        "'temperature':%s, 'humidity':%s, 'waterlevel': %s}, 'counter':%i}"),
          soilmoisturepercent_1,
          soilMoistureValue_1,
          soilmoisturepercent_2,
          soilMoistureValue_2,
          soilmoisturepercent_3,
          soilMoistureValue_3,
          soilmoisturepercent_4,
          soilMoistureValue_4,
          soilmoisturepercent_5,
          soilMoistureValue_5,
          soilmoisturepercent_6,
          soilMoistureValue_6,
          tempStr,
          humStr,
          diststr,
          counter);
  Serial.println(rasp_output);


  counter++;
  delay(1000);
}