#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>
#include <pthread.h>

#include "LedStrip.h"
#include "SocketListener.h"

char* global_data;

pthread_mutex_t load_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t load_signal = PTHREAD_COND_INITIALIZER;

void * dataloader(void * arg)
{
    LedStrip* strip = (LedStrip*) arg;
    while(1) {
        // Load phase
        pthread_mutex_lock(&load_mutex);
        pthread_cond_wait(&load_signal, &load_mutex);
        pthread_mutex_unlock(&load_mutex);

        strip->Flip();
        strip->LoadData(global_data + 1);
    }

    return NULL;
}

int main( int argc, const char* argv[] ) {
    // Create a thread for each LED strip
    std::vector<pthread_t*> threads;

    // Connect to a LED strip
    std::vector<LedStrip*> strips;

    // Specify the screen geometry and strips on the command line, like this:
    // host 160 40 /dev/ttyACM0 0 /dev/ttyACM1 8

    int display_height = atoi(argv[1]);
    int display_width = atoi(argv[2]);

    std::cout << "Initializing display"
              << ", width=" << display_width
              << ", height=" << display_height
              << std::endl;

    // Init a data buffer, let's only make this once. TODO: WTF!
    global_data = new char[display_width*display_height*3+1];

    for(int i = 3; i < argc; i+=2) {
        std::cout << "Adding output device, port=" << argv[i]
                  << ", offset=" << atoi(argv[i+1])
                  << std::endl;
        strips.push_back(new LedStrip(
            display_width,
            display_height,
            atoi(argv[i+1]))
        );
        strips.back()->Connect(argv[i]);

        threads.push_back(new pthread_t);
        pthread_create(
            threads.back(),
            NULL,
            dataloader,
            (void *)(strips.back())
        );
    }

    SocketListener listener;
    listener.Connect("0.0.0.0", 58082);

    while(1) {
        int status = listener.GetFrame(
            global_data,
            display_width*display_height*3+1
        );
        if (status == 0) {
//            pthread_mutex_unlock(&load_mutex);
            pthread_cond_broadcast(&load_signal);
//            pthread_mutex_lock(&load_mutex);
        }
    }
}
