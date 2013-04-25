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
      
      int r = int(red(image.pixels[y*image.width+x]));
      int g = int(green(image.pixels[y*image.width+x]));
      int b = int(blue(image.pixels[y*image.width+x]));

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
  
  // Actually write out the data
  void writeRLE() {
    println("Saving animation to: " + m_name);
    PrintWriter file = createWriter(m_name + ".h");
    
    List<Integer> colors = new ArrayList<Integer>();
    
    file.println("// Data file for animation " + m_name);
    file.println("// Compression: RLE");
    file.println("// Uncompressed size: " + m_frameData.size() + " bytes");
    
    // Print all data to a string buffer now, so we can add more stats to the output file.
    StringWriter data = new StringWriter();
    
    data.write("const PROGMEM prog_uint8_t " + m_name + "Data[]  = {\n");

    int totalRuns = 0;
        
    // for each frame
    // We want to make RLE: 1 bit new frame marker, 7 bits length, 8 bits r, 8 bits g, 8 bits b
    for(int frame = 0; frame < m_frameData.size()/m_numberOfLEDs/3; frame++) {
      int runCount = 0;
      int startingOffset = frame*m_numberOfLEDs*3;
      
      // Read in the first pixel
      int rleCount = 1;
      int rleData =   (m_frameData.get(startingOffset  ) << 16)
                    + (m_frameData.get(startingOffset+1) <<  8)
                    + (m_frameData.get(startingOffset+2)      );
      
      for(int i = 1; i < m_numberOfLEDs; i++) {
        int newData =  (m_frameData.get(startingOffset + i*3   ) << 16)
                     + (m_frameData.get(startingOffset + i*3 +1) <<  8)
                     + (m_frameData.get(startingOffset + i*3 +2)      );

        if(rleData == newData) {
          rleCount++;
        }
        else {
          data.write(String.format("  %3d, %3d, %3d, %3d,\n",rleCount,
                                                             (rleData >> 16) & 0xff,
                                                             (rleData >> 8)  & 0xff,
                                                             (rleData)       & 0xff));
          rleCount = 1;
          rleData = newData;
          runCount++;
          totalRuns++;
        }

      }
      data.write(String.format("  %3d, %3d, %3d, %3d,\n",rleCount,
                                                         (rleData >> 16) & 0xff,
                                                         (rleData >> 8)  & 0xff,
                                                         (rleData)       & 0xff));
      totalRuns++;
    }
    
    data.write("};\n");
    
    file.println("// Compressed size: " + totalRuns*4 + " bytes");
    file.println("// Unique runs: " + totalRuns);
    
    file.print(data);
    
    file.println("animation " + m_name + "(" + (m_frameData.size()/m_numberOfLEDs/3) + "," + m_name + "Data, ENCODING_RLE);");
    
    file.flush();
    file.close();
  }
  
  
  // Actually write out the data
  void write16bitRLE() {
    println("Saving animation to: " + m_name);
    PrintWriter file = createWriter(m_name + ".h");
    
    List<Integer> colors = new ArrayList<Integer>();
    
    file.println("// Data file for animation " + m_name);
    file.println("// Compression: 16 bit RLE");
    file.println("// Uncompressed size: " + m_frameData.size() + " bytes");
    
    // Print all data to a string buffer now, so we can add more stats to the output file.
    StringWriter data = new StringWriter();
    
    data.write("const PROGMEM prog_uint8_t " + m_name + "Data[]  = {\n");

    int totalRuns = 0;
        
    // for each frame
    // We want to make RLE: 1 bit new frame marker, 7 bits length, 8 bits r, 8 bits g, 8 bits b
    for(int frame = 0; frame < m_frameData.size()/m_numberOfLEDs/3; frame++) {
      int runCount = 0;
      int startingOffset = frame*m_numberOfLEDs*3;
      
      // Read in the first pixel
      int rleCount = 1;
      int rleData =   ((m_frameData.get(startingOffset  ) >> 3) << 11)
                    | ((m_frameData.get(startingOffset+1) >> 2) <<  5)
                    | ((m_frameData.get(startingOffset+2) >> 3)      );
      
      for(int i = 1; i < m_numberOfLEDs; i++) {
        int newData =   ((m_frameData.get(startingOffset + i*3   ) >> 3) << 11)
                      | ((m_frameData.get(startingOffset + i*3 +1) >> 2) <<  5)
                      | ((m_frameData.get(startingOffset + i*3 +2) >> 3)      );

        if(rleData == newData) {
          rleCount++;
        }
        else {
          data.write(String.format("  %3d, %3d, %3d,\n",rleCount,
                                                        (rleData >> 8) & 0xff,
                                                        (rleData)      & 0xff));
          rleCount = 1;
          rleData = newData;
          runCount++;
          totalRuns++;
        }

      }
      data.write(String.format("  %3d, %3d, %3d,\n",rleCount,
                                                    (rleData >> 8)  & 0xff,
                                                    (rleData)       & 0xff));
      totalRuns++;
    }
    
    data.write("};\n");
    
    file.println("// Compressed size: " + totalRuns*3 + " bytes");
    file.println("// Unique runs: " + totalRuns);
    
    file.print(data);
    
    file.println("animation " + m_name + "(" + (m_frameData.size()/m_numberOfLEDs/3) + "," + m_name + "Data, ENCODING_16RLE);");
    
    file.flush();
    file.close();
    
    println("Compressed size: " + totalRuns*3 + " bytes");
  }
}


