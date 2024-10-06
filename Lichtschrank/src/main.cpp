#include <Arduino.h>

#include <EEPROM.h>
//Variablen werden definiert. Lichtschranke 1=Unterbrechung auf Pin 2 und A0. Lichtschranke 2=Unterbrechungzwei auf Pin 3 und A1.

const int EEPROMAddr = 42;

volatile int const Unterbrechungen = 2;
int const Signaleingang = 0;
volatile int const Unterbrechungenzwei = 3;
int const Signaleingangzwei = 1;

const int digitalAus1 = 6;
const int digitalAus2 = 7;

// der Aufzählungsdatenyp enthält Bezeichnungen für alle Zustände, die unser System einnehmen kann.
enum zustand { grund,
               einS1lS2h,
               einzS1hS2h,
               einzS1lS2l,
               einS1hS2l,
               einErkannt,
               ausS1hS2l,
               auszS1hS2h,
               auszS1lS2l,
               ausS1lS2h,
               ausErkannt,
               fehler };
// zugehörige Variable
zustand erkennungsZustand;

//Variablen für die Zaehler für Ein- und Ausflüge
int anzahlEinfluege;
int anzahlAusfluege;

//Variable für die Ausgabe der im Turm befindlichen Fledermäuse insgesamt
int Gesamtanzahl;

//Raw Value einmal ausgehend von A0 und einmal ausgehend von A1
double analog0Voltage;
double analog1Voltage;

// Variable, die den Zeitpunkt des Eintritts in einen Zustand speichert
unsigned long stateEntryTime;
const unsigned long maxStateDuration2Base = 5000;    // Maximalzeit bis wir wieder in den Grundzustand übergehen: 5000 ms
const unsigned long maxStateDuration2Error = 10000;  // Maximalzeit bis wir in den Fehlerzustand übergehen: 10000 ms
unsigned long stateDuration;                         // wie lange sind wir schon in einem jeweiligen Zustand
unsigned long currentTime;

unsigned long serialWriteTime;  // um alle 30 Sekunden die Fledermauszahl zu schreiben
unsigned long previousSerialWriteTime;

//Werte für CheckserialInput
int extractedValue = 0;
bool newData = false;


//Diese Funktion überwacht die serielle Monitor und fang die Anfangsanzahl der Fledermauser ab: 
void checkSerialInput() {
  static byte ndx = 0;
  char receivedChars[32];  // Buffer to store the received characters
  const char startMarker = 'P';
  const char endMarker = '\n';
  char rc;
  
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= sizeof(receivedChars)) {
        ndx = sizeof(receivedChars) - 1;
      }
    }
    else {
      receivedChars[ndx] = '\0';  // Null-terminate the string
      ndx = 0;
      
      // Check if the received string starts with "PY:"
      if (strncmp(receivedChars, "PY:", 3) == 0) {
        extractedValue = atoi(receivedChars + 3);  // Extract the integer value
        newData = true;
      }
    }
  }
}

double readAnalogVoltage(int analogInput) {
  int analogRawValue;
  double measuredVoltage;

  analogRawValue = analogRead(analogInput);
  delay(5);
  analogRawValue = analogRead(analogInput);  //Frage: Warum wird A0 hier direkt nochmal ausgelesen?
  // Arduinos besitzen einen Analog-Digital-Wandler (Analog-Digital-Converter bzw. ADC auf Englisch).
  // Um genau zu sein: Arduinos besitzen genau einen (1) ADC.
  // Das bedeutet, dass alle digitalen Eingänge über den einen ADC ausgelesen werden.
  // Wird zuerst A0 ausgelesen und anschließend A1, so geschieht folgendes:
  // Der Eingang des ADC wird auf den analogen Eingang geschaltet, von dem gelesen werden soll
  // anschließend wird die Spannung ausgelesen und in einen Zahlenwert zwischen 0 und 1023
  // umgewandelt.
  // Wenn ich also erst von A0 und anschließend von A1 Werte lese, muss ich auf A1 umschalten.
  // Die Erfahrung zeigt, dass unmittelbar nach dem Umschalten, wenn der ADC direkt die Spannung
  // liest, der Spannungswert, der am "neuen" Eingang (in dem Fall A1) liegt, noch nicht
  // korrekt gelesen wird.
  // Abhilfe: Zum Umschalten analogRead() ausführen, dann ein paar ms warten und anschließend
  // nochmal auslesen. Der zweite Wert ist dann korrekt.

  measuredVoltage = analogRawValue / 1023.0 * 5;  //Umrechnung des Raw Value (liegt zwischen 0-1023) in Spannung (zw. 0-5 V)
  // Ergebnis zurückgeben
  return measuredVoltage;
}


