static int LED_COUNT = 32;

void setup()
{
  DDRB = 0xFF;
  DDRD = 0xFF;
}

void send_single_byte(uint8_t c)
{
  // D5 is clock, D4 is data
  for(uint8_t i = 0; i < 8; i++) {
    PORTD = (((c >> (7 - i)) & 0x01) << 4);
    PORTD = (((c >> (7 - i)) & 0x01) << 4) | 0x20;
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


void loop()
{
  for(uint8_t i = 0; i < 10; i++) {
//    send_pixel(0,0,0);
  }
  
  float brightness = random(100,100)/100.0;
  
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    uint8_t red =   64*(1+sin(i/2.0 + j/4.0       ))*brightness;
    uint8_t green = 64*(1+sin(i/1.0 + f/9.0  + 2.1))*brightness;
    uint8_t blue =  64*(1+sin(i/3.0 + k/14.0 + 4.2))*brightness;
    
    send_pixel(red, green, blue);
  }
  

  
  send_single_byte(0x00);
 
  j = j + random(1,2);
  f = f + random(1,2);
  k = k + random(1,2);
}



