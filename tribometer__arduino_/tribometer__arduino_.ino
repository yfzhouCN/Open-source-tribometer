#include<MsTimer2.h>     
#define fiction A1
long voltage;
const int dirPin   = 2;   
const int pulPin  = 3;  

const int STEPS_PER_REV =2000;
 
char cmd; 
float data;  
long Motor_Speed;
long Motor_time;
float Motor_r;
float Motor_sudu;
long Motor_zhuansu;


boolean  Motor_Speed_flag=false;
boolean  Motor_Time_flag=false;


const int buttonPin = 10;     
int buttonState = 0;         



void fiction_read() {
     voltage = analogRead(fiction);
 
     Serial.println(voltage);
  
}

void setup() { 
 
  pinMode(pulPin,OUTPUT); 
  pinMode(dirPin,OUTPUT); 
 
  
  Serial.begin(9600);
  Serial.println("+++++++++++++++++++++++++++++++++++++++++++++++++++");     
  Serial.println("+          Friction corrosion tester              +");   
  Serial.println("+++++++++++++++++++++++++++++++++++++++++++++++++++");  
  Serial.println("");  
  Serial.println("Please input the instructions of the stepper motor:"); 

  MsTimer2::set(100,fiction_read);   
  
}
 
void loop() {    
  if (Serial.available()) {     
    cmd = Serial.read();           
     
 
    data = Serial.parseInt();
    
    runUsrCmd();
   
  }
} 
 

void runUsrCmd(){
  switch(cmd){ 
    case 'x':    
      Serial.print("Set Rotation To "); 
      if (data == 0){
        digitalWrite(dirPin, 0);
        Serial.println("Clockwise."); 
      } else {
        digitalWrite(dirPin, 1);
        Serial.println("Anticlockwise."); 
      }
      break;
      
    case 'd': 
      Motor_zhuansu = data;
      Motor_Speed = 15000/(data);
      Motor_Speed_flag=true;
      Serial.print("Half pulse time (us) ");
      Serial.println(Motor_Speed);
      Serial.print("Step motor speed (r/min) ");
      Serial.println(Motor_zhuansu);
      
      break;

    case 'q':
      Motor_r =data;
     Serial.print("Turning radius(mm) ");
     Serial.println(data);
       break;
       
    case 'w':
      Motor_sudu = data;
      Motor_Speed=15000*2*Motor_r*3.14/(Motor_sudu*60);
      Serial.print("Half pulse time (us)");
      Serial.println(Motor_Speed);
      break;
    
      
    case 't': 
      
    
      Motor_time=data*2000;
      Motor_Time_flag=true;
      Serial.print("Stepper motor cycles ");
      Serial.println(data);
      break; 


     case 'y': 
     if(Motor_Speed_flag&&Motor_Time_flag){
   
       Motor_Speed=Motor_Speed-10;
       runStepper(Motor_Speed, Motor_time);
     }
      else{
        Serial.println("Please set up the parameter first! "); 
      }
      break;   
      
    case 'z':    
      Serial.println("Start measuring "); 
    
      while(cmd != 'a') {
         voltage = analogRead(fiction);
         Serial.print("fiction(N) ");
         Serial.println(voltage*5.00/1023);
     
         delay(500);
         cmd = Serial.read(); 
          
      }
      Serial.print("Stop");
      break; 

    default:  
      Serial.println("Unknown Command");
  }
}
 
void runStepper (long rotationSpeed, long stepNum){
  MsTimer2::start();     
  for(long x = 0; x < stepNum && cmd != 's'; x++) {
    digitalWrite(pulPin,HIGH); 
    delayMicroseconds(rotationSpeed); 
    digitalWrite(pulPin,LOW); 
    delayMicroseconds(rotationSpeed); 
    cmd = Serial.read(); 
    
   
  }  
  MsTimer2::stop();      

}


 
