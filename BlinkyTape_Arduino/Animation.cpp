#include "Animation.h"

Animation::Animation() {
  init(0, NULL, ENCODING_NONE, 0);
}

Animation::Animation(uint16_t frameCount,
                     const prog_uint8_t* frameData,
                     const uint8_t encoding,
                     const uint8_t ledCount)
{
  init(frameCount, frameData, encoding, ledCount);
  reset();
}

void Animation::init(uint16_t frameCount,
                     const prog_uint8_t* frameData,
                     const uint8_t encoding,
                     const uint8_t ledCount)
{
  m_frameCount = frameCount;
  m_frameData = const_cast<prog_uint8_t*>(frameData);
  m_encoding = encoding;
  m_ledCount = ledCount;

  m_frameIndex = 0;
  currentFrameData = m_frameData;
}
 
void Animation::reset() {
  m_frameIndex = 0;
  currentFrameData = m_frameData;
}

void Animation::draw(struct CRGB strip[]) {
  switch(m_encoding) {
    case ENCODING_NONE:
      drawNoEncoding(strip);
      break;
    case ENCODING_16RLE:
      draw16bitRLE(strip);
      break;
  }
};

void Animation::drawNoEncoding(struct CRGB strip[]) {
  currentFrameData = m_frameData + m_frameIndex*m_ledCount*3;
  
  for(uint8_t i = 0; i < m_ledCount; i+=1) {
    strip[i] = CRGB(pgm_read_byte(currentFrameData + i*3    ),
                    pgm_read_byte(currentFrameData + i*3 + 1),
                    pgm_read_byte(currentFrameData + i*3 + 2));
  }
  
  LEDS.show();
  
  m_frameIndex = (m_frameIndex + 1)%m_frameCount;
}

void Animation::draw16bitRLE(struct CRGB strip[]) {

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
      strip[count + i] = CRGB(r,g,b);
    }
    
    count += run_length;
    currentFrameData += 3;
  }
  
  LEDS.show();

  m_frameIndex = (m_frameIndex + 1)%m_frameCount;
  if(m_frameIndex == 0) {
    currentFrameData = m_frameData;
  }
};
