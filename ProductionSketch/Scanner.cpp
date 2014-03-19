#include "Scanner.h"
#include "BlinkyTape.h"

#include <Arduino.h>

Scanner::Scanner(uint8_t newScanWidth) :
  scanWidth(newScanWidth) {
    
  }

void Scanner::draw(CRGB* leds) {  
  static uint8_t position = 2;
  static uint8_t direction = 0; // 0 is positive, 1 is negative

  for (uint8_t i = 0; i < LED_COUNT; i++) {
    if((i >= position) && (i < position + scanWidth)) {
      leds[i].r = 0;
      leds[i].g = 0;
      leds[i].b = 255;
    }
    else {
      leds[i].r = 0;
      leds[i].g = 0;
      leds[i].b = 0;
    }    
  }
  
  if(direction == 0) {
    position += 1;
    
  }
  else {
    position -= 1;
  }
  
  if(position > LED_COUNT - scanWidth) {
    direction = 1;
  }
  else if(position == 0) {
    direction = 0;
  }
  
  delay(30);
}
