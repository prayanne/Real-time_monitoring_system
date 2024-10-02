//DHT22
#include "DHT.h" //DHT22 헤더 호출

#define DHTPIN 4 //DHT22 정보 수신 핀 지정

#define DHTTYPE DHT22 //DHT 센서들 중, DHT22를 사용

DHT dht(DHTPIN, DHTTYPE); //DHT센서 선언, DHT핀은 4번, DHT타입은 DHT22

String humidity; //DHT센서, 습도를 문자열로 저장하는 변수
String temperture; //DHT센서, 온도를 문자열로 저장하는 변수

//HC-06
#include <SoftwareSerial.h> //시리얼 통신 핀을 지정하는 헤더, 소프트웨어로 조작하여, 한 묶음 밖에 없는 시리얼 통신 핀을 늘림. | 기존은 0, 1핀 밖에 없음 -> 컴퓨터랑 통신할 때, 사용

SoftwareSerial BTSerial(2, 3);   //bluetooth module Tx:Digital 2 Rx:Digital 3 | 시리얼 통신을 블루투스로 할 것이므로 시리얼 핀 지정
//우노 사용을 추천, 레오나르도 보드는 통신에 실패함. 다른 보드들은 2, 3번 핀 사용이 불가할 수 있음

/*******************************************/
//setup
void setup() {
  Serial.begin(9600); //시리얼 통신 | 유선 연결 컴퓨터 - 아두이노
  BTSerial.begin(9600); //블루투스 시리얼 통신 | 무선 연결 컴퓨터[파이썬 내장] - 아두이노 
  dht.begin(); //DHT22센서 시작
}

/*******************************************/
//loop()
void loop() {
  float h = dht.readHumidity(); //변수 f에 습도 값을 저장 | DHT.h에 있는 함수입니다.
  float t = dht.readTemperature(); //변수 t에 온도 값을 저장 | DHT.h에 있는 함수입니다.
  
  if (isnan(t) || isnan(h)) { //t와 h의 값들 중, 하나라도 수가 아니라면, 블루투스 시리얼 통신으로 0만을 송신함. | 파이썬에서 오류임을 표기하기 위해서이다.
    BTSerial.println("1"); //오류임을 알리는 1[문자열]
  } else {
  humidity = String(h); // 습도값을 문자열로 전환 | float -> string
  temperture = String(t); // 온도값을 문자열로 전환 | float -> string


  //값들 앞에는 오류 없이 수신되고 있음을 표시하는 값, [ 0, 1 ]이 존재함. 이는 다른 값들과 콤마(,)로 구분됨.
  //not_default와 다르게, 여기는 "습도값[문자열], 온도값[문자열]"로 송출됨. | 이유는 파이썬에서, 콤마(,)를 기준으로 값을 나눌 것이기 때문.
  BTSerial.print("0,");
  BTSerial.print(humidity + ","); // 습도값 송신 | 블루투스 사용 | BTSerial은 블루투스끼리 시리얼 통신을 함. | .print("내용")은 "내용"을 상대 시리얼 모듈로 송신하는 것
  BTSerial.println(temperture); // 온도값 송신 | 블루투스 사용 | BTSerial은 블루투스끼리 시리얼 통신을 함. | .print("내용")은 "내용"을 상대 시리얼 모듈로 송신하는 것
  }
  delay(1000); // 과도한 정보 송출을 막기 위해, 0.5초의 지연을 삽입
}
