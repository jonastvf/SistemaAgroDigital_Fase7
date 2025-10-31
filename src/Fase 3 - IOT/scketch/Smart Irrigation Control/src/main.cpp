#include <Arduino.h>

/*************************************************
 * Projeto: FarmTech Solutions - Fase 3 CAP 01   *
 * Sistema de Irrigação com Sensores Integrados  *
 *                                               *
 * Autor: Raphael da Silva                       *
 * RM: 561452                                    *
 * Turma: 1TIAOA                                 *
 * GitHub: https://github.com/Phaeld/1TIAOA-CAP-01
 *                                               *
 * Descrição:                                    *
 * Sistema físico simulado que coleta dados de   *
 * sensores de umidade, nutrientes (K e P) e pH, *
 * acionando uma bomba de irrigação conforme os  *
 * valores. Os dados serão armazenados em um     *
 * banco de dados SQL com fins de análise.       *
 *************************************************/


#include <DHT.h>


#define DHTPIN 15       
#define DHTTYPE DHT22  


DHT dht(DHTPIN, DHTTYPE);  

#define PH_SENSOR 34
#define POTASSIUM_SENSOR 12
#define PHOSPHORUS_SENSOR 14
#define PUMP 16

// declare functions
void logo();
void humidityValue();
void sensorsValue();
void irrigationControl();

void setup() {

pinMode(PH_SENSOR, INPUT);
pinMode(POTASSIUM_SENSOR, INPUT);
pinMode(PHOSPHORUS_SENSOR, INPUT);
pinMode(PUMP, OUTPUT);

Serial.begin(9600);  
dht.begin();  
logo();       

}

void loop() {

humidityValue();
sensorsValue();
irrigationControl();

// Separate the readings
Serial.println("==============================");
delay(2000);

}

// Function reads the humidity value from the DHT sensor
void humidityValue(){
  
float humidity = dht.readHumidity();  

 
if (isnan(humidity)) {
  Serial.println("Falha na leitura da umidade do DHT22");
  return;
}
Serial.println();
Serial.print("Umidade: ");
Serial.print(humidity);
Serial.println(" %");

}

// Function reads the sensor pH, phosphorus and potassium
void sensorsValue(){

  // Read the pH sensor value and map it to a pH value
float phValue= analogRead(PH_SENSOR);
float phState = map(phValue, 0, 4095, 0, 14);

Serial.print("Sensor pH:" );
Serial.print(phState);
Serial.println(" %");

int phosphorusState = digitalRead(PHOSPHORUS_SENSOR); 
String phosphorus_value;
if (phosphorusState == 1){
  phosphorus_value = "ALTO NÍVEL FOSFORO";
}else{
  phosphorus_value = "BAIXO NÍVEL FOSFORO";
}

Serial.print("Sensor Fosforo (P):" );
Serial.print(phosphorus_value);
Serial.println(" ");

int potassiumState = digitalRead(POTASSIUM_SENSOR); 
String potassium_value;
if (potassiumState == 1){
  potassium_value = "ALTO NÍVEL POTASSIO";
}
else{
  potassium_value = "BAIXO NÍVEL POTASSIO";
}

Serial.print("Sensor Potassio (K):" );
Serial.print(potassium_value);
Serial.println(" ");

}

// The function controls the irrigation system via the DHT sensor + relay
void irrigationControl(){

const int humidity_threshold = 50;
float humidity = dht.readHumidity();
  
if (humidity < humidity_threshold){
  digitalWrite(PUMP, HIGH);
  delay(100);
  Serial.println("Bomba assionada!");
}
else{
  digitalWrite(PUMP, LOW);
  delay(100);
  Serial.println("Bomba desligada!"); 
  }
}

// Function resposable for printing the logo
void logo() {

String logo_pt1 = "___________                        _________      .__          __  .__";
String logo_pt2 = "\\_   _____/____ _______  _____    /   _____/ ____ |  |  __ ___/  |_|__| ____   ____   ______";
String logo_pt3 = "|    __) \\__  \\\\_  __ \\/     \\   \\_____  \\ /  _ \\|  | |  |  \\   __\\  |/  _ \\ /    \\ /  ___/";
String logo_pt4 = "|     \\   / __ \\|  | \\/  Y Y  \\  /        (  <_> )  |_|  |  /|  | |  (  <_> )   |  \\\\___ \\ ";
String logo_pt5 = " \\___  /  (____  /__|  |__|_|  / /_______  /\\____/|____/____/ |__| |__|\\____/|___|  /____  >";
String logo_pt6 = "     \\/        \\/            \\/          \\/                                       \\/     \\/";

Serial.println(logo_pt1);
Serial.println(logo_pt2);
Serial.println(logo_pt3);
Serial.println(logo_pt4);
Serial.println(logo_pt5);
Serial.println(logo_pt6);
Serial.println("");
Serial.println("Terminal de Contole dos Sensores");
Serial.println("");
Serial.println("==============================");

}