// Diese Funktion wird aufgerufen wenn am Signal 1 ein Interrupt aufgetreten ist (steigende oder fallende Flanke)
void handleInterrupt1() {
  // Erkennen um welche Flanke es sich handelt
  // Signal-Pin: Unterbrechungen
  bool readValue;                            // wir erzeugen eine logische Variable
  readValue = digitalRead(Unterbrechungen);  // wir lesen den Wert am Pin "Unterbrechungen" (LOW bzw. false oder HIGH bzw. true)
  if (readValue)
  // Verarbeitung der steigenden Flanke
  {
    ///////////////////////// Von uns auskommentiert /////////////////////////
    // Serial.println("Eingang 1 steigende Flanke erkannt");
    ///////////////////////// Von uns auskommentiert /////////////////////////

    // Hier fragen wir für alle möglichen Zustände ab, was passieren soll, wenn am Eingang 1 eine steigende Flanke auftaucht.
    if (erkennungsZustand == einS1lS2h) {
      erkennungsZustand = einzS1hS2h;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();  // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == einzS1lS2l) {
      erkennungsZustand = einS1hS2l;
      // Das ist ein Übergang in einen Zwischenzustand, von dem aus wir bei Timeout in einen Fehlerzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();                 // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == auszS1lS2l)  // Fehler-Übergang zurück zum vorherigen Zustand
    {
      erkennungsZustand = ausS1hS2l;
      // Das ist ein Übergang in einen Zwischenzustand, von dem aus wir bei Timeout in einen Fehlerzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();                // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == ausS1lS2h)  // DAs ist der Übergang, bei dem wir einen Ausflug erkannt haben
    {
      // Ausflug-Zähler um eins erhöhen und anschließend in Grundzustand zurück
      anzahlAusfluege++;  // entspricht dem Zustand Ausflug erkannt

      ///////////////////////// Von uns auskommentiert /////////////////////////
      // Serial.print("Anzahl Ausfluege: ");
      // Serial.println(anzahlAusfluege);
      ///////////////////////// Von uns auskommentiert /////////////////////////

      erkennungsZustand = grund;
      // Bei Übergang in Grundzustand gibt es keinen Timeout mehr.
      // Daher in der stateEntryTime merken, dass kein Timeout mehr möglich ist
      stateEntryTime = 0;

      //Die Gesamtanzahl der im Turm befindlichen Fledermäuse ausgeben nachdem ein Ausflug registriert wurde
      if (Gesamtanzahl > 0)
        Gesamtanzahl = Gesamtanzahl - 1;
      else (Gesamtanzahl = 0);
      // Serial.print("Im Turm befindliche Fledermaeuse: ");
      
      Serial.print("->");
      Serial.print(anzahlEinfluege);
      Serial.print(", <-");
      Serial.print(anzahlAusfluege);
      Serial.print(", $");
      Serial.println(Gesamtanzahl);
      EEPROM.put(EEPROMAddr, Gesamtanzahl);
    }
  } else
  // Verarbeitung der fallenden Flanke
  {
    ///////////////////////// Von uns auskommentiert /////////////////////////
    // Serial.println("Eingang 1 fallende Flanke erkannt");
    ///////////////////////// Von uns auskommentiert /////////////////////////

    // Hier fragen wir für alle möglichen Zustände ab, was passieren soll, wenn am Eingang 1 eine fallende Flanke auftaucht.
    //NAMEN ZUSTÄNDE: grund, einS1lS2h, einzS1hS2h, einzS1lS2l, einS1hS2l, einErkannt, ausS1hS2l, auszS1hS2h, auszS1lS2l, ausS1lS2h, ausErkannt, fehler
    if (erkennungsZustand == grund) {
      erkennungsZustand = einS1lS2h;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();                 // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == einzS1hS2h)  // Fehler-Übergang zurück zum vorherigen Zustand
    {
      erkennungsZustand = einS1lS2h;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();                // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == einS1hS2l)  // Fehler-Übergang zurück zum vorherigen Zustand
    {
      erkennungsZustand = einzS1lS2l;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();  // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == ausS1hS2l) {
      erkennungsZustand = auszS1lS2l;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();  // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == auszS1hS2h) {
      erkennungsZustand = ausS1lS2h;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();  // millis() sagt wir lange der Arduino läuft in Millisekunden
    }
  }
}




// Diese Funktion wird aufgerufen wenn am Signal 2 ein Interrupt aufgetreten ist (steigende oder fallende Flanke)
void handleInterrupt2() {
  // Erkennen um welche Flanke es sich handelt
  // Signal-Pin: Unterbrechungenzwei
  bool readValue;                                // wir erzeugen eine logische Variable
  readValue = digitalRead(Unterbrechungenzwei);  // wir lesen den Wert am Pin "Unterbrechungenzwei" (LOW bzw. false oder HIGH bzw. true)
  if (readValue)
  // Verarbeitung der steigenden Flanke

  {
    ///////////////////////// Von uns auskommentiert /////////////////////////
    // Serial.println("Eingang 2 steigende Flanke erkannt");
    ///////////////////////// Von uns auskommentiert /////////////////////////
    // Hier fragen wir für alle möglichen Zustände ab, was passieren soll, wenn am Eingang 2 eine steigende Flanke auftaucht.
    if (erkennungsZustand == einzS1lS2l) {
      erkennungsZustand = einS1lS2h;            // Fehler-Übergang zurück zum vorherigen Zustand
                                                // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
                                                // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();                // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == einS1hS2l)  // Das ist der Übergang, bei dem wir einen Einflug erkannt haben
    {
      // Einflug-Zähler um eins erhöhen und anschließend in Grundzustand zurück
      anzahlEinfluege++;  // entspricht dem Zustand Einflug erkannt

      ///////////////////////// Von uns auskommentiert /////////////////////////
      // Serial.print("Anzahl Einfluege: ");
      // Serial.println(anzahlEinfluege);
      ///////////////////////// Von uns auskommentiert /////////////////////////

      erkennungsZustand = grund;

      // Bei Übergang in Grundzustand gibt es keinen Timeout mehr.
      // Daher in der stateEntryTime merken, dass kein Timeout mehr möglich ist
      stateEntryTime = 0;

      //Die Gesamtanzahl der im Turm befindlichen Fledermäuse ausgeben nachdem ein Einflug registriert wurde
      Gesamtanzahl = Gesamtanzahl + 1;
      ///////////////////////// Von uns auskommentiert /////////////////////////
      // Serial.print("Im Turm befindliche Fledermaeuse: ");
      ///////////////////////// Von uns auskommentiert /////////////////////////
      
    Serial.print("->");
      Serial.print(anzahlEinfluege);
      Serial.print(", <-");
      Serial.print(anzahlAusfluege);
      Serial.print(", $");
      Serial.println(Gesamtanzahl);
      EEPROM.put(EEPROMAddr, Gesamtanzahl);

    } else if (erkennungsZustand == ausS1hS2l) {
      erkennungsZustand = auszS1hS2h;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();  // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == auszS1lS2l) {
      erkennungsZustand = ausS1lS2h;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();  // millis() sagt wir lange der Arduino läuft in Millisekunden
    }
  } else
  // Verarbeitung der fallenden Flanke
  {
    ///////////////////////// Von uns auskommentiert /////////////////////////
    // Serial.println("Eingang 2 fallende Flanke erkannt");
    ///////////////////////// Von uns auskommentiert /////////////////////////
    
    // Hier fragen wir für alle möglichen Zustände ab, was passieren soll, wenn am Eingang 2 eine fallende Flanke auftaucht.
    if (erkennungsZustand == einS1lS2h) {
      erkennungsZustand = einzS1lS2l;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();  // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == einzS1hS2h) {
      erkennungsZustand = einS1hS2l;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();  // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == grund) {
      erkennungsZustand = ausS1hS2l;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();                 // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == auszS1hS2h)  // Fehler-Übergang zurück zum vorherigen Zustand
    {
      erkennungsZustand = ausS1hS2l;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();                // millis() sagt wir lange der Arduino läuft in Millisekunden
    } else if (erkennungsZustand == ausS1lS2h)  // Fehler-Übergang zurück zum vorherigen Zustand
    {
      erkennungsZustand = auszS1lS2l;
      // Das ist ein Übergang in den Zwischenzustand, von dem aus wir wieder bei Timeout in den Grundzustand gehen
      // 1.: Zeitpunkt des Übergangs merken
      stateEntryTime = millis();  // millis() sagt wir lange der Arduino läuft in Millisekunden
    }
  }
}


//Programm void setup wird einmalig bei Start des Programms durchgeführt
void setup() {

  Serial.begin(9600);

  pinMode(Unterbrechungen, INPUT);
  pinMode(Unterbrechungenzwei, INPUT);
  pinMode(digitalAus1, OUTPUT);
  pinMode(digitalAus2, OUTPUT);
  digitalWrite(digitalAus1, HIGH);
  digitalWrite(digitalAus2, HIGH);

  attachInterrupt(digitalPinToInterrupt(Unterbrechungen), handleInterrupt1, CHANGE);
  // In unserem Zustandsdiagramm müssen wir jedoch sowohl
  // auf fallende als auch auf steigende Flanken
  // reagieren. Leider kann man einem Pin nur eine
  // Interrupt Funktion zuweisen, die muss also sowohl
  // auf steigende als auch auf fallende Flanken reagieren
  // also auf jede Veränderung.
  // In der Funktion müssen wir dann herausfinden, ob sie auf
  // eine steigende oder fallende Flanke reagiert hat.


  attachInterrupt(digitalPinToInterrupt(Unterbrechungenzwei), handleInterrupt2, CHANGE);

  pinMode(13, OUTPUT);  // der digitale Ausgang 13 steuert "nur" die LED auf dem
                        // Arduino an. Damit können wir Aktivität auf dem
                        // Arduino zeigen, im aktuellen Programm geben wir
                        // kein Signal auf dem digitalen Ausgang 13 aus.
                        // Prinzipiell sind Ein- / Ausgänge, die nur mit einer
                        // Zahl bezeichnet sind immer digitale Ein- / Ausgänge
                        // während die analogen Eingänge immer 'Ax' heißen
                        // wobei x eine Zahl ist (0 bis 7 wenn ich den Uno richtig
                        // in Erinnerung habe.

  // definieren, dass das System sich im Grundzustand befindet
  erkennungsZustand = grund;
  // Ein- und Ausfluege initialisieren
  anzahlEinfluege = 0;
  anzahlAusfluege = 0;

  // possibly reset EEPROM if A4 has a value > 0
  if (analogRead(A4) > 5)  // just to be sure...
    EEPROM.put(EEPROMAddr, (unsigned int)0);

  // warten solange Reset button gedrückt iwt.
  while (analogRead(A4) > 5) {
    ///////////////////////// Von uns auskommentiert /////////////////////////
    // Serial.println("Resetting EEPROM...");
    ///////////////////////// Von uns auskommentiert /////////////////////////
    delay(500);
  }

  // Anzahl der im Turm befindlichen Fledermäuse beim Start des Programms initialisieren
  Gesamtanzahl = 0;
  EEPROM.get(EEPROMAddr, Gesamtanzahl);
  ///////////////////////// Von uns auskommentiert /////////////////////////
  // Serial.println("Programm gestartet.");
  // Serial.print("Im Turm befindliche Fledermaeuse: ");
  
  Serial.println(Gesamtanzahl);

  // wir sind in keinem Zwischenzustand
  stateEntryTime = 0;

  previousSerialWriteTime = millis();  // das "erste" Mal die Fledermauszahl auf die Serielle Schnittstelle "geschrieben"
}

//Programm void loop wird immer wieder regelmäßig abgefragt
void loop() {
  // Dieser Teil liest die analogen Eingänge von den Lichtschranken ein und setzt die digitalen Ausgänge, die
  // die Interrupts auslösen
  analog0Voltage = readAnalogVoltage(A0);

  if (analog0Voltage < 0.05) {
    // Wenn auf dem digitalen Ausgang ein LOW-Signal zu sehen ist, haben wir eine Unterbrechung
    // das bedeutet eine fallende Flanke in der Interrupt-Funktion
    digitalWrite(digitalAus1, LOW);
  } else {
    digitalWrite(digitalAus1, HIGH);
  }

  //Ab hier wird die selbe Abfrage dann für A1 durchgeführt.
  analog1Voltage = readAnalogVoltage(A1);

  if (analog1Voltage < 0.05) {
    digitalWrite(digitalAus2, LOW);
  } else {
    digitalWrite(digitalAus2, HIGH);
  }


  // ab hier kümmern wir uns um mögliche Timeouts
  if (stateEntryTime > 0)  // nur wenn wir in einem relevanten Zustand sind:
  {
    // Zuerst: Berechnen, wie lange wir schon in dem Zustand sind.
    // aktuelle Zeit holen:
    currentTime = millis();
    // berechnen, wie lange wir im aktuellen Zustand sind:
    stateDuration = currentTime - stateEntryTime;

    switch (erkennungsZustand)  // Mechanismus, der für einzelne Werte in der Variablen bestimmte Aktionen ausführt
    {
      case einS1lS2h:
        // Von hier aus würden wir bei Timeout in den Fehlerzustand gehen.
        // Serial.println("Zustand Einflug 1 low 2 high");
        if (stateDuration > maxStateDuration2Error) {
          // wir gehen in den Grundzustand zurück wenn wir zu lange in dem Zustand bleiben
          erkennungsZustand = fehler;
          stateEntryTime = 0;
          ///////////////////////// Von uns auskommentiert /////////////////////////
          // Serial.println("Uebergang in Fehlerzustand nach Timeout...");
          ///////////////////////// Von uns auskommentiert /////////////////////////
        }
        break;
      case einzS1hS2h:
        // Von hier aus würden wir bei Timeout in den Grundzustand gehen
        if (stateDuration > maxStateDuration2Base) {
          // wir gehen in den Grundzustand zurück wenn wir zu lange in dem Zustand bleiben
          erkennungsZustand = grund;
          stateEntryTime = 0;
          ///////////////////////// Von uns auskommentiert /////////////////////////
          // Serial.println("Uebergang in Grundzustand nach Timeout...");
          ///////////////////////// Von uns auskommentiert /////////////////////////
        }
        break;
      case einzS1lS2l:
        // Von hier aus würden wir bei Timeout in den Fehlerzustand gehen.
        // Serial.println("Zustand Einflug 1 low 2 low");
        if (stateDuration > maxStateDuration2Error) {
          // wir gehen in den Grundzustand zurück wenn wir zu lange in dem Zustand bleiben
          erkennungsZustand = fehler;
          stateEntryTime = 0;
          ///////////////////////// Von uns auskommentiert /////////////////////////
          // Serial.println("Uebergang in Fehlerzustand nach Timeout...");
          ///////////////////////// Von uns auskommentiert /////////////////////////
        }
        break;
      case einS1hS2l:
        // Von hier aus würden wir bei Timeout in den Fehlerzustand gehen.
        // Serial.println("Zustand Einflug 1 high 2 low");
        if (stateDuration > maxStateDuration2Error) {
          // wir gehen in den Grundzustand zurück wenn wir zu lange in dem Zustand bleiben
          erkennungsZustand = fehler;
          stateEntryTime = 0;
          ///////////////////////// Von uns auskommentiert /////////////////////////
          // Serial.println("Uebergang in Fehlerzustand nach Timeout...");
          ///////////////////////// Von uns auskommentiert /////////////////////////
        }
        break;
      case ausS1hS2l:
        // Von hier aus würden wir bei Timeout in den Fehlerzustand gehen.
        // Serial.println("Zustand Ausflug 1 high 2 low");
        if (stateDuration > maxStateDuration2Error) {
          // wir gehen in den Grundzustand zurück wenn wir zu lange in dem Zustand bleiben
          erkennungsZustand = fehler;
          stateEntryTime = 0;
          ///////////////////////// Von uns auskommentiert /////////////////////////
          // Serial.println("Uebergang in Fehlerzustand nach Timeout...");
          ///////////////////////// Von uns auskommentiert /////////////////////////
        }
        break;
      case auszS1hS2h:
        // Von hier aus würden wir bei Timeout in den Grundzustand gehen
        if (stateDuration > maxStateDuration2Base) {
          // wir gehen in den Grundzustand zurück wenn wir zu lange in dem Zustand bleiben
          erkennungsZustand = grund;
          stateEntryTime = 0;
          ///////////////////////// Von uns auskommentiert /////////////////////////
          // Serial.println("Uebergang in Grundzustand nach Timeout...");
          ///////////////////////// Von uns auskommentiert /////////////////////////
        }
        break;
      case auszS1lS2l:
        // Von hier aus würden wir bei Timeout in den Fehlerzustand gehen.
        // Serial.println("Zustand Ausflug 1 low 2 low");
        if (stateDuration > maxStateDuration2Error) {
          // wir gehen in den Grundzustand zurück wenn wir zu lange in dem Zustand bleiben
          erkennungsZustand = fehler;
          stateEntryTime = 0;
          ///////////////////////// Von uns auskommentiert /////////////////////////
          // Serial.println("Uebergang in Fehlerzustand nach Timeout...");
          ///////////////////////// Von uns auskommentiert /////////////////////////
        }
        break;
      case ausS1lS2h:
        // Von hier aus würden wir bei Timeout in den Fehlerzustand gehen.
        // Serial.println("Zustand Ausflug 1 low 2 high");
        if (stateDuration > maxStateDuration2Error) {
          // wir gehen in den Grundzustand zurück wenn wir zu lange in dem Zustand bleiben
          erkennungsZustand = fehler;
          stateEntryTime = 0;
          ///////////////////////// Von uns auskommentiert /////////////////////////
          // Serial.println("Uebergang in Fehlerzustand nach Timeout...");
          ///////////////////////// Von uns auskommentiert /////////////////////////
        }
        break;
        // Serial.println("Hier sollten wir nicht sein...");
    }
  }  // Ende if (stateEntryTime > 0)...

  // regelmäßig Gesamtanzahl schreiben
  serialWriteTime = millis();
  if ((serialWriteTime < previousSerialWriteTime) || (serialWriteTime - previousSerialWriteTime > 30000)) {
    ///////////////////////// Von uns auskommentiert /////////////////////////
    // Serial.print("Im Turm befindliche Fledermaeuse: ");
    ///////////////////////// Von uns auskommentiert /////////////////////////

   Serial.print("->");
      Serial.print(anzahlEinfluege);
      Serial.print(", <-");
      Serial.print(anzahlAusfluege);
      Serial.print(", $");
      Serial.println(Gesamtanzahl);
    previousSerialWriteTime = millis();
  }
  // delay(5); // 5 ms warten

  checkSerialInput();
  if(newData)
  {
     Serial.print("Extracted value: ");
     Serial.println(extractedValue);
     Gesamtanzahl = extractedValue; 
     anzahlEinfluege = 0 ; 
     anzahlAusfluege = 0 ; 
     //EEPROM.update(EEPROMAddr, extractedValue);
     newData = false;  // Reset the flag
  }
}


static int Zaehler = 0;

// ++x = Wert x um 1 erhöht und gibt den neuen x Wert aus // x++ = Wert x um 1 erhöht und gibt den alten x Wert aus (bei -- wird x um 1 erniedrigt)


