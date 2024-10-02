//HC-06
#include <SoftwareSerial.h> //시리얼 통신 핀을 지정하는 헤더, 소프트웨어로 조작하여, 한 묶음 밖에 없는 시리얼 통신 핀을 늘림. | 기존은 0, 1핀 밖에 없음 -> 컴퓨터랑 통신할 때, 사용

SoftwareSerial BTSerial(2, 3);   //bluetooth module Tx:Digital 2 Rx:Digital 3 | 시리얼 통신을 블루투스로 할 것이므로 시리얼 핀 지정
//우노 사용을 추천, 레오나르도 보드는 통신에 실패함. 다른 보드들은 2, 3번 핀 사용이 불가할 수 있음
/*******************************************/

//Max30102
#include <Wire.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"

MAX30105 particleSensor;

#define MAX_BRIGHTNESS 255

uint16_t irBuffer[100]; //infrared LED sensor data
uint16_t redBuffer[100];  //red LED sensor data

int32_t bufferLength; //data length
int32_t spo2; //SPO2 value
int8_t validSPO2; //indicator to show if the SPO2 calculation is valid
int32_t heartRate; //heart rate value
int8_t validHeartRate; //indicator to show if the heart rate calculation is valid

byte pulseLED = 11; //Must be on PWM pin
byte readLED = 13; //Blinks with each data read

/*******************************************/
//setup
void setup() {
  Serial.begin(115200);
  BTSerial.begin(115200); //블루투스 시리얼 통신 | 무선 연결 컴퓨터[파이썬 내장] - 아두이노

  //Max30102
  pinMode(pulseLED, OUTPUT);
  pinMode(readLED, OUTPUT);

  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println(F("MAX30105 was not found. Please check wiring/power."));
    while (1);
  }
  byte ledBrightness = 60; //Options: 0=Off to 255=50mA
  byte sampleAverage = 4; //Options: 1, 2, 4, 8, 16, 32
  byte ledMode = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  byte sampleRate = 100; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411; //Options: 69, 118, 215, 411
  int adcRange = 4096; //Options: 2048, 4096, 8192, 16384

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);
}

/*******************************************/
//loop()
void loop() {
  //Max30102
  bufferLength = 100; //buffer length of 100 stores 4 seconds of samples running at 25sps

  //read the first 100 samples, and determine the signal range
  for (byte i = 0 ; i < bufferLength ; i++)
  {
    while (particleSensor.available() == false) //do we have new data?
      particleSensor.check(); //Check the sensor for new data

    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample(); //We're finished with this sample so move to next sample

    while (1)
    {
      //dumping the first 25 sets of samples in the memory and shift the last 75 sets of samples to the top
      for (byte i = 25; i < 100; i++)
      {
        redBuffer[i - 25] = redBuffer[i];
        irBuffer[i - 25] = irBuffer[i];
      }

      //take 25 sets of samples before calculating the heart rate.
      for (byte i = 75; i < 100; i++)
      {
        while (particleSensor.available() == false) //do we have new data?
          particleSensor.check(); //Check the sensor for new data

        digitalWrite(readLED, !digitalRead(readLED)); //Blink onboard LED with every data read

        redBuffer[i] = particleSensor.getRed();
        irBuffer[i] = particleSensor.getIR();
        particleSensor.nextSample(); //We're finished with this sample so move to next sample

        //Send_2
        Serial.print(",");
        Serial.print(heartRate, DEC);
        BTSerial.print(",");
        BTSerial.print(heartRate, DEC);
        
        Serial.print(",");
        Serial.print(spo2, DEC);
        BTSerial.print(",");
        BTSerial.print(spo2, DEC);
      }

      //After gathering 25 new samples recalculate HR and SP02
      maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
    }

  }
  delay(1000); // 과도한 정보 송출을 막기 위해, 0.5초의 지연을 삽입
}
