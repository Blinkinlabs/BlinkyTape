#include "ColorLoop.h"
#include "BlinkyTape.h"

#include <Arduino.h>

float rBal = 1.0;
float gBal = 1.0;
float bBal = 1.0;

void setColorLoopColors(float newRBal, float newGBal, float newBBal) {
  rBal = newRBal;
  gBal = newGBal;
  bBal = newBBal;
}

void colorLoop(CRGB* leds) {  
  static uint8_t i = 0;
  static int j = 0;
  static int f = 0;
  static int k = 0;
  static int count;

  static int pixelIndex;
  
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    leds[i].r = 64*(1+sin(i/2.0 + j/4.0  )) * rBal;
    leds[i].g = 64*(1+sin(i/1.0 + f/9.0 + 2.1)) * gBal;
    leds[i].b = 64*(1+sin(i/3.0 + k/14.0 + 4.2)) * bBal;
    
//    if ((millis() - last_time > 15) && pixelIndex <= LED_COUNT + 1) {
//      last_time = millis();
//      count = LED_COUNT - pixelIndex;
//      pixelIndex++;
//    }
    
    // why is this per LED?
    for (int x = count; x >= 0; x--) {
      leds[x] = CRGB(0, 0, 0);
    }
    
  }
  
  j = j + 1;
  f = f + 1;
  k = k + 2;
}
