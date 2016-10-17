#ifndef SHIMMER_H
#define SHIMMER_H

#include <FastLED.h>
#include "BlinkyTape.h"

class Shimmer : public Pattern {
  private:
    //Shimmer variables
    uint8_t maxValue[LED_COUNT];
    uint8_t direction[LED_COUNT];
    
    // TODO: Loss of precision here affects output.
    float value[LED_COUNT];
    float death[LED_COUNT];
//    uint8_t value[LED_COUNT];
//    uint8_t death[LED_COUNT];
    
    uint8_t stepSize;
    uint8_t ledMax;

    uint8_t colorTemperature;
    float color_temp_factor_r;
    float color_temp_factor_g;
    float color_temp_factor_b;
    
  public:
    Shimmer(uint8_t newColorTemperature);
    void reset();
    void draw(CRGB * leds);
    
    void SetColorTemperature(uint8_t newColorTemperature);
};


#endif
