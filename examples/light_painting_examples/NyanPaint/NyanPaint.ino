/**
 * Light Painting with NyanCat and Blinkytube!
 * Usage:
 *  1. Power up the Blinkytube. The rainbow animation will begin cycling
 *  2. Pressing the button will finalize the painting by drawing Nyancat, then stopping
 *  3. Press button again to return to rainbow mode.
 *
 *  Adjust anim_delay_my below to tweak timing.
 */

#ifndef _NEOPIXEL_H
#define _NEOPIXEL_H
#include <Adafruit_NeoPixel.h>
#endif

#include "animation.h"
#include "nyan_rainbow.h"
#include "nyan_cat.h"

#define LED_COUNT 60
#define THRESHOLD 1

Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_COUNT, 5, NEO_GRB + NEO_KHZ800);

uint8_t pixel_index;
long last_time;

uint8_t btn_pin = 13;

#define ANI_RAINBOW 0
#define ANI_CAT 1
#define ANI_DONE 2
uint8_t state = ANI_RAINBOW;
boolean switch_states = false;
long btn_up_time = 0;
long state_time = 0;
uint8_t anim_delay_ms = 10;

void setup()
{ 
  Serial.begin(57600);

  strip.begin();
  strip.show();
  last_time = millis();

  pinMode(btn_pin, INPUT);
  digitalWrite(btn_pin, HIGH);
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

  if(digitalRead(btn_pin) == 0 && btn_up_time > state_time){
    switch_states = true;
    Serial.println("BUTTON!!");
  } else {
    btn_up_time = millis();
  }
  switch(state) {
    case ANI_RAINBOW:
      rainbow.draw(strip);
      if(switch_states && rainbow.isDone()){
        state = ANI_CAT;
        switch_states = false;
        state_time = millis();
      }
      delay(anim_delay_ms);
      break;
    case ANI_CAT:
      nyancat.draw(strip);
      if(nyancat.isDone()){
        state = ANI_DONE;
        switch_states = false;
        state_time = millis();
      }
      delay(anim_delay_ms);
      break;
    default:
      if(switch_states) {
        state = ANI_RAINBOW;
        switch_states = false;
        state_time = millis();
      }
      delay(100);
  }
  
}




