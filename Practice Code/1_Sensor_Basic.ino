// 목적: 시리얼 통신을 이해하고 있는지 확인하는 코드
// 수행할 항목 : - 처리되어 있는 줄의 코드를 작성
// - 처리되어 있는 항목은 3개 입니다.

// 전제 조건: 
// DHT22 센서를 사용, digital pin 4번 사용
// 컴퓨터 to 아두이노, 유선 연결


/*******************************************/
//DHT22 설정
#include "DHT.h" //DHT22 헤더 호출

#define DHTPIN 4 //DHT22 정보 수신 핀 지정
#define DHTTYPE DHT22 //DHT 센서들 중, DHT22를 사용
DHT dht(DHTPIN, DHTTYPE); //DHT센서 선언, DHT핀은 4번, DHT타입은 DHT22

String humidity; //DHT센서, 습도를 문자열로 저장하는 변수
String temperture; //DHT센서, 온도를 문자열로 저장하는 변수

/*******************************************/
//setup
void setup() {
  - //시리얼 통신 시작, 9600 비트레이트로 설정 | 유선 연결, 컴퓨터 to 아두이노
  dht.begin(); //DHT22센서 시작
}

/*******************************************/
//loop()
void loop() {
  float h = dht.readHumidity();  //변수 f에 습도 값을 저장 | DHT.h에 있는 함수입니다.
  float t = dht.readTemperature(); //변수 t에 온도 값을 저장 | DHT.h에 있는 함수입니다.
  
  humidity = String(h); // 습도값을 문자열로 전환 | float -> string
  temperture = String(t); // 온도값을 문자열로 전환 | float -> string

  //"습도값[문자열], 온도값[문자열]"로 송출됨. | 이유는 파이썬에서, 콤마(,)를 기준으로 값을 나눌 것이기 때문.

  - // 시리얼 통신 | 습도값 송신 | ?.print("내용")은 "내용"을 상대 시리얼 모듈로 송신하는 것
  - // 시리얼 통신 | 온도값 송신 | ?.println("내용")은 "내용"을 상대 시리얼 모듈로 송신하는 것

}