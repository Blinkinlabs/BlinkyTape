#ifndef SOCKETLISTENER_H
#define SOCKETLISTENER_H

#include <string>

class SocketListener {
  public:
    /**
     * Start a UDP server at the given address
     * @param ip_address IP address to listen on (0.0.0.0 binds to all)
     * @param port Port to listen on (58082 is popular)
     */
    void Connect(std::string ip_address, unsigned int port);

    /**
     * Get a frame of data from the socket and check that it is valid.
     * @param frame Buffer to store the frame in.
     * @param length Expected length of the frame.
     * @return 0 if successful, < 0 if a failure occurred.
     */
    int GetFrame(char* frame, int length);

  private:
    std::string m_address;
    unsigned int m_port;

    int m_fd;
};

#endif
