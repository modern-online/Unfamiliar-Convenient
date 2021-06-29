// Check/Change Roomba's state: Cleaning, Docking, or Charging
void checkRegime() {
  if (currentMillis - prevRegimeMillis >= regimeCheckInterval) {
    bool batteryLowCharge = batteryLow();
    
    if (!cleaning && !batteryLowCharge && !charging) { 
      Serial.print(F("******* CLEANING!! *******"));
      
      // start cleaning
      roo.clean();

      cleaning = true;
      docking = false;
      charging = false;
    }

    else if (!docking && cleaning && batteryLowCharge) {
      roo.seekDock();

      cleaning = false;
      docking = true;
      charging = false;
      gpsCaptured = false; // reset gps capture, not cleaning
    }
 
    else {
      // change to true after debugging
      if (batteryCharging()) {
        //myX = 0;
        //myY = 0;
        
        cleaning = false;
        docking = false;
        charging = true;
  
        // Wait for CS1's green light
        if (!batteryLowCharge && gpsCaptured) {
          // NOT SURE IF THIS IS OK
          charging = false;
        }
      }      
    }
    
    // Update timer
    prevRegimeMillis += regimeCheckInterval;
  }
}

void remoteControl() {   
  if (currentMillis - prevRemoteMillis >= remoteControlInterval) {      
    if (Serial3.available() > 0) {
      String s = Serial3.readString();
      //Serial.println("Message from Python: " + s);
      if (s == "stop") {
        roo.stop();
      }
      else if (s == "start") {
        roo.clean();    
      }
    }
    
    // Update timer
    prevRemoteMillis += remoteControlInterval;
  }
}
