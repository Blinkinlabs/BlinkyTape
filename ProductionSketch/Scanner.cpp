#include "Scanner.h"
#include "BlinkyTape.h"

#include <Arduino.h>

Scanner::Scanner(uint16_t newScanWidth, CRGB newColor) :
  scanWidth(newScanWidth),
  color(newColor) {
  }

void Scanner::reset() {
  position = 2;
  direction = 1;
}

void Scanner::draw(CRGB* leds) {  
  for (uint16_t i = 0; i < LED_COUNT; i++) {
    if((i >= position) && (i < position + scanWidth)) {
      leds[i] = color;
    }
    else {
      leds[i] = CRGB(0);
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
  
  delay(30);  // TODO: Don't place me here
}
