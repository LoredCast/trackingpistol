#include <string.h>
#include <Stepper.h>
#include <Servo.h>

const int stepsPerRevolution = 200;

Servo servoYL;
Servo servoYR;

String incoming;
//String data = "";

Stepper StepperX = Stepper(stepsPerRevolution, 2, 3, 4, 5);

int parseX(String incoming)
{
    incoming.remove(incoming.indexOf(","));
    incoming.remove(incoming.indexOf("X"), 1);
    return incoming.toInt();
}

int parseY(String incoming)
{
    incoming.remove(0, incoming.indexOf(",") + 1);
    incoming.remove(incoming.indexOf("Y"), 1);
    return incoming.toInt();
}

void setup()
{

    Serial.begin(9600);

    StepperX.setSpeed(25);

    servoYL.attach(9);
    servoYR.attach(10);
    Serial.setTimeout(2);
}

void loop()
{
    //StepperX.step(30);
    //servoYL.write(90);
    //servoYR.write(90);
    //StepperX.step(-30);
}

void serialEvent()
{
    incoming = Serial.readString();
    //data += incoming;

    servoYL.write(parseY(incoming));
    servoYR.write(182 - parseY(incoming));
    //servoY.write(parseY(incoming));

    //servoY.write(Ypos);
    //Serial.println(incoming);
}
