#include <FastSPI_LED2.h>
#include <avr/pgmspace.h>
#include <Animation.h>
#include "pov.h"

#define LED_COUNT 60
struct CRGB leds[LED_COUNT];

Animation pov;

void setup()
{  
  Serial.begin(57600);

  LEDS.addLeds<WS2811, 5, GRB>(leds, LED_COUNT);
  LEDS.showColor(CRGB(0, 0, 0));
  LEDS.setBrightness(230); // 90% brightness
  LEDS.show();
  
  // Read the animation data from the end of the program memory, and construct a new Animation from it.
  int frameCount;
  prog_uint8_t* frameData;

  // These could be whereever, but need to agree with Processing.
  #define CONTROL_DATA_ADDRESS (0x7000 - 4)
  #define FRAME_DATA_ADDRESS   (CONTROL_DATA_ADDRESS)
  #define FRAME_COUNT_ADDRESS  (CONTROL_DATA_ADDRESS + 2)

  frameData  =
  (prog_uint8_t*)((pgm_read_byte(FRAME_DATA_ADDRESS    ) << 8)
                  + (pgm_read_byte(FRAME_DATA_ADDRESS + 1)));
               
  frameCount = (pgm_read_byte(FRAME_COUNT_ADDRESS    ) << 8)
             + (pgm_read_byte(FRAME_COUNT_ADDRESS + 1));
             
  
  pov.init(frameCount, frameData, ENCODING_16RLE, LED_COUNT);
  
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
  
  pov.draw(leds);
  delay(20);
}

