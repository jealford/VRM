int seriesResistor = 1130;  
int thermistorPin = A0; 
int beta = 3636;
int val = 0;
int soilPin = A1;
int soilPower = 7;

void setup(void) {
  Serial.begin(9600);
  pinMode(soilPower, OUTPUT);
  digitalWrite(soilPower, LOW);
}
     
void loop(void) {
  float thermR;
  float temp;
  thermR = analogRead(thermistorPin);
  thermR = (1023 / thermR)  - 1;    
  thermR = seriesResistor / thermR; 
  temp = beta / log(thermR / (1000*exp(-beta/298.15)));
  temp = temp - 263.15;
  Serial.print("Soil ");  
  Serial.println(readSoil());
  Serial.print("Temp "); 
  Serial.println(temp);    
  delay(1000);
 }

 int readSoil()
{
  digitalWrite(soilPower, HIGH);
  delay(10);
  val = analogRead(soilPin);
  digitalWrite(soilPower, LOW);
  return val;
}
