//DHT22
#include "DHT.h"

#define DHTPIN 4

#define DHTTYPE DHT22

float h = 0;
float t = 0;
int count = 100;

DHT dht(DHTPIN, DHTTYPE);
//Max30102
#include <Wire.h>
#include "MAX30105.h"

#include "heartRate.h"

MAX30105 particleSensor;

const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred

long mil_start = 0;
long mil_end = 0;
long mil_gap = 0;

float beatsPerMinute;
int beatAvg;

void setup()
{
  Serial.begin(115200);
  Serial.println("Initializing...");

  dht.begin();

  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  Serial.println("Place your index finger on the sensor with steady pressure.");

  particleSensor.setup(); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED
}

void loop()
{
  if (count >= 100){
    mil_start = millis();
    h = dht.readHumidity();
    t = dht.readTemperature();
    count = 0;
    mil_end = millis();
    mil_gap = mil_end - mil_start;
  }
  
    long irValue = particleSensor.getIR();

    if (checkForBeat(irValue) == true)
    {
      //We sensed a beat!
      long delta = millis() - lastBeat - mil_gap;
      lastBeat = millis();

      beatsPerMinute = 60 / (delta / 1000.0);

      if (beatsPerMinute < 255 && beatsPerMinute > 20)
      {
        rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
        rateSpot %= RATE_SIZE; //Wrap variable

        //Take average of readings
        beatAvg = 0;
        for (byte x = 0 ; x < RATE_SIZE ; x++)
          beatAvg += rates[x];
        beatAvg /= RATE_SIZE;
      }
    }

    Serial.print("IR=");
    Serial.print(irValue);
    Serial.print(", BPM=");
    Serial.print(beatsPerMinute);
    Serial.print(", Avg BPM=");
    Serial.print(beatAvg);
    Serial.print(" Humidity: ");
    Serial.print(h);
    Serial.print(" ");
    Serial.print("Temperature: "); 
    Serial.print(t);
    Serial.print(" *C");
    if (irValue < 50000)
      Serial.print(" No finger?");

    Serial.println();
    count++;

}


