// Arduino code for moisture sensor
//Output in percentage

#include <ros.h>
#include <std_msgs/Int16.h>

ros::NodeHandle nh;
std_msgs::Int16 moisture_percent;
ros::Publisher moisture_publisher("sensor/moisture",&moisture_percent);

int sensor_pin = A0;
int moisture_value = 0;

void setup(){
    nh.initNode();
    nh.advertise(moisture_publisher);
}

void loop(){
    moisture_percent.data = dataAcquisition();
    moisture_publisher.publish(&moisture_percent);
    nh.spinOnce();
    delay(500);
}

int dataAcquisition(){
    moisture_value = analogRead(sensor_pin);
    return convertToPercentage(moisture_value);
    // For calibrations comment the above line
    // and uncoment the next one 
    //return moisture_value;
}

int convertToPercentage(int value){
    int percentValue = 0;
    percentValue = map(value,1024, 255, 0, 100);
    return percentValue;
}