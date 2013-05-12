#ifndef ANIMATION_H
#define ANIMATOR_H

#include "Arduino.h"
#ifndef _NEOPIXEL_H
#define _NEOPIXEL_H
#include <Adafruit_NeoPixel.h>
#endif

#define ENCODING_NONE  0
#define ENCODING_RLE   1
#define ENCODING_16RLE 2

class animation {
 private:
  const uint16_t m_frameCount;
  const prog_uint8_t* m_frameData;
  const uint8_t m_encoding;
  const uint8_t m_ledCount;
  
  uint16_t m_frameIndex;
  prog_uint8_t* currentFrameData;

  void drawNoEncoding(Adafruit_NeoPixel& strip);  
  void drawRLE(Adafruit_NeoPixel& strip);
  void draw16bitRLE(Adafruit_NeoPixel& strip);
  
 public:
  animation(uint16_t frameCount, const prog_uint8_t* frameData, const uint8_t encoding = ENCODING_NONE);
 
  // Reset the animation
  void reset();
  // Is animation finished/not started?
  boolean isDone();
  
  // Draw the next frame of the animation
  void draw(Adafruit_NeoPixel& strip);
};

#endif
