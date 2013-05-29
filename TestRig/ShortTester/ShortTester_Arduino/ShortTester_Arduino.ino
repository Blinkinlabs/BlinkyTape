// Simple I/O controller for use with the 

// Mode averaging code from here:
// http://www.elcojacobs.com/eleminating-noise-from-sensor-readings-on-arduino-with-digital-filtering/
#define NUM_READS 100
float readTemperature(int sensorpin){
   // read multiple values and sort them to take the mode
   int sortedValues[NUM_READS];
   for(int i=0;i<NUM_READS;i++){
     int value = analogRead(sensorpin);
     int j;
     if(value<sortedValues[0] || i==0){
        j=0; //insert at first position
     }
     else{
       for(j=1;j<i;j++){
          if(sortedValues[j-1]<=value && sortedValues[j]>=value){
            // j is insert position
            break;
          }
       }
     }
     for(int k=i;k>j;k--){
       // move all values higher than current reading up one position
       sortedValues[k]=sortedValues[k-1];
     }
     sortedValues[j]=value; //insert current reading
   }
   //return scaled mode of 10 values
   float returnval = 0;
   for(int i=NUM_READS/2-5;i<(NUM_READS/2+5);i++){
     returnval +=sortedValues[i];
   }
   returnval = returnval/10;
   return returnval*1100/1023;
}

void setup() {
  Serial.begin(9600);
  analogReference(INTERNAL);
}

// All commands are two bytes: [command][channel]
// m: measure an analog channel
// r: read a digital channel
// o: set a digital channel to output
// i: set a digital channel to input without a pullup
// p: set a digital channel to input with a pullup
// h: set a digital channel output high
// l: set a digital channel output low

void loop() {
  if(Serial.available() > 1) {
    char command = Serial.read();
    char channel = Serial.read();
    
    switch(command) {
      case 'm':
        Serial.println(readTemperature(channel));
        break;
      case 'r':
        Serial.println(digitalRead(channel));
        break;
      case 'o':
        pinMode(channel, OUTPUT);
        break;
      case 'i':
        pinMode(channel, INPUT);
        break;
      case 'p':
        pinMode(channel, INPUT_PULLUP);
        break;
      case 'h':
        digitalWrite(channel, HIGH);
        break;
      case 'l':
        digitalWrite(channel, LOW);
        break;
    }
  }
}
