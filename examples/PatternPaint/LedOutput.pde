// TODO: Make this threaded! We can't hit high framerates otherwise :-(

class LedOutput
{
  private String m_portName;  // TODO: How to request cu.* devices?
  private Serial m_outPort;

  private int m_numberOfLEDs;

  LedOutput(PApplet parent, String portName, int numberOfLEDs) {
    m_portName = portName;
    m_numberOfLEDs = numberOfLEDs;

    println("Connecting to BlinkyBoard on: " + portName);
    m_outPort = new Serial(parent, portName, 115200);
  }
  
  void sendUpdate(float x1, float y1, float x2, float y2) {
    sendUpdate(get(), x1, y1, x2, y2);
  }
  
  // Update the blinkyboard with new colors
  void sendUpdate(PImage image, float x1, float y1, float x2, float y2) {
    image.loadPixels();
    
    // Note: this should be sized appropriately
    byte[] data = new byte[m_numberOfLEDs*3 + 1];
    int dataIndex = 0;

    // data is R,G,B
    for(int i = 0; i < m_numberOfLEDs; i++) {
      // Sample a point along the line
      int x = (int)((x2 - x1)/m_numberOfLEDs*i + x1);
      int y = (int)((y2 - y1)/m_numberOfLEDs*i + y1);
      
      int r = int(red(image.pixels[y*image.width+x]));
      int g = int(green(image.pixels[y*image.width+x]));
      int b = int(blue(image.pixels[y*image.width+x]));
      
//      if (enableGammaCorrection) {
//        r = (int)(Math.pow(r/256.0,this.gammaValue)*256*bright);
//        g = (int)(Math.pow(g/256.0,this.gammaValue)*256*bright);
//        b = (int)(Math.pow(b/256.0,this.gammaValue)*256*bright);
//      }

// For WS2811
      data[dataIndex++] = (byte)min(254, r);
      data[dataIndex++] = (byte)min(254, g);
      data[dataIndex++] = (byte)min(254, b);

// For LPD8806
//      data[dataIndex++] = (byte)(0x80 + (g >> 1));
//      data[dataIndex++] = (byte)(0x80 + (r >> 1));
//      data[dataIndex++] = (byte)(0x80 + (b >> 1));

    }
    
// For WS2811
    data[dataIndex++] = (byte)255;

// For LPD8806
//    data[dataIndex++] = (byte)0;
    
    // Don't send data too fast, the arduino can't handle it.
    int maxChunkSize = 5;
    for(int currentChunkPos = 0; currentChunkPos < m_numberOfLEDs*3 + 1; currentChunkPos += maxChunkSize) {
      int currentChunkSize = min(maxChunkSize, m_numberOfLEDs*3 + 1 - currentChunkPos);
      byte[] test = new byte[currentChunkSize];
      
      for(int i = 0; i < currentChunkSize; i++) {
//        if(currentChunkPos + i > m_numberOfLEDs*3) {
//          test[i] = (byte)255;
//        }
//        else {
          test[i] = data[currentChunkPos + i];
//        }

      }
    
      m_outPort.write(test);
    }
  }
}

