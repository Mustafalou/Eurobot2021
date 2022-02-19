#include <ros.h>
#include <std_msgs/Empty.h>
#include <std_msgs/Float32.h>
#include <std_msgs/String.h>
#include <std_msgs/Int16MultiArray.h>

char frameid[] = "position";
ros::NodeHandle nh;


#define Left_ENC_A 2
#define Left_ENC_B 7
#define Right_ENC_A 3
#define Right_ENC_B 8


void moveCb( const std_msgs::Float32& msg){
  drive(msg.data,500);  // blink the led
}
void rotateCb( const std_msgs::Float32& msg){
  rotate(msg.data,500);  // blink the led
}
void stopCb( const std_msgs::Empty& msg){
  stop();  // blink the led
}
ros::Subscriber<std_msgs::Float32> sub("move", &moveCb );
ros::Subscriber<std_msgs::Float32> sub2("rotate", &rotateCb );
ros::Subscriber<std_msgs::Empty> sub3("stop", &stopCb );

const byte pin_fwdG = 5; //for H-bridge: run motor forward - IN1
const byte pin_bwdG = 6; //for H-bridge: run motor backward -IN2
const byte pin_fwdD = 9; //for H-bridge: run motor forward - IN 1
const byte pin_bwdD = 10; //for H-bridge: run motor backward- IN 2

int right_pos =0 ;
int left_pos =0 ;
std_msgs::Int16MultiArray  pos;

ros::Publisher pub_position("position", &pos);
int lowSpeed = 200;
int highSpeed = 50;
double speed_ang = 0, speed_lin = 0;
double wheel_rad = 0.035, wheel_sep = 0.24;

unsigned long previousMillis = 0;
double distanceD = 0;
double distanceG = 0;
double distanceC = 0;
double w_r = 0, w_l = 0;
double x_current = 0.0;
double y_current = 0.0;
double theta = 0.0;

double x_final = 0.05;
double y_final = 0.0;

void setup(){
  
  nh.initNode();
  nh.advertise(pub_position);
  nh.subscribe(sub);
  nh.subscribe(sub2);
  nh.subscribe(sub3);
  //Serial.begin(9600);
  pinMode(Right_ENC_A,INPUT);
  pinMode(Right_ENC_B,INPUT);
  attachInterrupt(digitalPinToInterrupt(Right_ENC_A), readRightEncoder, RISING);

  pinMode(Left_ENC_A,INPUT);
  pinMode(Left_ENC_B,INPUT);
  attachInterrupt(digitalPinToInterrupt(Left_ENC_A), readLeftEncoder, RISING);

  digitalWrite(pin_fwdG, 0); //stop motor
  digitalWrite(pin_bwdG, 0); //stop motor
  digitalWrite(pin_fwdD, 0); //stop motor
  digitalWrite(pin_bwdD, 0); //stop motor
  //Serial.begin(9600);
}

void MotorL(int Pulse_Width1);
void MotorR(int Pulse_Width2);
long range_time;

void loop(){
  


  //Serial.begin(9600);
  
  distanceG = ((left_pos) * 2 * 3.14 * wheel_rad) / 1920; // 0.035m=Radius of the wheels
  //left_pos = 0;

  distanceD = ((right_pos) * 2 * 3.14 * wheel_rad) / 1920; //
  //right_pos = 0;

  distanceC = (distanceG + distanceD) / 2;

  theta += (distanceD - distanceG) / wheel_sep; // 0.24m =distance between wheels
  x_current += cos(theta) * distanceC;
  y_current += sin(theta) * distanceC;
  
  /*
  Serial.println("X :");
  Serial.println(x_current);
  Serial.println("Y :");
  Serial.println(y_current);
  */
  
  Serial.print("Left pos");
  Serial.println(left_pos);
  Serial.print("Right pos");
  Serial.println(right_pos);
  
  nh.spinOnce();
  
    
}

void readRightEncoder(){
   (digitalRead(Right_ENC_B)>0) ? (right_pos++) : (right_pos--);
}

void readLeftEncoder(){
   (digitalRead(Left_ENC_B)>0) ? (left_pos--) : (left_pos++);
}

void MotorL(int Pulse_Width1) {
  if (Pulse_Width1 > 0) {
    analogWrite(pin_fwdG, Pulse_Width1);
  }
  if (Pulse_Width1 < 0) {
    Pulse_Width1 = abs(Pulse_Width1);
    analogWrite(pin_bwdG, Pulse_Width1);
  }
  if (Pulse_Width1 == 0) {
    analogWrite(pin_fwdG, Pulse_Width1);
    analogWrite(pin_bwdG, Pulse_Width1);
  }
}
void MotorR(int Pulse_Width2) {
  if (Pulse_Width2 > 0) {
    analogWrite(pin_fwdD,Pulse_Width2);

  }
  if (Pulse_Width2 < 0) {
    Pulse_Width2 = abs(Pulse_Width2);
    analogWrite(pin_bwdD, Pulse_Width2);

  }
  if (Pulse_Width2 == 0) {
    analogWrite(pin_fwdD, Pulse_Width2);
    analogWrite(pin_bwdD, Pulse_Width2);

  }
}
void rotate(int val, int tps){
  MotorL(val);
  MotorR(-val);
  delay(tps);
  stop();
  
  
  }
void drive(int val, int tps){
  MotorL(val);
  MotorR(val);
}
int positions[2];
void stopcb(){
  MotorL(0);
  MotorR(0);
}
void givePosition(){
  pos.data[2]=right_pos;
  pos.data[1]=left_pos;
  pos.data_length=3;
  pub_position.publish(&pos);
}
