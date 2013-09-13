#include <FastSPI_LED2.h>
#include <Animation.h>

#define LED_COUNT 60
struct CRGB leds[LED_COUNT];

#ifdef REVB // RevB boards have a slightly different pinout.

#define LED_OUT      5
#define BUTTON_IN    13
#define ANALOG_INPUT A11
#define IO_A         15

#else

#define LED_OUT      13
#define BUTTON_IN    10
#define ANALOG_INPUT A9
#define IO_A         7
#define IO_B         11

#endif

#define BRIGHT_STEP_COUNT 5
uint8_t brightnesSteps[BRIGHT_STEP_COUNT] = {5,15,40,70,93};
uint8_t brightness = 4;
uint8_t lastButtonState = 1;

long last_time;

void setup()
{  
  Serial.begin(57600);
  
  LEDS.addLeds<WS2811, LED_OUT, GRB>(leds, LED_COUNT);
  LEDS.showColor(CRGB(0, 0, 0));
  LEDS.setBrightness(93); // Limit max current draw to 1A
  LEDS.show();

  pinMode(BUTTON_IN, INPUT_PULLUP);
  pinMode(ANALOG_INPUT, INPUT_PULLUP);
  pinMode(IO_A, INPUT_PULLUP);
  pinMode(IO_B, INPUT_PULLUP);
  
  last_time = millis();
}


void color_loop() {  
  static uint8_t i = 0;
  static int j = 0;
  static int f = 0;
  static int k = 0;
  static int count;

  static int pixelIndex;
  
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    leds[i].r = 64*(1+sin(i/2.0 + j/4.0       ));
    leds[i].g = 64*(1+sin(i/1.0 + f/9.0  + 2.1));
    leds[i].b = 64*(1+sin(i/3.0 + k/14.0 + 4.2));
    
    if ((millis() - last_time > 15) && pixelIndex <= LED_COUNT + 1) {
      last_time = millis();
      count = LED_COUNT - pixelIndex;
      pixelIndex++; 
    }
    
    // why is this per LED?
    for (int x = count; x >= 0; x--) {
      leds[x] = CRGB(0, 0, 0);
    }
    
  }
  LEDS.show();
  
  j = j + 1;
  f = f + 1;
  k = k + 2;
}

void serialLoop() {
  static int pixelIndex;

  while(true) {

    if(Serial.available() > 2) {

      uint8_t buffer[3]; // Buffer to store three incoming bytes used to compile a single LED color

      for (uint8_t x=0; x<3; x++) { // Read three incoming bytes
        uint8_t c = Serial.read();
        
        if (c < 255) {
          buffer[x] = c; // Using 255 as a latch semaphore
        }
        else {
          LEDS.show();
          pixelIndex = 0;
          
          // BUTTON_IN (D10):   07 - 0111
          // IO_A(D7):          11 - 1011
          // IO_B (D11):        13 - 1101
          // ANALOG_INPUT (A9): 14 - 1110

          char c = (digitalRead(BUTTON_IN)    << 3)
                 | (digitalRead(IO_A)         << 2)
                 | (digitalRead(IO_B)         << 1)
                 | (digitalRead(ANALOG_INPUT)     );
          Serial.write(c);
          
          break;
        }

        if (x == 2) {   // If we received three serial bytes
          leds[pixelIndex] = CRGB(buffer[0], buffer[1], buffer[2]);
          pixelIndex++;
        }
      }
    }
  }
}

void loop()
{
  // If'n we get some data, switch to passthrough mode
  if(Serial.available() > 0) {
    serialLoop();
  }
  
  uint8_t buttonState = digitalRead(BUTTON_IN);
  if((buttonState != lastButtonState) && (buttonState == 0)) {
    brightness = (brightness + 1) % BRIGHT_STEP_COUNT;
    LEDS.setBrightness(brightnesSteps[brightness]);
  }
  lastButtonState = buttonState;
  
  color_loop();
}

