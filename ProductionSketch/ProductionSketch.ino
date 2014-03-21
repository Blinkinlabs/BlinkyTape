#include <EEPROM.h>

// This is the example sketch that gets loaded on every BlinkyTape during production!
#include <FastLED.h>
#include <Animation.h>

#include "BlinkyTape.h"
#include "ColorLoop.h"
#include "SerialLoop.h"
#include "Shimmer.h"
#include "Scanner.h"

#define STEP_UP_DOWN_BRIGHTNESS


struct CRGB leds[LED_COUNT];

#ifdef STEP_UP_DOWN_BRIGHTNESS
  #define BRIGHT_STEP_COUNT 8
  volatile uint8_t brightnesSteps[BRIGHT_STEP_COUNT] = {5,15,40,70,93, 70, 40, 15};
#else
  #define BRIGHT_STEP_COUNT 5
  volatile uint8_t brightnesSteps[BRIGHT_STEP_COUNT] = {5,15,40,70,93};
#endif

uint8_t brightness = 4;
uint8_t lastBrightness = 4;


// For fading in a new sketch
long lastTime;
int pixelIndex;


// Button interrupt variables and Interrupt Service Routine
uint8_t buttonState = 0;
bool buttonDebounced;
long buttonDownTime = 0;
long buttonPressTime = 0;

#define BUTTON_BRIGHTNESS_SWITCH_TIME  1     // Time to hold the button down to switch brightness
#define BUTTON_PATTERN_SWITCH_TIME    1000   // Time to hold the button down to switch patterns


#define PATTERN_EEPROM_ADDRESS 0
uint8_t currentPattern = 0;
uint8_t patternCount = 0;
#define MAX_PATTERNS 10
Pattern* patterns[MAX_PATTERNS];


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
  
  EEPROM.write(PATTERN_EEPROM_ADDRESS, newPattern);
  
  currentPattern = newPattern;
  patterns[currentPattern]->reset();
  
  lastTime = millis();
  pixelIndex = 0;
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
  
  registerPattern(new ColorLoop(1,1,1));
  registerPattern(new ColorLoop(.2,1,1));
  registerPattern(new Scanner(4, CRGB(255,0,0)));
  registerPattern(new Shimmer(0));
  

  // Attempt to read in the last used pattern; if it's an invalid
  // number, initialize it to 0 instead.
  currentPattern = EEPROM.read(PATTERN_EEPROM_ADDRESS);
  if(currentPattern >= patternCount) {
    currentPattern = 0;
  }
  
  initializePattern(currentPattern);
}

void loop()
{
  // If'n we get some data, switch to passthrough mode
  if(Serial.available() > 0) {
    serialLoop(leds);
  }
  
  // Draw the current pattern
  runPattern();
    
// Disable- will do a fade down/up instead.
//  //Then, if we transitioning in a new pattern, fade it in.
//  if ((millis() - lastTime > 15) && pixelIndex <= LED_COUNT + 1) {
//    lastTime = millis();
//    pixelIndex++;
//  }
//  
//  // why is this per LED?
//  for (int x = (LED_COUNT - pixelIndex); x >= 0; x--) {
//    leds[x] = CRGB(0, 0, 0);
//  }

    LEDS.show();
}

