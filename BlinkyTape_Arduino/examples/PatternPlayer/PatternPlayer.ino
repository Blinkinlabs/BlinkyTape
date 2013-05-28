#include <Adafruit_NeoPixel.h>

#include <Animation.h>
#include "pov.h"

#define LED_COUNT 60
#define THRESHOLD 1

Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_COUNT, 5, NEO_GRB + NEO_KHZ800);

uint8_t pixel_index;
long last_time;

void setup()
{  
  Serial.begin(57600);

  strip.begin();
  strip.show();
  last_time = millis();
}

void serialLoop() {

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
          pixel_index = 0;
          break;
        }

        if (x == 2) {   // If we received three serial bytes
          strip.setPixelColor(pixel_index, strip.Color(buffer[0], buffer[1], buffer[2]));
          pixel_index++;
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
  
  pov.draw(strip);
  delay(20);
}

