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


void moveCb( const std_msgs::Int16MultiArray& msg){
  drive(msg.data[0],msg.data[1]);  
}
void rotateCb( const std_msgs::Int16MultiArray& msg){
  rotate(msg.data[0],msg.data[1]);  
}
void stopCb( const std_msgs::Empty& msg){
  stop();
}
void startCb(const std_msgs::Empty& msg) {
  givePosition();
}
ros::Subscriber<std_msgs::Int16MultiArray> sub("move", &moveCb );
ros::Subscriber<std_msgs::Int16MultiArray> sub2("rotate", &rotateCb );
ros::Subscriber<std_msgs::Empty> sub3("stop", &stopCb );
ros::Subscriber<std_msgs::Empty> sub4("start", &startCb);
const byte pin_fwdG = 5; //for H-bridge: run motor forward - IN1
const byte pin_bwdG = 6; //for H-bridge: run motor backward -IN2
const byte pin_fwdD = 9; //for H-bridge: run motor forward - IN 1
const byte pin_bwdD = 10; //for H-bridge: run motor backward- IN 2

int right_pos =0 ;
int left_pos =0 ;
int final_right_pos=0;
int final_left_pos=0;
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

bool action_done = false;
void setup(){
  
  nh.initNode();
  nh.advertise(pub_position);
  nh.subscribe(sub);
  nh.subscribe(sub2);
  nh.subscribe(sub3);
  nh.subscribe(sub4);
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
int i=0;
void loop(){
  if (action_done ==true &&  i == 0) i++;stop();
  distanceG = ((left_pos) * 2 * 3.14 * wheel_rad) / 1920; // 0.035m=Radius of the wheels
  //left_pos = 0;

  distanceD = ((right_pos) * 2 * 3.14 * wheel_rad) / 1920; //
  //right_pos = 0;

  distanceC = (distanceG + distanceD) / 2;

  theta += (distanceD - distanceG) / wheel_sep; // 0.24m =distance between wheels
  x_current += cos(theta) * distanceC;
  y_current += sin(theta) * distanceC;
  
  
  Serial.print("Left pos");
  Serial.println(left_pos);
  Serial.print("Right pos");
  Serial.println(right_pos);
  
  nh.spinOnce();
}

void readRightEncoder(){
   
   if (digitalRead(Right_ENC_B)>0)  {
    right_pos-- ;
    if (right_pos - final_right_pos <=0) action_done=true;
   }else{
    right_pos++;
    if (right_pos - final_right_pos >=0) action_done=true;
   }
   
}
void readLeftEncoder(){
   if (digitalRead(Left_ENC_B)>0)  {
    left_pos++ ;
    if (left_pos - final_left_pos >0) action_done=true;
   }else{
    left_pos--;
    if (left_pos - final_left_pos <0) action_done=true;
   }
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
void rotate(int val, int tick){
  final_left_pos  += tick;
  final_right_pos -= tick;
  action_done=false;
  i=0;
  delay(500);
  MotorL(val);
  MotorR(-val);
}
void drive(int val, int tick){
  final_right_pos += tick;
  final_left_pos  += tick;
  action_done=false;
  i=0;
  delay(500);
  MotorL(val);
  MotorR(val);
  
}
void stop(){
  MotorL(0);
  MotorR(0);
  givePosition();
}
void givePosition(){
  pos.data[2]=right_pos;
  pos.data[1]=left_pos; 
  pos.data[4]=final_right_pos;
  pos.data[3]=final_left_pos;  
  pos.data_length=5;
  pub_position.publish(&pos);
}