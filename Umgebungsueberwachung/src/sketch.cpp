#include <Arduino.h>
#include <DHT.h>
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789
#include <SPI.h>
#include <stdio.h>



// PIN Definition DHT22 Sensoren
#define DHTTYPE DHT22
DHT dht1(2,DHT22);
DHT dht2(4,DHT22);
DHT dht3(7,DHT22);

// PIN Definition TFT-Display
#define DC 8
#define RES 9
#define CS 10

Adafruit_ST7735 TFTScreen = Adafruit_ST7735(CS, DC, RES); 

void setup() {

  // Ausgabe auf Seriellen Monitor
  Serial.begin(9600);
  //Serial.println(F("DHT22 test!"));

  // DHT Sensoren auslesen
  dht1.begin();
  dht2.begin();
  dht3.begin();

//  // Ausgabe auf TFT Bildschirm starten und Hintergrundbildschirm auf Schwarz
  // TFTScreen.begin();
  TFTScreen.initR(INITR_BLACKTAB);  // Hintergrund auf Schwarz
  TFTScreen.setTextSize(1);    // Textgroeße
  TFTScreen.setRotation(1);
  
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)

  // 1. DHT Sensor
  float h1 = dht1.readHumidity();
  // Read temperature as Celsius (the default)
  float t1 = dht1.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f1 = dht1.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h1) || isnan(t1) || isnan(f1)) 
  {
    Serial.println(F("Sensor DHT_1 konnnte nicht ausgelesen werden!")); 
  }
  else
  {
    // Serial.println(F("DHT_1 hat folgende Werte"));
    // Serial.print(F("Luftfeuchtigkeit: "));
    // Serial.print(h1);
    // Serial.print(F("%  Temperatur: "));
    // Serial.print(t1);
    // Serial.print(F("°C "));
    // Serial.print(f1);
    // Serial.println(F("°F"));
  }


  // 2. DHT Sensorf
  float h2 = dht2.readHumidity();
  // Read temperature as Celsius (the default)
  float t2 = dht2.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f2 = dht2.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h2) || isnan(t2) || isnan(f2)) 
  {
    Serial.println(F("Sensor DHT_2 konnnte nicht ausgelesen werden!"));
  }
  else
  {
    // Serial.println(F("DHT_2 hat folgende Werte"));
    // Serial.print(F("Luftfeuchtigkeit: "));
    // Serial.print(h2);
    // Serial.print(F("%  Temperatur: "));
    // Serial.print(t2);
    // Serial.print(F("°C "));
    // Serial.print(f2);
    // Serial.println(F("°F"));
  }

  
  // 3. DHT Sensor
  float h3 = dht3.readHumidity();
  // Read temperature as Celsius (the default)
  float t3 = dht3.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f3 = dht3.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h3) || isnan(t3) || isnan(f3)) 
  {
    Serial.println(F("Sensor DHT_3 konnnte nicht ausgelesen werden!"));
  }
  else
  {
    // Serial.println(F("DHT_3 hat folgende Werte"));
    // Serial.print(F("Luftfeuchtigkeit: "));
    // Serial.print(h3);
    // Serial.print(F("%  Temperatur: "));
    // Serial.print(t3);
    // Serial.print(F("°C "));
    // Serial.print(f3);
    // Serial.println(F("°F"));
  }


  // Gesamt
  float h_ges = (h1 + h2 + h3)/3;
  float t_ges = (t1 + t2 + t3)/3;
  
  //Serial.println(F("Gesamtwerte"));
  //Serial.print(F("Durchschnittliche Luftfeuchtigkeit: "));
  Serial.print(h_ges);
  Serial.print(F("%,"));
  Serial.print(t_ges);
  Serial.print(F("C,"));
  Serial.print(t1); 
  Serial.print("T1,"); 
  Serial.print(t2); 
  Serial.print("T2,"); 
  Serial.print(t3); 
  Serial.print("T3,"); 
  Serial.print(h1); 
  Serial.print("H1,");
  Serial.print(h2); 
  Serial.print("H2,");
  Serial.print(h3); 
  Serial.println("H3");   



  // TFT Ausgabe
  TFTScreen.fillScreen(ST77XX_BLACK);
  TFTScreen.setTextColor(ST77XX_WHITE);
  TFTScreen.setCursor(0, 2);
  TFTScreen.println(" Gesamtwerte");
  TFTScreen.println(" ");
  TFTScreen.println(" Durchschnittliche");
  TFTScreen.println(" Luftfeuchtigkeit: ");
  TFTScreen.print(" ");
  TFTScreen.print(h_ges);
  TFTScreen.println("%");
  TFTScreen.println(" ");
  TFTScreen.println(" Durchschnittliche");
  TFTScreen.println(" Temperatur: ");
  TFTScreen.print(" ");
  TFTScreen.print(t_ges);
  TFTScreen.print(B0, HEX);
  TFTScreen.println("C");

}
