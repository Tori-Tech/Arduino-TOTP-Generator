#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// Non-blocking timer variables
unsigned long lastRequestTime = 0;
const unsigned long interval = 30000; // 30 seconds in milliseconds

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600); 
  
  lcd.print("TOTP Generator");
  lcd.setCursor(0, 1);
  lcd.print("Starting up...");
  delay(1000);
  lcd.clear();
  lcd.print("New code");
  lcd.setCursor(0, 1);
  lcd.print("every 30s");
  delay(2000); // gotta give the system a brief moment to stabilize
  
  lcd.clear();
  lcd.print("Fetching TOTP...");
}

void loop() {
  unsigned long currentMillis = millis();

  // check if 30 seconds have passed, or if this is the very first loop run
  if (currentMillis - lastRequestTime >= interval || lastRequestTime == 0) {
    lastRequestTime = currentMillis;

    lcd.clear();
    lcd.print("Fetching TOTP...");

    // clear any leftover serial data before requesting
    while (Serial.available() > 0) { Serial.read(); }

    // send request to Python server 
    Serial.println("REQ_TOTP");

    // wait for Python to reply; if no response in 2 seconds, time out
    unsigned long startTime = millis();
    while (Serial.available() == 0 && (millis() - startTime < 2000)) {
      // wait for incoming data
    }

    if (Serial.available() > 0) {
      String totpCode = Serial.readStringUntil('\n');
      totpCode.trim(); // clean any trailing spaces

      lcd.clear();
      lcd.print("Your Code:");
      lcd.setCursor(0, 1);
      lcd.print(totpCode);
    } else {
      // if Python didn't respond in time
      lcd.clear();
      lcd.print("Error:");
      lcd.setCursor(0, 1);
      lcd.print("Python Timeout");
    }
  }
}
