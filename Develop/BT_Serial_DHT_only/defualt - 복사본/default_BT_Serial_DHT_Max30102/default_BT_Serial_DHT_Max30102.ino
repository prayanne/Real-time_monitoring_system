//DHT22
#include "DHT.h" //DHT22 헤더 호출

#define DHTPIN 4 //DHT22 정보 수신 핀 지정

#define DHTTYPE DHT22 //DHT 센서들 중, DHT22를 사용

DHT dht(DHTPIN, DHTTYPE); //DHT센서 선언, DHT핀은 4번, DHT타입은 DHT22

String humidity; //DHT센서, 습도를 문자열로 저장하는 변수
String temperture; //DHT센서, 온도를 문자열로 저장하는 변수
/*******************************************/

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
  dht.begin(); //DHT22센서 시작

  //Max30102
  pinMode(pulseLED, OUTPUT);
  pinMode(readLED, OUTPUT);

  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println(F("MAX30105 was not found. Please check wiring/power."));
    while (1);
  }

  Serial.println(F("Attach sensor to finger with rubber band. Press any key to start conversion"));
  while (Serial.available() == 0) ; //wait until user presses a key
  Serial.read();

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
  //DHT22
  float h = dht.readHumidity(); //변수 f에 습도 값을 저장 | DHT.h에 있는 함수입니다.
  float t = dht.readTemperature(); //변수 t에 온도 값을 저장 | DHT.h에 있는 함수입니다.

  humidity = String(h); // 습도값을 문자열로 전환 | float -> string
  temperture = String(t); // 온도값을 문자열로 전환 | float -> string

    //Send_1
    //값들 앞에는 오류 없이 수신되고 있음을 표시하는 값, [ 0, 1 ]이 존재함. 이는 다른 값들과 콤마(,)로 구분됨.
    //not_default와 다르게, 여기는 "습도값[문자열], 온도값[문자열]"로 송출됨. | 이유는 파이썬에서, 콤마(,)를 기준으로 값을 나눌 것이기 때문.
    BTSerial.print("0,");
    BTSerial.print(humidity + ","); // 습도값 송신 | 블루투스 사용 | BTSerial은 블루투스끼리 시리얼 통신을 함. | .print("내용")은 "내용"을 상대 시리얼 모듈로 송신하는 것
    BTSerial.println(temperture); // 온도값 송신 | 블루투스 사용 | BTSerial은 블루투스끼리 시리얼 통신을 함. | .print("내용")은 "내용"을 상대 시리얼 모듈로 송신하는 것
    
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
