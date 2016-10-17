#ifndef SCANNER_H
#define SCANNER_H

#include <FastLED.h>
#include "BlinkyTape.h"

class Scanner : public Pattern {
  private:
    uint16_t scanWidth;
    CRGB color;
    
    uint16_t position;
    uint8_t direction; // 0 is positive, 1 is negative
    
  public:
    Scanner(uint16_t newScanWidth, CRGB newColor);
    void reset();
    void draw(CRGB * leds);
};

#endif
