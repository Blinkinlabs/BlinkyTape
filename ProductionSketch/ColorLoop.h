#ifndef COLOR_LOOP_H
#define COLOR_LOOP_H

#include <FastLED.h>

extern void setColorLoopColors(float newRBal, float newGBal, float newBBal);
extern void colorLoop(CRGB * leds);

#endif
