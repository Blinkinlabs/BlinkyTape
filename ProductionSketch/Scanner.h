#ifndef SCANNER_H
#define SCANNER_H

#include <FastLED.h>
#include "BlinkyTape.h"

class Scanner : public Pattern {
  private:
    uint8_t scanWidth;
    
  public:
    Scanner(uint8_t newScanWidth);
    void reset() {};
    void draw(CRGB * leds);
};

#endif
