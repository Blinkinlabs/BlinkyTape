
#include "animation.h"

// TODO: maybe make this a helper function, so that the variables can stay const? That's likely too
// heavyweight for Arduino.
animation::animation(const prog_uint8_t* animationData)
{
  // Read the frame count from the first two bytes of 
  m_encoding = pgm_read_byte(animationData);
  m_frameCount = pgm_read_word(animationData + 1);
  m_frameData = const_cast<prog_uint8_t*>(animationData + 3);
  m_ledCount = 60;
  
  reset();
}

animation::animation(uint16_t frameCount, const prog_uint8_t* frameData, const uint8_t encoding) :
  m_frameCount(frameCount),
  m_frameData(const_cast<prog_uint8_t*>(frameData)),
  m_encoding(encoding),
  m_ledCount(60)
{
  reset();
}
 
void animation::reset() {
  m_frameIndex = 0;
  currentFrameData = const_cast<prog_uint8_t*>(m_frameData);
}

void animation::draw(Adafruit_NeoPixel& strip) {
  switch(m_encoding) {
    case ENCODING_NONE:
      drawNoEncoding(strip);
      break;
    case ENCODING_RLE:
      drawRLE(strip);
      break;
    case ENCODING_16RLE:
      draw16bitRLE(strip);
      break;
  }
};

void animation::drawNoEncoding(Adafruit_NeoPixel& strip) {
  currentFrameData = const_cast<prog_uint8_t*>(m_frameData) + m_frameIndex*m_ledCount*3;
  
  for(uint8_t i = 0; i < m_ledCount; i+=1) {

    strip.setPixelColor(i, strip.Color(pgm_read_byte(currentFrameData + i*3    ),
                                       pgm_read_byte(currentFrameData + i*3 + 1),
                                       pgm_read_byte(currentFrameData + i*3 + 2)));
  }
  
  strip.show();
  
  m_frameIndex = (m_frameIndex + 1)%m_frameCount;
}

void animation::drawRLE(Adafruit_NeoPixel& strip) {

  // Read runs of RLE data until we get enough data.
  uint8_t count = 0;
  while(count < 60) {
    uint8_t run_length = 0x7F & pgm_read_byte(currentFrameData);
    uint8_t r = pgm_read_byte(currentFrameData + 1);
    uint8_t g = pgm_read_byte(currentFrameData + 2);
    uint8_t b = pgm_read_byte(currentFrameData + 3);
    
    for(uint8_t i = 0; i < run_length; i+=1) {
      strip.setPixelColor(count + i, strip.Color(r,g,b));
    }
    
    count += run_length;
    currentFrameData += 4;
  }
  
  strip.show();

  m_frameIndex = (m_frameIndex + 1)%m_frameCount;
  if(m_frameIndex == 0) {
    currentFrameData = const_cast<prog_uint8_t*>(m_frameData);
  }
};

void animation::draw16bitRLE(Adafruit_NeoPixel& strip) {

  // Read runs of RLE data until we get enough data.
  uint8_t count = 0;
  while(count < 60) {
    uint8_t run_length = 0x7F & pgm_read_byte(currentFrameData);
    uint8_t upperByte = pgm_read_byte(currentFrameData + 1);
    uint8_t lowerByte = pgm_read_byte(currentFrameData + 2);
    
    uint8_t r = ((upperByte & 0xF8)     );
    uint8_t g = ((upperByte & 0x07) << 5)
              | ((lowerByte & 0xE0) >> 3);
    uint8_t b = ((lowerByte & 0x1F) << 3);
    
    for(uint8_t i = 0; i < run_length; i+=1) {
      strip.setPixelColor(count + i, strip.Color(r,g,b));
    }
    
    count += run_length;
    currentFrameData += 3;
  }
  
  strip.show();

  m_frameIndex = (m_frameIndex + 1)%m_frameCount;
  if(m_frameIndex == 0) {
    currentFrameData = const_cast<prog_uint8_t*>(m_frameData);
  }
};
