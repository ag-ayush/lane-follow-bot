#include <Servo.h>

const byte numLEDs = 2;
byte ledPin[numLEDs] = {9, 10};  // White - LEFT - 9 & Green - RIGHT - 10

const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

char messageFromPC[buffSize] = {0};
float movement = 0;

unsigned long curMillis;

//=============

void setup() {
  Serial.begin(9600);

  // flash LEDs so we know we are alive
  for (byte n = 0; n < numLEDs; n++) {
    // Configures the specified pin to behave either as an input or an output.
    pinMode(ledPin[n], OUTPUT);
    //If the pin has been configured as an OUTPUT with pinMode(), its voltage will be set to the corresponding value: 5V for HIGH, 0V for LOW.
    digitalWrite(ledPin[n], HIGH);
  }
  delay(500); // delay() is OK in setup as it only happens once

  for (byte n = 0; n < numLEDs; n++) {
    digitalWrite(ledPin[n], LOW);
  }

  // tell the PC we are ready
  Serial.println("<Arduino is ready>");
}

//=============

void loop() {
  curMillis = millis(); //// Returns the number of milliseconds since the Arduino board began running the current program.
  getDataFromPC();
  updateFlashInterval();
  replyToPC();
}

//=============

void getDataFromPC() {
  /*
     Receive data from PC and save it into inputBuffer

     Serial.available()
        Get the number of bytes (characters) available for reading from the serial port.
        This is data that's already arrived and stored in the serial receive buffer (which holds 64 bytes).
  */
  if (Serial.available() > 0) {

    char x = Serial.read();

    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }

    if (readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) {
      bytesRecvd = 0;
      readInProgress = true;
    }
  }
}

//=============

void parseData() {

  // split the data into its parts

  char * strtokIndx;                        // this is used by strtok() as an index

  strtokIndx = strtok(inputBuffer, ",");    // get the first part - the string
  strcpy(messageFromPC, strtokIndx);        // copy it to messageFromPC

  strtokIndx = strtok(NULL, ",");
  movement = atof(strtokIndx);         // convert this part to a float

}

//=============

void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<Msg ");
    Serial.print(messageFromPC);
    Serial.print(" Movement ");
    Serial.print(movement);
    Serial.print(" Time ");
    Serial.print(curMillis >> 9); // divide by 512 is approx = half-seconds
    Serial.println(">");
  }
}

//============

void updateFlashInterval() {
  // this illustrates using different inputs to call different functions
  if (strcmp(messageFromPC, "LEFT") == 0) {
    analogWrite(ledPin[0], 255 * movement);
    delay(10);
    analogWrite(ledPin[0], 0);
  }

  if (strcmp(messageFromPC, "RIGHT") == 0) {
    analogWrite(ledPin[1], 255 * movement);
    delay(10);
    analogWrite(ledPin[1], 0);
  }

  if (strcmp(messageFromPC, "STRAIGHT") == 0) {
    analogWrite(ledPin[0], 0);
    analogWrite(ledPin[1], 0);
  }
}

