
#include <string.h>
#include <Servo.h>

Servo servoX; // create servo object to control a servo
Servo servoY;

int Xpos;
int Ypos;          // variable to store the servo position
String incoming;  
String data = "";    // a variable to read incoming serial data into



void setup()
{
    // initialize serial communication:
    Serial.begin(9600);
    servoX.attach(9);
    servoY.attach(10);
    Serial.setTimeout(5);
}


int parseX(String incoming) {
    incoming.remove(incoming.indexOf(","));
    incoming.remove(incoming.indexOf("X"), 1);
    return incoming.toInt();
}

int parseY(String incoming) {
    incoming.remove(0, incoming.indexOf(",") + 1);
    incoming.remove(incoming.indexOf("Y"), 1);
    return incoming.toInt();
}

void loop()
{
    /*

     //see if there's incoming serial data:
    if (Serial.available() > 0)
    {
        incoming = Serial.readString();
        
        int n = incoming.toInt();
        Serial.println("incoming:: " + incoming);
        
        if (n < 180) {
            servoX.write(n);
        } 
        

        
        //incoming += c;
        String test = "100";

        //Xpos = parseX(incoming);
        //Ypos = parseY(incoming);

        
        
        //servoY.write(Ypos);
        //Serial.println(incoming.toInt());
        //Serial.println(Ypos);
        //Serial.println(incoming);
        incoming = "";
    }
    */
    
}


void serialEvent() {
    incoming = Serial.readString();
    
    data += incoming;

    servoX.write(parseX(incoming));
    servoY.write(parseY(incoming));

    //servoY.write(Ypos);
    //Serial.println(incoming);
}

/* Processing code for this example

  // Mouse over serial

  // Demonstrates how to send data to the Arduino I/O board, in order to turn ON
  // a light if the mouse is over a square and turn it off if the mouse is not.

  // created 2003-4
  // based on examples by Casey Reas and Hernando Barragan
  // modified 30 Aug 2011
  // by Tom Igoe
  // This example code is in the public domain.

  import processing.serial.*;

  float boxX;
  float boxY;
  int boxSize = 20;
  boolean mouseOverBox = false;

  Serial port;

  void setup() {
    size(200, 200);
    boxX = width / 2.0;
    boxY = height / 2.0;
    rectMode(RADIUS);

    // List all the available serial ports in the output pane.
    // You will need to choose the port that the Arduino board is connected to
    // from this list. The first port in the list is port #0 and the third port
    // in the list is port #2.
    // if using Processing 2.1 or later, use Serial.printArray()
    println(Serial.list());

    // Open the port that the Arduino board is connected to (in this case #0)
    // Make sure to open the port at the same speed Arduino is using (9600bps)
    port = new Serial(this, Serial.list()[0], 9600);
  }

  void draw() {
    background(0);

    // Test if the cursor is over the box
    if (mouseX > boxX - boxSize && mouseX < boxX + boxSize &&
        mouseY > boxY - boxSize && mouseY < boxY + boxSize) {
      mouseOverBox = true;
      // draw a line around the box and change its color:
      stroke(255);
      fill(153);
      // send an 'H' to indicate mouse is over square:
      port.write('H');
    }
    else {
      // return the box to its inactive state:
      stroke(153);
      fill(153);
      // send an 'L' to turn the LED off:
      port.write('L');
      mouseOverBox = false;
    }

    // Draw the box
    rect(boxX, boxY, boxSize, boxSize);
  }

*/

