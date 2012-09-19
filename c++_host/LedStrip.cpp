#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>

#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */

#include "LedStrip.h"

void LedStrip::Connect(std::string portname)
{
    m_fd = open(portname.c_str(), O_RDWR | O_NOCTTY | O_NDELAY);
    if (m_fd == -1)
    {
        perror("open_port: Unable to open port:");
        perror(portname.c_str());
        exit(1);  // TODO: Should we actually exit here?
    }
}

void LedStrip::SendBytes64(char* data) {
    int return_code;
    // TODO: we should check if our file disappears.
    
    do {
        return_code = write(m_fd, data, 64);
        // If a write error occurs, it is probably because the buffer is full.
        // Force it to drain, then try again.
        if (return_code < 0) {
            tcdrain(m_fd);
        }
    }
    while (return_code < 0);
}

// void LedStrip::ConvertColor24(char* output_data, char* input_data) {
//     memset(output_data,0,24);

//     output_data[0] = 0xFF;
//     output_data[8] = 0xFF;
//     output_data[16] = 0xFF;


//     for (int bit_index = 7; bit_index > 0; bit_index--) {
//         for (int pixel_index = 0; pixel_index < 8; pixel_index++) {
//             output_data[1 +7-bit_index] |= ((input_data[1 + 3*pixel_index] >> bit_index) & 1) << pixel_index;
//             output_data[9 +7-bit_index] |= ((input_data[    3*pixel_index] >> bit_index) & 1) << pixel_index;
//             output_data[17+7-bit_index] |= ((input_data[2 + 3*pixel_index] >> bit_index) & 1) << pixel_index;
//         }
//     }
// }

void LedStrip::LoadData(char* input_data) {
    char output_data[m_image_height*3];

    // Convert the data to the appropriate space
    // for (int row = 0; row < m_image_height; row++) {
    //     // Increment input for these reasons:
    //     // 3*m_offset - LED strip offset
    //     // 3*m_image_width*row - current row
    //     ConvertColor24(
    //         output_data+row*24,
    //         input_data+3*m_offset+3*m_image_width*row
    //     );
    // }

    for (int x = 0; x < m_image_height * 3; x++) {

        output_data[x] = input_data[x] | 0x80;
    }

    // Write out the appropriate amount of data
    for (int index = 0; index < m_image_height*3; index+=64) {
        SendBytes64(output_data+index);
    }
}

void LedStrip::Flip() {
    char test[64];
    for (int index = 0; index < 64; index++) {
        test[index] = 0x00;
    }

    // Write out the appropriate amount of data
    SendBytes64(test);
}
