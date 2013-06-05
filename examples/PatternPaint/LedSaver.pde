
// These need to agree with the defines in PatternPlayer sketch.
int ANIMATION_DATA_ADDRESS = 0x4000;
int CONTROL_DATA_ADDRESS = (0x7000 - 4);
  

class LedColor
{
  color m_c;
  
  LedColor(color c) {
    m_c = c;
  }
  
  int getRed() {
    return (int)(red(m_c));
  }

  int getGreen() {
    return (int)(green(m_c));
  }
  
  int getBlue() {
    return (int)(blue(m_c));
  }
  
  // Get a 5-6-5 representation of the color
  int getSixteenBit() {
    return ((getRed()   >> 3) << 11)
         | ((getGreen() >> 2) <<  5)
         | ((getBlue()  >> 3)      );
  }
}

// Container class to describe a single run of RLE compressed data
class RleRun
{
  int m_length;
  int m_data;
  
  RleRun(int length, int data) {
    m_length = length;
    m_data = data;
  }
}

class LedSaver
{
  private final int m_numberOfLEDs;   // Number of LEDs on the Blinkytape (60)
  private final String m_name;        // Animation name
  private List<LedColor> m_frameData;    // Array of stored color data

  // Create a new LED saver
  // @param name Animation name
  // @param numberOfLEDs Number of LEDs in a single frame of the animation
  LedSaver(String name, int numberOfLEDs) {
    m_numberOfLEDs = numberOfLEDs;
    m_name = name;
    
    m_frameData = new ArrayList<LedColor>();
  }
  
  // Add a frame to the animation, using the screen as a data source
  // @param x1 First coordinate of the line to sample along
  // @param y1 First coordinate of the line to sample along
  // @param x1 Second coordinate of the line to sample along
  // @param y1 Second coordinate of the line to sample along
  void addFrame(float x1, float y1, float x2, float y2) {
    addFrame(get(), x1, y1, x2, y2);
  }
  
  // Add a frame to the animation, using the screen as a data source
  // @param image Source image to sample from
  // @param x1 First coordinate of the line to sample along
  // @param y1 First coordinate of the line to sample along
  // @param x1 Second coordinate of the line to sample along
  // @param y1 Second coordinate of the line to sample along
  void addFrame(PImage image, float x1, float y1, float x2, float y2) {
    image.loadPixels();

    // data is R,G,B
    for(int i = 0; i < m_numberOfLEDs; i++) {
      // Sample a point along the line and save it to the array
      int x = (int)((x2 - x1)/m_numberOfLEDs*i + x1);
      int y = (int)((y2 - y1)/m_numberOfLEDs*i + y1);
      
      m_frameData.add(new LedColor(image.pixels[y*image.width+x]));
    }
  }
  
  // Actually write out the data
  void write() {
    println("Saving animation to: " + m_name);
    PrintWriter file = createWriter(m_name + ".h");
    
    file.println("// Data file for animation " + m_name);
    file.println("// Compression: none");
    file.println("// Data size: " + m_frameData.size()*3 + "bytes");
    file.println("");
    
    file.println("const PROGMEM prog_uint8_t " + m_name + "Data[]  = {");

    for(int i = 0; i < m_frameData.size(); i++) {
      if(i%m_numberOfLEDs == 0 && i != 0) {
        file.println("");
      }
      file.println(String.format("  %3d,%3d,%3d,",m_frameData.get(i).getRed(),
                                                  m_frameData.get(i).getGreen(),
                                                  m_frameData.get(i).getBlue()));
    }
    
    file.println("};");
    file.println("animation " + m_name + "(" + (m_frameData.size()/m_numberOfLEDs*3) + "," + m_name + "Data);");
    file.flush();
    file.close();
  }
  
  List<RleRun> get16bitRleData() {
    List<RleRun> runs = new ArrayList<RleRun>();
        
    // for each frame
    // We want to make RLE: 1 bit new frame marker, 7 bits length, 8 bits r, 8 bits g, 8 bits b
    for(int frame = 0; frame < m_frameData.size()/m_numberOfLEDs; frame++) {
      
      // Read in the first pixel
      RleRun run = new RleRun(1, m_frameData.get(frame*m_numberOfLEDs).getSixteenBit());
      
      // For each successive pixel, if it's different 
      for(int i = 1; i < m_numberOfLEDs; i++) {
        int newData = m_frameData.get(frame*m_numberOfLEDs + i).getSixteenBit();

        if(run.m_data == newData) {
          run.m_length++;
        }
        else {
          runs.add(run);
          run = new RleRun(1, newData);
        }
      }
      runs.add(run);
    }
    
    return runs;
  }
  
  // Write the data out as a hex file!
  void write16bitRLEHex() {
    List<RleRun> runs = get16bitRleData();

    // Animation data
    byte[] data = new byte[runs.size()*3];
    
    for(int i = 0; i < runs.size(); i++) {
      data[i*3    ] = (byte)(runs.get(i).m_length);
      data[i*3 + 1] = (byte)((runs.get(i).m_data >> 8) & 0xff);
      data[i*3 + 2] = (byte)((runs.get(i).m_data)      & 0xff);
    }

    String animationDataOutput = writeOutData(ANIMATION_DATA_ADDRESS, data, 0, data.length);
    
    // Make the control structure
    byte[] controlData = new byte[4];
    controlData[0] = (byte)((ANIMATION_DATA_ADDRESS >> 8) & 0xFF);
    controlData[1] = (byte)((ANIMATION_DATA_ADDRESS     ) & 0xFF);
    controlData[2] = (byte)((m_frameData.size()/m_numberOfLEDs >> 8) & 0xFF);
    controlData[3] = (byte)((m_frameData.size()/m_numberOfLEDs     ) & 0xFF);
    
    String controlDataOutput = writeOutData(CONTROL_DATA_ADDRESS, controlData, 0, controlData.length);
    
    PrintWriter file = createWriter(m_name + ".hex");
    file.print(controlDataOutput);
    file.print(animationDataOutput);
      
    file.flush();
    file.close();
  }
  
  // Write out the data as a c++ header
  void write16bitRLE() {
    println("Saving animation to: " + m_name);

    List<RleRun> runs = get16bitRleData();
    
    PrintWriter file = createWriter(m_name + ".h");
    
    file.println("// Data file for animation " + m_name);
    file.println("// Compression: 16 bit RLE");
    file.println("// Uncompressed size: " + m_frameData.size()*3 + " bytes");
    file.println("// Compressed size: " + runs.size()*3 + " bytes");
    file.println("// Unique runs: " + runs.size());
    
    file.println("const PROGMEM prog_uint8_t " + m_name + "Data[]  = {");
    
    for(RleRun run : runs) {
      file.println(String.format("  %3d, %3d, %3d,", run.m_length,
                                                     (run.m_data >> 8)  & 0xff,
                                                     (run.m_data)       & 0xff));
    }
    
    file.println("};");
    
    file.println("animation " + m_name + "(" + (m_frameData.size()/m_numberOfLEDs) + "," + m_name + "Data, ENCODING_16RLE);");
    
    file.flush();
    file.close();
  }
}


