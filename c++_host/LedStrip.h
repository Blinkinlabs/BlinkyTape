#ifndef LEDSTRIP_H
#define LEDSTRIP_H

#include <string>

class LedStrip {
  public:
    /**
     * Create a new LedStrip
     * @param image_width Width of the source impage
     * @param image_height Height of the source image
     * @param offst Row offset to write to this strip
     */
    LedStrip(int image_width, int image_height, int offset) :
      m_image_width(image_width),
      m_image_height(image_height),
      m_offset(offset) {
    }

    /**
     * Open a serial device for writing
     * @param portname Name of the serial port to open (example: /dev/ttyACM0)
     */
    void Connect(std::string portname);

    /**
     * Write a buffer of data out to the serial port
     * @param data Frame of color data to load, image_height*image_width*3 bytes
     */
    void LoadData(char* data);

    /**
     * Cause the strips to update their displays by clocking out 0's
     */
    void Flip();

  private:
    /**
     * Send 64 bytes of data to the machine. Automatically handles flushing the
     * data, and retrying if necessicary.
     * @param data 64 bytes of data to send.
     **/
    void SendBytes64(char* data);

    /**
     * Convert a block of colors from split RGB format to parallal format
     * @param[out] output_data 24 bytes of formatted color data.
     * @param[in] input_data 24 bytes of input color data
     */
    //void ConvertColor24(char* output_data, char* input_data);

    int m_image_width;
    int m_image_height;
    int m_offset;

    int m_fd;	// File descriptor
};

#endif
