#include <Adafruit_NeoPixel.h>

#include <avr/pgmspace.h>
#include <Animation.h>
#include "pov.h"

#define LED_COUNT 60
#define THRESHOLD 1

Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_COUNT, 5, NEO_GRB + NEO_KHZ800);

Animation pov;

uint8_t pixel_index;
long last_time;

void setup()
{  
  Serial.begin(57600);

  strip.begin();
  strip.show();
  last_time = millis();
  
  // Read the animation data from the end of the program memory, and construct a new Animation from it.
  int frameCount;
  prog_uint8_t* frameData;

  // These could be whereever, but ne ed to agree with Processing.
  #define CONTROL_DATA_ADDRESS (0x7000 - 4)
  #define FRAME_DATA_ADDRESS   (CONTROL_DATA_ADDRESS)
  #define FRAME_COUNT_ADDRESS  (CONTROL_DATA_ADDRESS + 2)

//  frameData  = (prog_uint8_t*)0x4000;
  frameData  =
  (prog_uint8_t*)((pgm_read_byte(FRAME_DATA_ADDRESS    ) << 8)
                  + (pgm_read_byte(FRAME_DATA_ADDRESS + 1)));
               
  frameCount = (pgm_read_byte(FRAME_COUNT_ADDRESS    ) << 8)
             + (pgm_read_byte(FRAME_COUNT_ADDRESS + 1));
             
  
  pov.init(frameCount, frameData, ENCODING_16RLE, LED_COUNT);
  
}

void serialLoop() {

  while(true) {

    if(Serial.available() > 2) {

      uint8_t buffer[3]; // Buffer to store three incoming bytes used to compile a single LED color

      for (uint8_t x=0; x<3; x++) { // Read three incoming bytes
        uint8_t c = Serial.read();
        
        if (c < 255) {
          buffer[x] = c; // Using 255 as a latch semaphore
        }
        else {
          strip.show();
          pixel_index = 0;
          break;
        }

        if (x == 2) {   // If we received three serial bytes
          strip.setPixelColor(pixel_index, strip.Color(buffer[0], buffer[1], buffer[2]));
          pixel_index++;
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
  
  pov.draw(strip);
  delay(20);
}

