#define LED_COUNT 32

uint32_t led_array[LED_COUNT];

void setup()
{
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

void send_pixel_32(uint32_t c) {
  
  send_single_byte((c >> 16) | 0x80);
  send_single_byte((c >> 8) | 0x80);
  send_single_byte((c >> 0) | 0x80);
    
}

int j = 0;
int f = 0;
int k = 0;

void color_loop() {
  float brightness = random(100,100)/100.0;
  
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    uint8_t red =   64*(1+sin(i/2.0 + j/4.0       ))*brightness;
    uint8_t green = 64*(1+sin(i/1.0 + f/9.0  + 2.1))*brightness;
    uint8_t blue =  64*(1+sin(i/3.0 + k/14.0 + 4.2))*brightness;
    
    uint32_t pix = green;
    pix = (pix << 8) | red;
    pix = (pix << 8) | blue;
    
    led_array[i] = pix;
  }
  
  j = j + random(1,2);
  f = f + random(1,2);
  k = k + random(1,2);
}

void loop()
{
 
  color_loop();
  
  for (int x = 0; x < LED_COUNT; x++) {
    send_pixel_32(led_array[x]); 
  }
  
  send_single_byte(0x00);
 
}
