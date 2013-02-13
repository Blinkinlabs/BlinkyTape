static int LED_COUNT = 32;

void setup()
{
  Serial.begin(115200);
  
  DDRB = 0xFF;
  DDRD = 0xFF;
}

//// For teensy prototypes
//void send_single_byte(uint8_t c)
//{
//  // D5 is clock, D4 is data
//  for(uint8_t i = 0; i < 8; i++) {
//    PORTD = (((c >> (7 - i)) & 0x01) << 4);
//    PORTD = (((c >> (7 - i)) & 0x01) << 4) | 0x20;
//  }
//}

// For blinkyboards
void send_single_byte(uint8_t c)
{
  // D5 is clock, D4 is data
  for(uint8_t i = 0; i < 8; i++) {
    PORTB = (((c >> (7 - i)) & 0x01) << 2);
    PORTB = (((c >> (7 - i)) & 0x01) << 2) | 0x02;
  }
}

void send_pixel(uint8_t red, uint8_t green, uint8_t blue) {
  send_single_byte(0x80 | red);
  send_single_byte(0x80 | green);
  send_single_byte(0x80 | blue);
}

int j = 0;
int f = 0;
int k = 0;


uint8_t i = 0;
void loop()
{
  // If'n we get some data, switch to passthrough mode
  if(Serial.available()) {
    while(true) {
      send_single_byte(Serial.read());
      while(!Serial.available()) {}
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

//  j = k;
//  for (uint8_t i = 0; i < LED_COUNT; i++) {
//    if (j == 0) {
//      send_pixel(127,64,0);
//    }
//    else if(j == 1) {
//      send_pixel(64,127,0);
//    }
//    else if(j == 2) {
//      send_pixel(0,127,64);
//    }
//    else if(j == 3) {
//      send_pixel(0,64,127);
//    }
//    else if(j == 4) {
//      send_pixel(64,0,127);
//    }
//    else {
//      send_pixel(127,0,64);
//    }
//    
//    j = (j+1)%6;
//  }
//  k = (k+1)%6;
  
  send_single_byte(0x00);
 

}



