static int LED_COUNT = 32;

void setup()
{
  Serial.begin(57600);
  
  bitClear(PORTB, PORTB1);
  bitClear(PORTB, PORTB2);
  
  bitSet(DDRB, DDB1);
  bitSet(DDRB, DDB2);
}

// For blinkyboards
void send_single_byte(uint8_t c)
{
  for(uint8_t i = 0; i < 8; i++) {
    // PB1 is clock, PB2 is data
    if(c >> (7 - i) & 0x01) {
      bitSet(PORTB, PORTB2);
    }
    else {
      bitClear(PORTB, PORTB2);      
    }
    
    bitSet(PORTB, PORTB1);
    bitClear(PORTB, PORTB1);
  }
}

void send_pixel(uint8_t red, uint8_t green, uint8_t blue) {
  send_single_byte(0x80 | red);
  send_single_byte(0x80 | green);
  send_single_byte(0x80 | blue);
}

uint8_t i = 0;
int j = 0;
int f = 0;
int k = 0;

void loop()
{
  // If'n we get some data, switch to passthrough mode
  if(Serial.available() > 0) {
    while(true) {
      if(Serial.available() > 0) {
        char c = Serial.read();
        send_single_byte(c);
      }
    }
  }
  
  float brightness = random(100,100)/100.0;
  
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    uint8_t red =   64*(1+sin(i/2.0 + j/4.0       ))*brightness;
    uint8_t green = 64*(1+sin(i/1.0 + f/9.0  + 2.1))*brightness;
    uint8_t blue =  64*(1+sin(i/3.0 + k/14.0 + 4.2))*brightness;
    
    send_pixel(red, green, blue);
  }

  j = j + random(1,2);
  f = f + random(1,2);
  k = k + random(1,2);
  
  send_single_byte(0x00);
}



