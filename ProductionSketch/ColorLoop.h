#ifndef COLOR_LOOP_H
#define COLOR_LOOP_H

#include <FastLED.h>
#include "BlinkyTape.h"

class ColorLoop : public Pattern {
  private:
    float rBal;
    float gBal;
    float bBal;
    
  public:
    ColorLoop(float newRBal, float newGBal, float newBBal);
    void reset() {};
    void draw(CRGB * leds);
};

#endif
