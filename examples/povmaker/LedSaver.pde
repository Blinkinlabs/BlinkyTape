class LedSaver
{
  private int m_numberOfLEDs;
  
  private String m_name;
  private List<Integer> m_frameData;

  LedSaver(String fileName, int numberOfLEDs) {
    m_numberOfLEDs = numberOfLEDs;
    
    m_name = fileName;
    m_frameData = new ArrayList<Integer>();
  }
  
  void sendUpdate(float x1, float y1, float x2, float y2) {
    sendUpdate(get(), x1, y1, x2, y2);
  }
  
  // Update the blinkyboard with new colors
  void sendUpdate(PImage image, float x1, float y1, float x2, float y2) {
    image.loadPixels();
    
    // Note: this should be sized appropriately
//    byte[] data = new byte[m_numberOfLEDs*3 + 1];
    int dataIndex = 0;

    // data is R,G,B
    for(int i = 0; i < m_numberOfLEDs; i++) {
      // Sample a point along the line
      int x = (int)((x2 - x1)/m_numberOfLEDs*i + x1);
      int y = (int)((y2 - y1)/m_numberOfLEDs*i + y1);
      
      int r = int(red(image.pixels[y*width+x]));
      int g = int(green(image.pixels[y*width+x]));
      int b = int(blue(image.pixels[y*width+x]));

      m_frameData.add(r);
      m_frameData.add(g);
      m_frameData.add(b);
    }
  }
  
  // Actually write out the data
  void write() {
    println("Saving animation to: " + m_name);
    PrintWriter file = createWriter(m_name + ".h");
    
    file.println("// Data file for animation " + m_name);
    file.println("// Compression: none");
    file.println("// Data size: " + m_frameData.size() + "bytes");
    file.println("");
    
    file.println("const PROGMEM prog_uint8_t " + m_name + "Data[]  = {");

    for(int i = 0; i < m_frameData.size()/3; i++) {
      if(i%m_numberOfLEDs == 0 && i != 0) {
        file.println("");
      }
      file.println(String.format("  %3d,%3d,%3d,",m_frameData.get(i*3  ),
                                                  m_frameData.get(i*3+1),
                                                  m_frameData.get(i*3+2)));
    }
    
    file.println("};");
    file.println("animation " + m_name + "(" + (m_frameData.size()/m_numberOfLEDs/3) + "," + m_name + "Data);");
    file.flush();
    file.close();
  }
}

