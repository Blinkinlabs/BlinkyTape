#ifndef _NEOPIXEL_H
#define _NEOPIXEL_H
#include <Adafruit_NeoPixel.h>
#endif

#include "animation.h"
#include "pov.h"

#define LED_COUNT 60
#define THRESHOLD 1

Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_COUNT, 5, NEO_GRB + NEO_KHZ800);

uint8_t pixel_index;
long last_time;

void setup()
{ 
  Serial.begin(57600);

  strip.begin();
  strip.show();
  last_time = millis();
}


class star {
 public:
  int8_t pos; // led position
  uint8_t framesPerMove; // more is slower
  int length;
  uint8_t r,g,b;

  uint8_t frameCount;

  star() {
    framesPerMove = 10;
    reset();
  }

  void reset() {
    frameCount = 0;
    pos = -random(0,10);
    framesPerMove = random(20,60);
    r = random(0,255);
    g = random(0,255);
    b = random(0,255);
    length = random(1,4);
  }
  
  void draw() {
    strip.setPixelColor(pos-1, strip.Color(r>>2,g>>2,b>>2));
    for(uint8_t i = 0; i < length; i++) {
      strip.setPixelColor(pos+ i, strip.Color(r,g,b));
    }
    strip.setPixelColor(pos+length, strip.Color(r>>2,g>>2,b>>2));

    
    // move
    frameCount++;
    if(frameCount >= framesPerMove) {
      pos += 1;
      frameCount = 0;
    }
    
    // if we get to the end, reset
    if(pos >= LED_COUNT) {
      reset();
    }
  }
  
};


void star_loop() {
  #define starCount 10
  static star stars[starCount];
  
  for(uint8_t i = 0; i < LED_COUNT; i++) {
    strip.setPixelColor(i, strip.Color(0,0,0));
  }
  
  for(uint8_t i = 0; i < starCount; i++) {
    stars[i].draw();
  }
  strip.show();
}
  

void color_loop() {  
  static uint8_t i = 0;
  static int j = 0;
  static int f = 0;
  static int k = 0;
  static int count;

  float brightness = .9;
  
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    uint8_t red =   64*(1+sin(i/2.0 + j/4.0       ))*brightness;
    uint8_t green = 64*(1+sin(i/1.0 + f/9.0  + 2.1))*brightness;
    uint8_t blue =  64*(1+sin(i/3.0 + k/14.0 + 4.2))*brightness;
    
    uint32_t pix = green;
    pix = (pix << 8) | red;
    pix = (pix << 8) | blue;
    
    strip.setPixelColor(i, pix);
    
    if ((millis() - last_time > 15) && pixel_index <= LED_COUNT + 1) {
      last_time = millis();
      count = LED_COUNT - pixel_index;
      pixel_index++; 
    }
    
    for (int x = count; x >= 0; x--) {
      strip.setPixelColor(x, strip.Color(0,0,0));
    }
    
  }
  
  strip.show();
  
  j = j + random(1,2);
  f = f + random(1,2);
  k = k + random(1,2);
}


void strobe() {
  static uint8_t frame = 0;
  
  if (frame == 0) {
    for (int x = 0; x < LED_COUNT; x++) {
      strip.setPixelColor(x, strip.Color(0,0,0));
    }
    frame = 1;
  }
  else {
    for (int x = 0; x < LED_COUNT; x++) {
      strip.setPixelColor(x, strip.Color(24,24,24));
    }
    frame = 0;
  }
  
  strip.show();
  delay(59);
}

void serialLoop() {

  while(true) {

    if(Serial.available() > 2) {

      uint8_t buffer[3]; // Buffer to store three incoming bytes used to compile a single LED color

      for (uint8_t x=0; x<3; x++) { // Read three incoming bytes
        uint8_t c = Serial.read();
        
        if (c < 255) {
          buffer[x] = c; // Using 255 as a latch semaphore
        }
        else {
          strip.show();
          pixel_index = 0;
          break;
        }

        if (x == 2) {   // If we received three serial bytes
          strip.setPixelColor(pixel_index, strip.Color(buffer[0], buffer[1], buffer[2]));
          pixel_index++;
        }
      }
    }
  }
}

void loop()
{
  // If'n we get some data, switch to passthrough mode
  if(Serial.available() > 0) {
    serialLoop();
  }
  
  pov.draw(strip);
  delay(50);
  
//  star_loop();
  
//  strobe();
//  color_loop();
//  star_loop();
}



