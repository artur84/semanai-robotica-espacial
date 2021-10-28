//#define USE_USBCON //Uncomment this line if you are using an arduino DUE
/*
 * This program receives a ROS (Int32) message (between -255 and 255)
 * and commands the left and right DC motors of your rover (according to the specified value).
 * subscribed ROS topics 
 * - left_wheel_speed
 * - right_wheel_speed
 */

 #include "Arduino.h"
 #include <ros.h>
 #include <std_msgs/Int32.h>

/*******************************
 * Define the material
 ******************************/
//Arduino pin definitions
#define MLEFT_IN1 6//IN1 of the L298 should be connected to this arduino pin
#define MLEFT_IN2 7//IN2 of the L298 should be connected to this arduino pin
#define MLEFT_EN 8 //enable A
#define MRIGHT_IN1 9//IN3 of the L298 should be connected to this arduino pin
#define MRIGHT_IN2 10//IN4 of the L298 should be connected to this arduino pin
#define MRIGHT_EN 11 //enable B
#define LED 13 //A led that blinks when receiving


/*
 * Global variables
 */
ros::NodeHandle nh;
volatile int left_vel; //The motor velocity between -255->full speed backwards and 255-> Full speed forward
volatile int right_vel; //The motor velocity between -255->full speed backwards and 255-> Full speed forward

/* 
 * Stop the left motor
 */
void left_motor_stop() {
	//Stop if received an wrong direction
		digitalWrite(MLEFT_IN1, 0);
		digitalWrite(MLEFT_IN2, 0);
		analogWrite(MLEFT_EN, 0);
}

/* 
 * Stop the right motor
 */
void right_motor_stop() {
  //Stop if received an wrong direction
    digitalWrite(MRIGHT_IN1, 0);
    digitalWrite(MRIGHT_IN2, 0);
    analogWrite(MRIGHT_EN, 0);
}

/* Moves the motor in positive direction
		vel: [0-255] the desired pwm value 255 means full speed
 */
void left_motor_forward(unsigned int vel) {
		digitalWrite(MLEFT_IN1, 1);
		digitalWrite(MLEFT_IN2, 0);
		analogWrite(MLEFT_EN, vel);
}

/* Moves the motor in positive direction
    vel: [0-255] the desired pwm value 255 means full speed
 */
void right_motor_forward(unsigned int vel) {
    digitalWrite(MRIGHT_IN1, 1);
    digitalWrite(MRIGHT_IN2, 0);
    analogWrite(MRIGHT_EN, vel);
}

/* Moves the left motor backwards
		vel: [0-255] the desired pwm value 255 means full speed
 */
void left_motor_backwards(unsigned int vel) {
    digitalWrite(MLEFT_IN1, 0);
    digitalWrite(MLEFT_IN2, 1);
    analogWrite(MLEFT_EN, vel);
}

/* Moves right the motor backwards
    vel: [0-255] the desired pwm value 255 means full speed
 */
void right_motor_backwards(unsigned int vel) {
    digitalWrite(MRIGHT_IN1, 0);
    digitalWrite(MRIGHT_IN2, 1);
    analogWrite(MRIGHT_EN, vel);
}

//Left Motor callback
void left_vel_cb(const std_msgs::Int32 & msg) {
	digitalWrite(LED, HIGH - digitalRead(LED)); //toggles a led to indicate this topic is active
	left_vel = msg.data;
	if (left_vel > 0 && left_vel <= 255) {
		left_motor_forward((unsigned int) left_vel);
	} else if (left_vel < 0 && left_vel >= -255) {
		left_motor_backwards((unsigned int) -1*left_vel);
	} else {
		//Stop if received a wrong value or 0
		left_motor_stop();
	}
}

//Right Motor callback
void right_vel_cb(const std_msgs::Int32 & msg) {
  digitalWrite(LED, HIGH - digitalRead(LED)); //toggles a led to indicate this topic is active
  right_vel = msg.data;
  if (right_vel > 0 && right_vel <= 255) {
    right_motor_forward((unsigned int) right_vel);
  } else if (right_vel < 0 && right_vel >= -255) {
    right_motor_backwards((unsigned int) -1*right_vel);
  } else {
    //Stop if received a wrong value or 0
    right_motor_stop();
  }
}


//Creates the ROS subscribers
ros::Subscriber<std_msgs::Int32> left_vel_sub("left_wheel_speed", left_vel_cb);
ros::Subscriber<std_msgs::Int32> right_vel_sub("right_wheel_speed", right_vel_cb);
/*
 * Arduino SETUP
 */
void setup() {
	//init ROS communication
	nh.initNode();
	//Subscribed ROS topics
	nh.subscribe(left_vel_sub);
  nh.subscribe(right_vel_sub);
	// Arduino pins definition
	pinMode(LED, OUTPUT);
	pinMode(MLEFT_IN1, OUTPUT);
	pinMode(MLEFT_IN2, OUTPUT);
	pinMode(MLEFT_EN, OUTPUT);
  pinMode(MRIGHT_IN1, OUTPUT);
  pinMode(MRIGHT_IN2, OUTPUT);
  pinMode(MRIGHT_EN, OUTPUT);
}

/*
 * Arduino MAIN LOOP
 */
void loop() {
	nh.spinOnce();
	delay(1);
}
