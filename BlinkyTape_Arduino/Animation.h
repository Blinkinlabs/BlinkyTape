#ifndef ANIMATION_H
#define ANIMATION_H

#include <Arduino.h>
#include <FastSPI_LED2.h>

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

  void drawNoEncoding(struct CRGB strip[]);
  void draw16bitRLE(struct CRGB strip[]);
  
 public:
  Animation();
  Animation(uint16_t frameCount, const prog_uint8_t* frameData, const uint8_t encoding, const uint8_t ledCount);

  // Re-initialize the animation with new information
  void init(uint16_t frameCount, const prog_uint8_t* frameData, const uint8_t encoding, const uint8_t ledCount);
 
  // Reset the animation
  void reset();
  
  // Draw the next frame of the animation
  void draw(struct CRGB strip[]);
};

#endif
