#include <TimeLib.h>
#include <dht.h>



#define anInput     A0                        //analog feed from MQ135
#define co2Zero     200                     //calibrated CO2 0 level 13-22 100ppm
                                              // 32-61 52ppm 55 will give best resoulution
#define dht_apin    A1
#define an1Input    A2                        //Analog feed from MQ9
#define coZero      100                       //calibrated CO 0 level 
#define TIME_HEADER  "T"
#define TIME_REQUEST  7
//---------------------------------------------------------------------------------------------------------------
//                                                  SETUP
//---------------------------------------------------------------------------------------------------------------
dht DHT;
void setup() {
  
  pinMode(anInput,INPUT);                     //MQ135 analog feed set for input
  Serial.begin(9600);                         //serial comms for debuging
  //Serial.println("Time,CO2,CO,Temperature,Humidity");
  setTime(1553096100);//Set this before going live
  
  
}
//---------------------------------------------------------------------------------------------------------------
//                                               MAIN LOOP
//---------------------------------------------------------------------------------------------------------------
void loop() {

  DHT.read11(dht_apin);
//    Serial.print("Current humidity = ");
//    Serial.print(DHT.humidity);
//    Serial.print("%  ");
//    Serial.print("temperature = ");
//    Serial.print(DHT.temperature); 
//    Serial.println("C  ");
    delay(100);
    //Serial.print(" ");
int potato=0;    
int co2now[10];                               //int array for co2 readings
int co2raw = 0;                               //int for raw value of co2
int co2comp = 0;                              //int for compensated co2 
int co2ppm = 0;                               //int for calculated ppm
int zzz = 0;                                  //int for averaging
int grafX = 0;
int a=0;//int for x value of graph


  
//CO2
  for (int x = 0;x<10;x++){                   //samplpe co2 10x over 2 seconds
    co2now[x]=analogRead(A0);
    delay(200);
  }

for (int x = 0;x<10;x++){                     //add samples together
    zzz=zzz + co2now[x];
    
  }
  co2raw = zzz/10;                            //divide samples by 10
  co2comp = co2raw - co2Zero;                 //get compensated value
  co2ppm = map(co2comp,0,1023,300,2000);
  //Serial.print("CO2 Level");               //print title
//  Serial.print(" ");                       //skip a line
//  Serial.print(co2ppm);                      //print co2 ppm
//  Serial.println("PPM");                      //print units

  // C0
  int conow[10];                               //int array for co2 readings
int coraw = 0;                               //int for raw value of co2
int cocomp = 0;                              //int for compensated co2 
int coppm = 0;                               //int for calculated ppm
int zzz1 = 0;                                  //int for averaging
int grafX1 = 0;                                //int for x value of graph
for (int x1 = 0;x1<10;x1++){                   //samplpe co2 10x over 2 seconds
    co2now[x1]=analogRead(A2);
    delay(200);
  }

for (int x1 = 0;x1<10;x1++){                     //add samples together
    zzz1=zzz1 + conow[x1];
    
  }
  coraw = zzz/10;                            //divide samples by 10
  cocomp = coraw - coZero;                 //get compensated value
  coppm = map(cocomp,0,1023,3,50);
//  Serial.print(" ");                       //skip a line
//  Serial.print(coppm);                      //print co2 ppm
//  Serial.println(" PPM");  //print units
//Time Stuff

//TIme Stuff
if(co2ppm<700){
digitalClockDisplay();
Serial.print(",");
Serial.print(co2ppm);
Serial.print(",");
Serial.print(coppm);
Serial.print(",");
Serial.print(DHT.temperature);
Serial.print(",");
Serial.print(DHT.humidity);
Serial.println();
}


}
//void processSyncMessage() {
//  unsigned long pctime;
//  const unsigned long DEFAULT_TIME = 1553033640; // Jan 1 2013
//
//  if(Serial.find(TIME_HEADER)) {
//     pctime = Serial.parseInt();
//     if( pctime >= DEFAULT_TIME) { // check the integer is a valid time (greater than Jan 1 2013)
//       setTime(pctime); // Sync Arduino clock to the time received on the serial port
//     }
//  }
//}

time_t requestSync()
{
  Serial.write(TIME_REQUEST);  
  return 0; // the time will be sent later in response to serial mesg
}
void digitalClockDisplay(){
  // digital clock display of the time
  Serial.print(hour());
  printDigits(minute());
  printDigits(second());
  Serial.print(" "); 
}
void printDigits(int digits){
  // utility function for digital clock display: prints preceding colon and leading 0
  Serial.print(":");
  if(digits < 10)
    Serial.print('0');
  Serial.print(digits);
}




