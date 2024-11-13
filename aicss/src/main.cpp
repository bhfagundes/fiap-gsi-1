#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

// Definição dos pinos
const int LDR_PIN = 34;        // Sensor de luz
const int TRIG_PIN = 26;       // Sensor ultrassônico
const int ECHO_PIN = 27;       // Sensor ultrassônico
const int LED_INTERNO = 2;     // LED interno
const int LED_EXTERNO = 4;     // LED externo

// Variáveis globais
int valorLuz;
long distancia;

void setup() {
  Serial.begin(115200);
  
  pinMode(LDR_PIN, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_INTERNO, OUTPUT);
  pinMode(LED_EXTERNO, OUTPUT);
  
  Serial.println("Sistema Iniciado!");
}

void medirDistancia() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  long duracao = pulseIn(ECHO_PIN, HIGH);
  distancia = duracao * 0.034 / 2;
}

// Envio de dados para servidor Python
void enviarDados() {
  if(WiFi.status() == WL_CONNECTED) {
    String dados = "{\"luz\":" + String(valorLuz) + 
                  ",\"distancia\":" + String(distancia) + 
                  ",\"consumo_interno\":" + String(digitalRead(LED_INTERNO)) +
                  ",\"consumo_externo\":" + String(digitalRead(LED_EXTERNO)) + "}";
    
    // Enviar para servidor Python
    HTTPClient http;
    http.begin("http://localhost:5000/dados");
    http.POST(dados);
  }
}

void loop() {
  // Leitura do sensor de luz
  valorLuz = analogRead(LDR_PIN);
  
  // Medição de distância
  medirDistancia();
  
  // Controle da iluminação externa
  if (valorLuz < 2000) { // Ambiente escuro
    digitalWrite(LED_EXTERNO, HIGH);
  } else {
    digitalWrite(LED_EXTERNO, LOW);
  }
  
  // Controle da iluminação interna
  if (distancia < 100 && valorLuz < 2000) { // Pessoa próxima e ambiente escuro
    digitalWrite(LED_INTERNO, HIGH);
  } else {
    digitalWrite(LED_INTERNO, LOW);
  }
  
  // Envio dos dados para serial
  Serial.print("Luz: ");
  Serial.print(valorLuz);
  Serial.print(" | Distância: ");
  Serial.print(distancia);
  Serial.println(" cm");
  
  delay(1000);
}