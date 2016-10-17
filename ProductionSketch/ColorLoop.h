#ifndef COLOR_LOOP_H
#define COLOR_LOOP_H

#include <FastLED.h>
#include "BlinkyTape.h"

class ColorLoop : public Pattern {
  private:
    float rBal;
    float gBal;
    float bBal;
    
    int j;
    int f;
    int k;
    int count;
    
  public:
    ColorLoop(float newRBal, float newGBal, float newBBal);
    void reset();
    void draw(CRGB * leds);
};

#endif
