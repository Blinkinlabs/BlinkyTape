#ifndef ANIMATION_H
#define ANIMATOR_H

#include "Arduino.h"
#include <Adafruit_NeoPixel.h>

class animation {
 private:
  const uint16_t m_frameCount;
  const prog_uint8_t* m_frameData;
  
  const uint8_t m_ledCount;
  
  uint16_t m_frameIndex;
  
 public:
  animation(uint16_t frameCount, const prog_uint8_t* frameData);
 
  // Reset the animation
  void reset();
  
  // Draw the next frame of the animation
  void draw(Adafruit_NeoPixel& strip);
};

#endif
