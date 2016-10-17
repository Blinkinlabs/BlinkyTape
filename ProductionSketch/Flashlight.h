#ifndef FLASHLIGHT_H
#define FLASHLIGHT_H

#include <FastLED.h>
#include "BlinkyTape.h"

class Flashlight : public Pattern {
  private:
    CRGB color;
    
  public:
    Flashlight(CRGB newColor);
    void reset() {};
    void draw(CRGB * leds);
};

#endif
