// Pulse to the music

float maxWidth = 30;

class Pulser {
  float m_x;
  float m_y;
  float m_xv;
  float m_yv;
  float m_size;
  float m_scale;
  
  int m_band;

//  float m_value;
  float m_falloff;
  
  float m_h;
  float m_s;
  
  ArrayList<Float> m_values = new ArrayList<Float>();

  Pulser() {
    m_x = random(0,maxWidth);
    m_y = random(0,height);
    m_xv = random(-.2,.2);
    m_yv = random(-.2,.2);

    m_size  = 10;
    m_scale = 3;
    
    m_falloff = .70;
    
    m_h = random(0,100);
    m_s = 100;
  }
  
  // @param x X position
  // @param y Y position
  // @param s size
  Pulser(float x, float y, float s) {
    m_x = x;
    m_y = y;
    m_size = s;
  }
  
  void draw(FFT fft) {
    m_scale = globalVolume;
    
    m_values.add(fft.getAvg(m_band));
    
    float value = 0;
    for(Float v : m_values) {
      value += v;
    }
    value = value/m_values.size();
    
    while(m_values.size() > 1) {
      m_values.remove(0);
    }
    
//    m_value = max(fft.getAvg(m_band), m_value);
    
    // Draw a fuzzy rectangle
    noStroke();
    colorMode(HSB, 100);

    float b = max(0,min(100,m_scale*value));
    float a = max(0,min(100,m_scale*value));

    color fgcolor = color((m_h + sin(colorAngle)*100+50)%99, m_s, b, a);
    color bgcolor = color((m_h + sin(colorAngle)*100+50)%99, m_s, b, 0);

    int w = (int)(m_scale*value + m_size);

    drawFuzzyRectangle((int)(m_x-w/2),(int)( m_y-w/2), w, w, w, fgcolor, bgcolor);
    stroke(1);
    
    m_x = (m_x + m_xv);
    m_y = (m_y + m_yv);
    
    if(m_x > maxWidth) {
      m_x = 0;
      m_y = random(0,height);
    }
    else if(m_x < 0) {
      m_x = maxWidth;
      m_y = random(0,height);
    }
    
    if(m_y > height) {
      m_y = 0;
      m_x = random(0,maxWidth);
    }
    else if(m_y < 0) {
      m_y = height;
      m_x = random(0,maxWidth);
    }

    
//    m_value = m_value*m_falloff;
    
    colorMode(RGB, 256);
  }
  
//  void draw(float kickSize) {
//    // Draw a fuzzy rectangle
//    noStroke();
//
//    float bright = (kickSize -15)/8;
//    color fgcolor = color((sin(col             )+1)*128, 
//                          (sin(col + 3.14159*2/3)+1)*128, 
//                          (sin(col + 3.14159*4/3)+1)*128, 
//                          255);
////    color bgcolor = color(0,0);
//    color bgcolor = color((sin(col              )+1)*128, 
//                          (sin(col + 3.14159*2/3)+1)*128, 
//                          (sin(col + 3.14159*4/3)+1)*128, 
//                          0);
//
//    int w = (int)(m_size*bright);
//    drawFuzzyRectangle((int)(m_x-w/2),(int)( m_y-w/2), w, w, w, fgcolor, bgcolor);
//    stroke(1);
//    
//    m_x = (m_x + m_xv + maxWidth)%maxWidth;
//    m_y = (m_y + m_yv + height)%height;
//  }
}
