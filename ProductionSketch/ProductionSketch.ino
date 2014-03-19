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
volatile uint8_t brightnesSteps[BRIGHT_STEP_COUNT] = {5,15,40,70,93};
volatile uint8_t brightness = 4;
volatile uint8_t lastBrightness = 4;

long last_time;

// Button interrupt variables and Interrupt Service Routine
uint8_t buttonState = 0;
bool buttonDebounced;
volatile long buttonDownTime = 0;
volatile long buttonPressTime = 0;

#define BUTTON_BRIGHTNESS_SWITCH_TIME  1     // Time to hold the button down to switch brightness
#define BUTTON_PATTERN_SWITCH_TIME    1000   // Time to hold the button down to switch patterns

uint8_t currentPattern = 0;
uint8_t patternCount = 0;
#define MAX_PATTERNS 4
Pattern* patterns[MAX_PATTERNS];
//uint8_t patternSelectionIndicator = 255;

ColorLoop rainbow(1,1,1);
ColorLoop blues(.2,1,1);
Scanner   scanner(4, CRGB(0,255,0));
Shimmer   shimmer;

// Register a pattern
void registerPattern(Pattern* newPattern) {
  // If there is space for this pattern
  if(MAX_PATTERNS <= patternCount) {
    return;
  }
  
  patterns[patternCount] = newPattern;
  patternCount++;
}

// Change the current pattern
void initializePattern(uint8_t newPattern) {
  // Check if this is a valid pattern
  if(newPattern >= MAX_PATTERNS) {
    return;
  }
  
  currentPattern = newPattern;
  patterns[currentPattern]->reset();
  
//  patternSelectionIndicator = 0;
}

// Run one step of the current pattern
void runPattern() {
  patterns[currentPattern]->draw(leds);
}


// Called when the button is both pressed and released.
ISR(PCINT0_vect){
  buttonState = !(PINB & (1 << PINB6)); // Reading state of the PB6 (remember that HIGH == released)
  
  if(buttonState) {
    // On button down, record the time so we can convert this into a gesture later
    buttonDownTime = millis();
    buttonDebounced = false;
    
    // And configure and start timer4 interrupt.
    TCCR4B = 0x0F; // Slowest prescaler
    TCCR4D = _BV(WGM41) | _BV(WGM40);  // Fast PWM mode
    OCR4C = 0x10;        // some random percentage of the clock
    TCNT4 = 0;  // Reset the counter
    TIMSK4 = _BV(TOV4);  // turn on the interrupt
    
  }
  else {
    TIMSK4 = 0;  // turn off the interrupt
  }
}

// This is called every xx ms while the button is being held down; it counts down then displays a
// visual cue and changes the pattern.
ISR(TIMER4_OVF_vect) {
  // If the user is still holding down the button after the first cycle, they were serious about it.
  if(buttonDebounced == false) {
    buttonDebounced = true;
    lastBrightness = brightness;
    brightness = (brightness + 1) % BRIGHT_STEP_COUNT;
    LEDS.setBrightness(brightnesSteps[brightness]);
  }
  
  // If we've waited long enough, switch the pattern
  // TODO: visual indicator
  buttonPressTime = millis() - buttonDownTime;
  if(buttonPressTime > BUTTON_PATTERN_SWITCH_TIME) {
    // first unroll the brightness!
    brightness = lastBrightness;
    LEDS.setBrightness(brightnesSteps[brightness]);
    
    initializePattern((currentPattern+1)%patternCount);
    
    // Finally, reset the button down time, so we don't advance again too quickly
    buttonDownTime = millis();
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
  
  registerPattern(&rainbow);
  registerPattern(&blues);
  registerPattern(&scanner);
  registerPattern(&shimmer);
  
  last_time = millis();
  
}

void loop()
{
  // If'n we get some data, switch to passthrough mode
  if(Serial.available() > 0) {
    serialLoop(leds);
  }
  
//  if(patternSelectionIndicator < 85) {
//    patternSelectionIndicator += 1;
//    LEDS.showColor(CRGB(50,0,100));
//  }
//  else if(patternSelectionIndicator < 170) {
//    patternSelectionIndicator += 1;
//    LEDS.showColor(CRGB(0,0,0));
//  }
//  else if(patternSelectionIndicator < 254) {
//    patternSelectionIndicator += 1;
//    LEDS.showColor(CRGB(100,0,150));
//  }
//  else {
    runPattern();
    LEDS.show();
//  }
}

