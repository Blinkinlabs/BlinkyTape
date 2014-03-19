// This is the example sketch that gets loaded on every BlinkyTape during production!

#include <FastLED.h>
#include <Animation.h>

#include "BlinkyTape.h"
#include "ColorLoop.h"
#include "SerialLoop.h"
#include "Shimmer.h"
#include "Scanner.h"

struct CRGB leds[LED_COUNT];

#define BRIGHT_STEP_COUNT 5
uint8_t brightnesSteps[BRIGHT_STEP_COUNT] = {5,15,40,70,93};
uint8_t brightness = 4;

long last_time;

// Button interrupt variables and Interrupt Service Routine
uint8_t buttonState = 0;
volatile long buttonDownTime = 0;
volatile long buttonPressTime = 0;

#define BUTTON_BRIGHTNESS_SWITCH_TIME  1     // Time to hold the button down to switch brightness
#define BUTTON_PATTERN_SWITCH_TIME    500  // Time to hold the button down to switch patterns

uint8_t currentAnimation = 3;
#define ANIMATION_COUNT 4

ColorLoop rainbow(1,1,1);
Scanner   scanner(4);
Shimmer   shimmer();

// Change the current animation
void initializeAnimation(uint8_t newAnimation) {
  currentAnimation = newAnimation;
  
//  switch (currentAnimation) {
//    case 0:
//      setColorLoopColors(1,1,1);
//      break;
//    case 1:
//      setColorLoopColors(.2,1,1);
//      break;
//    case 2:
//      InitializeShimmer();
//      SetColorTemperature(0);
//      break;
//    case 3:
//      break;
//  }
}

// Run one step of the current animation
void runAnimation() {
  switch (currentAnimation) {
    case 0:
    case 1:
      rainbow.draw(leds);
      break;
    case 2:
      shimmer.draw(leds);
      break;
    case 3:
      scanner.draw(leds);
      break;
  }
}


ISR(PCINT0_vect){                        // Will be called on both pressing and releasing
  buttonState = !(PINB & (1 << PINB6)); // Reading state of the PB6 (remember that HIGH == released)
  
  if(buttonState) {
    // On button down, just record the time
    buttonDownTime = millis();
    // TODO: Start gesture timer...
  }
  else {
    // On button up, if we've waited a little time, then update the brightness.
    buttonPressTime = millis() - buttonDownTime;
    if(buttonPressTime > BUTTON_PATTERN_SWITCH_TIME) {
      initializeAnimation((currentAnimation+1)%ANIMATION_COUNT);
    }
    else if(buttonPressTime > BUTTON_BRIGHTNESS_SWITCH_TIME) {
      brightness = (brightness + 1) % BRIGHT_STEP_COUNT;
      LEDS.setBrightness(brightnesSteps[brightness]);
    }
  }
}

void setup()
{  
  Serial.begin(57600);
  
  LEDS.addLeds<WS2811, LED_OUT, GRB>(leds, LED_COUNT);
  LEDS.setBrightness(93); // Limit max current draw to 1A
  LEDS.show();

  pinMode(BUTTON_IN, INPUT_PULLUP);
  pinMode(ANALOG_INPUT, INPUT_PULLUP);
  pinMode(EXTRA_PIN_A, INPUT_PULLUP);
  pinMode(EXTRA_PIN_B, INPUT_PULLUP);
  
  // Interrupt set-up; see Atmega32u4 datasheet section 11
  PCIFR  |= (1 << PCIF0);  // Just in case, clear interrupt flag
  PCMSK0 |= (1 << PCINT6); // Set interrupt mask to the button pin (PCINT6)
  PCICR  |= (1 << PCIE0);  // Enable interrupt
  
  last_time = millis();
}

void loop()
{
  // If'n we get some data, switch to passthrough mode
  if(Serial.available() > 0) {
    serialLoop(leds);
  }
  
  runAnimation();

  LEDS.show();
}

