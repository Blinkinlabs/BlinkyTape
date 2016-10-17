#include "Flashlight.h"
#include "BlinkyTape.h"

#include <Arduino.h>

Flashlight::Flashlight(CRGB newColor) :
  color(newColor) {
  }

void Flashlight::draw(CRGB* leds) {  
  for (uint16_t i = 0; i < LED_COUNT; i++) {
    leds[i] = color;
  }
}
