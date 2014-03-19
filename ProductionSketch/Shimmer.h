#ifndef SHIMMER_H
#define SHIMMER_H

#include <FastLED.h>
#include "BlinkyTape.h"

class Shimmer : public Pattern {
  private:
    //Shimmer variables
    int max_value[LED_COUNT];
    uint8_t direction[LED_COUNT];
    float value[LED_COUNT];
    float death[LED_COUNT];
    int step_size;
    int ledMax;

    int color_temp;
    float color_temp_factor_r;
    float color_temp_factor_g;
    float color_temp_factor_b;
    
  public:
    Shimmer();
    void reset();
    void draw(CRGB * leds);
    
    void SetColorTemperature(uint8_t newColorTemperature);
};


#endif
