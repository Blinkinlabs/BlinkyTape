#ifndef ANIMATION_H
#define ANIMATION_H

#include "Arduino.h"
#ifndef _ADAFRUIT_NEOPIXEL_H
#define _ADAFRUIT_NEOPIXEL_H
#include <Adafruit_NeoPixel.h>
#endif

#define ENCODING_NONE  0
#define ENCODING_16RLE 1

class Animation {
 private:
  uint16_t m_frameCount;
  prog_uint8_t* m_frameData;
  uint8_t m_encoding;
  uint8_t m_ledCount;
  
  uint16_t m_frameIndex;
  prog_uint8_t* currentFrameData;

  void drawNoEncoding(Adafruit_NeoPixel& strip);  
  void draw16bitRLE(Adafruit_NeoPixel& strip);
  
 public:
  Animation();
  Animation(uint16_t frameCount, const prog_uint8_t* frameData, const uint8_t encoding, const uint8_t ledCount);

  // Re-initialize the animation with new information
  void init(uint16_t frameCount, const prog_uint8_t* frameData, const uint8_t encoding, const uint8_t ledCount);
 
  // Reset the animation
  void reset();
  
  // Draw the next frame of the animation
  void draw(Adafruit_NeoPixel& strip);
};

#endif
