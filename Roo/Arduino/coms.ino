void toPython() {
  if (currentMillis - prevSendMillis >= sendInterval) {
    String buf;
    buf += String(myX, 1);
    buf += F(";");
    buf += String(myY, 1);

    // Send buffer of Roomba's coordinates to Python
    Serial3.println(buf);
    Serial3.flush();

    // Send GPS data to Python

    if (gps.location.isValid())
      Serial3.println((gps.location.lat(), 6) + ";" + (gps.location.lng(), 6));
    
    
    // Update send timer
    prevSendMillis += sendInterval;
  }
}
