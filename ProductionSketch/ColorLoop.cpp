#include "ColorLoop.h"
#include "BlinkyTape.h"

#include <Arduino.h>


ColorLoop::ColorLoop(float newRBal, float newGBal, float newBBal) :
  rBal(newRBal),
  gBal(newGBal),
  bBal(newBBal) {
}

void ColorLoop::reset() {
  j = 0;
  f = 0;
  k = 0;
}

void ColorLoop::draw(CRGB* leds) {
  for (uint16_t i = 0; i < LED_COUNT; i++) {
    leds[i].r = 64*(1+sin(i/2.0 + j/4.0  )) * rBal;
    leds[i].g = 64*(1+sin(i/1.0 + f/9.0 + 2.1)) * gBal;
    leds[i].b = 64*(1+sin(i/3.0 + k/14.0 + 4.2)) * bBal;
  }
  
  j = j + 1;
  f = f + 1;
  k = k + 2;
}
