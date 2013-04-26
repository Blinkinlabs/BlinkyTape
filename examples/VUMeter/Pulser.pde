// Pulse to the music
class Pulser {
  float m_x;
  float m_y;
  float m_xv;
  float m_yv;
  float m_size;
  float m_scale;
  
  int m_band;

  float m_falloff;
  
  float m_h;
  float m_s;
  
  ArrayList<Float> m_values = new ArrayList<Float>();

  Pulser() {
    m_x = random(0,width);
    m_y = random(0,height);
    m_xv = random(-.2,.2);
    m_yv = random(-.2,.2);

    m_size  = 1;
    m_scale = 6;
    
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
    
    float avg = 0;
    int bandCount = 5;
    for( float band = 0; band < bandCount; band++) {
      avg += fft.getAvg(m_band);
    }
    avg = avg/bandCount;
    
    m_values.add(avg);
    
    float value = 0;
    for(Float v : m_values) {
      value += v;
    }
    value = value/m_values.size();
    
    while(m_values.size() > 2) {
      m_values.remove(0);
    }
    
    // Draw a fuzzy rectangle
    noStroke();
    colorMode(HSB, 100);

    if(value < 1) {
      value = 0;
    }

    float b = max(0,min(100,m_scale*value));
    float a = max(0,min(100,m_scale*value));

//    b = 100;
//    a = 100;

    color fgcolor = color(m_h, m_s, b, a);
    color bgcolor = color(m_h, m_s, b, 0);

    int w = (int)(m_scale*value + m_size);

    drawFuzzyRectangle((int)(m_x-w/2),(int)( m_y-w/2), w, w, w, fgcolor, bgcolor);
    stroke(1);
    
    m_x = (m_x + m_xv);
    m_y = (m_y + m_yv);
    
    if(m_x > width) {
      m_x = 0;
      m_y = random(0,height);
    }
    else if(m_x < 0) {
      m_x = width;
      m_y = random(0,height);
    }
    
    if(m_y > height) {
      m_y = 0;
      m_x = random(0,width);
    }
    else if(m_y < 0) {
      m_y = height;
      m_x = random(0,width);
    }
    
    colorMode(RGB, 256);
  }
}
