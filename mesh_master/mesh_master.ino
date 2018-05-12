
#include <ArduinoJson.h>  
  
#include "RF24Network.h"
#include "RF24.h"
#include "RF24Mesh.h"
#include <SPI.h>
//Include eeprom.h for AVR (Uno, Nano) etc. except ATTiny
#include <EEPROM.h>

/***** Configure the chosen CE,CS pins *****/
RF24 radio(7,8);
RF24Network network(radio);
RF24Mesh mesh(radio,network);

uint32_t displayTimer = 0;

struct Payload {
  int node_id;
  long timestamp;
  float density;  
};


struct Payload payload;
StaticJsonBuffer<200> jsonBuffer;
JsonObject& json= jsonBuffer.createObject();

void setup() {
  Serial.begin(115200);
  //Serial.println("Initializing");
  // Set the nodeID to 0 for the master node
  mesh.setNodeID(0);
  //Serial.println(mesh.getNodeID());
  // Connect to the mesh
  mesh.begin();

}


void loop() {    

  // Call mesh.update to keep the network updated
  mesh.update();
  
  // In addition, keep the 'DHCP service' running on the master node so addresses will
  // be assigned to the sensor nodes
  mesh.DHCP();
  
  
  // Check for incoming data from the sensors
  if(network.available()){
    RF24NetworkHeader header;
    network.peek(header);
    
    switch(header.type){
      // Display the incoming millis() values from the sensor nodes
      case 'M': 
        network.read(header,&payload,sizeof(payload)); 
        json["node_id"] = payload.node_id;
        json["timestamp"] = payload.timestamp;
        json["density"] = payload.density;
        
        json.printTo(Serial); 
        Serial.println();
        break;
      default: network.read(header,0,0); Serial.println(header.type);break;
    }
  }
  /*
  if(millis() - displayTimer > 5000){
    displayTimer = millis();
    Serial.println(" ");
    Serial.println(F("********Assigned Addresses********"));
     for(int i=0; i<mesh.addrListTop; i++){
       Serial.print("NodeID: ");
       Serial.print(mesh.addrList[i].nodeID);
       Serial.print(" RF24Network Address: 0");
       Serial.println(mesh.addrList[i].address,OCT);
     }
    Serial.println(F("**********************************"));
  }
  */
}
