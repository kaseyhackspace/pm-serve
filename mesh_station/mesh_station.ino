
//Dust sensor libs
#include <Adafruit_Sensor.h>
#include <SharpDustSensor.h>
//Mesh libs
#include "RF24.h"
#include "RF24Network.h"
#include "RF24Mesh.h"
#include <SPI.h>
#include <EEPROM.h>
//RTC Libs
#include <Wire.h>
#include "RTClib.h"

SharpDustSensor sensor = SharpDustSensor( 1, 9, A6 );

RF24 radio(7, 8);
RF24Network network(radio);
RF24Mesh mesh(radio, network);

#define nodeID 1

RTC_DS3231 rtc;

struct Payload {
  int node_id;
  long timestamp;
  float density;  
};


struct Payload payload;
struct Payload rec_payload;

void setup() {
  
  Serial.begin( 115200 );
  sensor.begin();
  sensor.setUseMultisample(true);
  sensor.setUseMovingAverage(true);
  
  mesh.setNodeID(nodeID);
  mesh.begin();
  
  if (! rtc.begin()) {
    //Serial.println("Couldn't find RTC");
    while (1);
  }
  if (rtc.lostPower()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }
}

void loop() {
  DateTime now = rtc.now();
  
  mesh.update();
  if ( ! mesh.checkConnection() ) {
    //refresh the network address
    //Serial.println("Renewing Address");
    mesh.renewAddress();
  } else {
    //Serial.println("Send fail, Test OK");
  }
          
  if((now.second()%30) == 0){
        //Serial.println(payload.density);
        float density = sensor.getDensity()*2.34;
        payload.node_id = nodeID;
        payload.timestamp = now.unixtime();
        payload.density = density;
        //Serial.println(payload.density);
        
        mesh.update();
      
        // Send an 'M' type message containing the payload
        if (!mesh.write(&payload, 'M', sizeof(payload))) {
        
          // If a write fails, check connectivity to the mesh network
          if ( ! mesh.checkConnection() ) {
            //refresh the network address
            //Serial.println("Renewing Address");
            mesh.renewAddress();
          } else {
            //Serial.println("Send fail, Test OK");
          }
        } 
        /*
        else {
          //Serial.print("Send OK: "); //Serial.println(payload["timestamp"]);
        }
        */
        delay(5000);
  }
  
  while (network.available()) {
    RF24NetworkHeader header;
    network.read(header, &rec_payload, sizeof(rec_payload));
    /*
    Serial.print("Received packet #");
    Serial.println(payload.density);
    */
  }
  
  delay( 1000 );
}
