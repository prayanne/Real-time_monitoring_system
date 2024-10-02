#include <SoftwareSerial.h>

SoftwareSerial bluetooth(7,8);

void setup() {


  Serial.begin(9600);
  bluetooth.begin(9600);


  Serial.println("HELLO!");
  pinMode(3, OUTPUT);
  analogWrite(3,0);
}


void loop() {

  if (bluetooth.available()) {
    
    String str_led = bluetooth.readString();
    
    Serial.print(str_led);
    
    if(str_led == "on") {
      analogWrite(3, 180);
      Serial.println("on");
    }
    if(str_led == "off") {
      analogWrite(3, 0);
      Serial.println("off");
    }
  
  }

  if (Serial.available()) {

    bluetooth.write(Serial.read());
  }

}
