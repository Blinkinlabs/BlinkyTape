#include <Adafruit_NeoPixel.h>
#include <Animation.h>

#define LED_COUNT 60
#define THRESHOLD 1

Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_COUNT, 5, NEO_GRB + NEO_KHZ800);

long last_time;

void setup()
{  
  Serial.begin(57600);

  strip.begin();
  strip.show();
  last_time = millis();
}


void color_loop() {  
  static uint8_t i = 0;
  static int j = 0;
  static int f = 0;
  static int k = 0;
  static int count;

  static int pixelIndex;

  float brightness = .9;
  
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    uint8_t red =   64*(1+sin(i/2.0 + j/4.0       ))*brightness;
    uint8_t green = 64*(1+sin(i/1.0 + f/9.0  + 2.1))*brightness;
    uint8_t blue =  64*(1+sin(i/3.0 + k/14.0 + 4.2))*brightness;
    
    uint32_t pix = green;
    pix = (pix << 8) | red;
    pix = (pix << 8) | blue;
    
    strip.setPixelColor(i, pix);
    
    if ((millis() - last_time > 15) && pixelIndex <= LED_COUNT + 1) {
      last_time = millis();
      count = LED_COUNT - pixelIndex;
      pixelIndex++; 
    }
    
    for (int x = count; x >= 0; x--) {
      strip.setPixelColor(x, strip.Color(0,0,0));
    }
    
  }
  strip.show();
  
  j = j + random(1,2);
  f = f + random(1,2);
  k = k + random(1,2);
}

void serialLoop() {
  static int pixelIndex;

  while(true) {

    if(Serial.available() > 2) {

      uint8_t buffer[3]; // Buffer to store three incoming bytes used to compile a single LED color

      for (uint8_t x=0; x<3; x++) { // Read three incoming bytes
        uint8_t c = Serial.read();
        
        if (c < 255) {
          buffer[x] = c; // Using 255 as a latch semaphore
        }
        else {
          strip.show();
          pixelIndex = 0;
          break;
        }

        if (x == 2) {   // If we received three serial bytes
          strip.setPixelColor(pixelIndex, strip.Color(buffer[0], buffer[1], buffer[2]));
          pixelIndex++;
        }
      }
    }
  }
}

void loop()
{
  // If'n we get some data, switch to passthrough mode
  if(Serial.available() > 0) {
    serialLoop();
  }
  
  color_loop();
}

