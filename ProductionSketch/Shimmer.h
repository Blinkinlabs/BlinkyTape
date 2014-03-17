#ifndef SHIMMER_H
#define SHIMMER_H

#include <FastLED.h>

extern void InitializeShimmer();
extern void SetColorTemperature(uint8_t newColorTemperature);
extern void Shimmer(CRGB* leds);

#endif
