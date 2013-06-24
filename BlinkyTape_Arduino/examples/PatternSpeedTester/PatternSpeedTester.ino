#include <FastSPI_LED2.h>
#include <Animation.h>
#include "pov.h"

#define LED_COUNT 60
struct CRGB leds[LED_COUNT];

float animationStartTime;
int frameCount;

float desiredFrameRate;
unsigned long frameDelayUs;

unsigned long endTime;

void setup()
{  
  Serial.begin(57600);

  LEDS.addLeds<WS2811, 5, GRB>(leds, LED_COUNT);
  LEDS.showColor(CRGB(0, 0, 0));
  LEDS.setBrightness(255); // 90% brightness
  LEDS.show();
  
  frameCount = 0;
  animationStartTime = millis();
  
  desiredFrameRate = 500;
  frameDelayUs = 1/desiredFrameRate*1000*1000;
  endTime = micros();  
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
  
  endTime += frameDelayUs;
  pov.draw(leds);
  while(micros() < endTime) {};
  
  frameCount++;
  if(frameCount > 100) {
    float elapsedTime = millis() - animationStartTime;
    Serial.println(1/(elapsedTime/100/1000));
    frameCount = 0;
    animationStartTime = millis();
  }
}

