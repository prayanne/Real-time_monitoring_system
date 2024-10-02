#include <SoftwareSerial.h>

SoftwareSerial bluetooth(7,8);

void setup() {


  Serial.begin(9600);
  bluetooth.begin(9600);


  Serial.println("HELLO!");

}


void loop() {


  if (bluetooth.available()) {

    Serial.write(bluetooth.read());

  }

  if (Serial.available()) {

    bluetooth.write(Serial.read());
  }

}
