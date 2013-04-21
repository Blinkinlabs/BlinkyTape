
#include "animation.h"

animation::animation(uint16_t frameCount, const prog_uint8_t* frameData) :
  m_frameCount(frameCount),
  m_frameData(frameData),
  m_ledCount(60)
{
  reset();
}
 
void animation::reset() {
  m_frameIndex = 0;
}
  
void animation::draw(Adafruit_NeoPixel& strip) {
  const prog_uint8_t* currentFrameData = m_frameData + m_frameIndex*m_ledCount*3;
  
  for(uint8_t i = 0; i < m_ledCount; i+=1) {

    strip.setPixelColor(i, strip.Color(pgm_read_byte(currentFrameData + i*3    ),
                                       pgm_read_byte(currentFrameData + i*3 + 1),
                                       pgm_read_byte(currentFrameData + i*3 + 2)));
  }
  
  strip.show();
  
  m_frameIndex = (m_frameIndex + 1)%m_frameCount;
};

