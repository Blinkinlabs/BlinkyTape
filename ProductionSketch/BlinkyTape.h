#ifndef BLINKY_TAPE_H
#define BLINKY_TAPE_H

#include <FastLED.h>

#define LED_COUNT 128    // Number of LEDs connected to the board. This is also the maximum number of LEDs that can be controlled via serial

#define LED_OUT       13
#define BUTTON_IN     10
#define ANALOG_INPUT  A9
#define EXTRA_PIN_A    7
#define EXTRA_PIN_B   11

class Pattern {
  public:
    virtual void draw(CRGB * leds);
    virtual void reset();
};

#endif
