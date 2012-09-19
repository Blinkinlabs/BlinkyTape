#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "SocketListener.h"

void SocketListener::Connect(std::string ip_address, unsigned int port) {
    struct sockaddr_in address;

    m_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (m_fd < 0)
    {
        perror("open_socket: Unable to open socket");
        exit(1);  // TODO: Should we actually exit here?
    }


    address.sin_family = AF_INET;
    address.sin_port = htons(port);
    inet_aton(ip_address.c_str(), &address.sin_addr);

    int return_code;
    return_code = bind(m_fd, (struct sockaddr*) &address, sizeof(struct sockaddr_in));
    if (return_code < 0)
    {
        perror("open_socket: Unable to bind to port");
        exit(1);  // TODO: Should we actually exit here?
    }
}

int SocketListener::GetFrame(char* frame, int length) {
    int received_length = read(m_fd, frame, length);

    // TODO: How to return erros here? 
    if (length != received_length) {
        std::cerr << "Bad data frame, expected_length=" << length
                  << " received_length=" << received_length << std::endl;
        return -1;
    }
 
    if (frame[0] != 0x01) {
        std::cerr << "Bad header, expected=1"
                  << " got=" << static_cast<int>(frame[0]) << std::endl;
        return -2;
    }

    return 0;
}
