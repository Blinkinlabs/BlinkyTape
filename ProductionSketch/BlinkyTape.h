#ifndef BLINKY_TAPE_H
#define BLINKY_TAPE_H

#define LED_COUNT 60

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
