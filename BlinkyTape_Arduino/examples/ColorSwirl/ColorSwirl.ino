#include <FastSPI_LED2.h>
#include <Animation.h>

#define LED_COUNT 60
struct CRGB leds[LED_COUNT];

#define PIN_BUTTON 10
#define PIN_IO_A   7
#define PIN_IO_B   11
#define PIN_SIGNAL 13
#define PIN_INPUT  10

long last_time;

void setup()
{  
  Serial.begin(57600);
  
  LEDS.addLeds<WS2811, PIN_SIGNAL, GRB>(leds, LED_COUNT);
  LEDS.showColor(CRGB(0, 0, 0));
  LEDS.setBrightness(230); // 90% brightness
  LEDS.show();
   
  last_time = millis();
}


void color_loop() {  
  static uint8_t i = 0;
  static int j = 0;
  static int f = 0;
  static int k = 0;
  static int count;

  static int pixelIndex;
  
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    leds[i].r = 64*(1+sin(i/2.0 + j/4.0       ));
    leds[i].g = 64*(1+sin(i/1.0 + f/9.0  + 2.1));
    leds[i].b = 64*(1+sin(i/3.0 + k/14.0 + 4.2));
    
    if ((millis() - last_time > 15) && pixelIndex <= LED_COUNT + 1) {
      last_time = millis();
      count = LED_COUNT - pixelIndex;
      pixelIndex++; 
    }
    
    // why is this per LED?
    for (int x = count; x >= 0; x--) {
      leds[x] = CRGB(0, 0, 0);
    }
    
  }
  LEDS.show();
  
  j = j + 1;
  f = f + 1;
  k = k + 2;
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
          LEDS.show();
          pixelIndex = 0;
          break;
        }

        if (x == 2) {   // If we received three serial bytes
          leds[pixelIndex] = CRGB(buffer[0], buffer[1], buffer[2]);
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

