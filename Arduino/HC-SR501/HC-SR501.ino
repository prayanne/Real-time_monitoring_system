/** 인체 감지 센서 실험 **/
int Led = 8;
int SensorOut = 7;
int val;

void setup() {
  pinMode(Led, OUTPUT);
  pinMode(SensorOut, INPUT);
  Serial.begin(9600);
  
}
void loop() {
  val = digitalRead(SensorOut);  // 적외선 센서값 읽어 저장
  if (val == HIGH)  {
    digitalWrite(Led, HIGH);
    Serial.println("Hi");
  }  
  else  {
    digitalWrite(Led, LOW);
    Serial.println("bye");
  }
  delay(100);  
}
