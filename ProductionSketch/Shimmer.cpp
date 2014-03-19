#include "Shimmer.h"
#include "BlinkyTape.h"

#include <Arduino.h>

//light champagne
float light_champagne_r = 1.0000;
float light_champagne_g = 0.9352;
float light_champagne_b = 0.8340;

//medium champagne
float medium_champagne_r = 1.0000;
float medium_champagne_g = 0.9412;
float medium_champagne_b = 0.7020;

void Shimmer::SetColorTemperature(uint8_t newColorTemperature) {
  //set color temp
  if (newColorTemperature == 0)
  {
    color_temp_factor_r = 1.0; // cool white
    color_temp_factor_g = 1.0;
    color_temp_factor_b = 1.0;
  }
  else if (newColorTemperature == 1)
  {
    color_temp_factor_r = light_champagne_r;
    color_temp_factor_g = light_champagne_g;
    color_temp_factor_b = light_champagne_b;    
  }
  else // color_temp == 2
  {
    color_temp_factor_r = medium_champagne_r;
    color_temp_factor_g = medium_champagne_g;
    color_temp_factor_b = medium_champagne_b;    
  }
}

void Shimmer::reset() {
  
    //Shimmer initiation
  for (uint8_t i = 0; i < LED_COUNT; i++)
  {
    value[i] = 0.0;
    maxValue[i] = random(ledMax);
    death[i] = maxValue[i] + (stepSize / 2) + (0.5 * random(ledMax));
    direction[i] = 1;
  }
  
  SetColorTemperature(colorTemperature);
}

Shimmer::Shimmer(uint8_t newColorTemperature) :
  stepSize(5),
  ledMax(255),
  colorTemperature(newColorTemperature) {
}

void Shimmer::draw(CRGB* leds) { 
  //  static uint8_t i = 0;
  //  int done = 0;
  int accelerated_step = 0;
  float unit = 0;

  //static int pixelIndex;

  for (int i = 0; i < LED_COUNT; i++) {
    unit = maxValue[i] / (float)ledMax;
    accelerated_step = (float)stepSize + ((float)ledMax * (0.015 * (float)stepSize * unit * unit * unit * unit));

    if (direction[i] == 1) {
      if (value[i] < maxValue[i]) {
        //value[i] += stepSize;
        value[i] = value[i] + accelerated_step;

        //error checking
        if (value[i] > ledMax) {
          value[i] = ledMax;
        }

        leds[i].r = (int)(value[i] * color_temp_factor_r);
        leds[i].g = (int)(value[i] * color_temp_factor_g);
        leds[i].b = (int)(value[i] * color_temp_factor_b);
      }
      else {
        direction[i] =0;
      }
    }
    else {
      if (value[i] > 0) {
        death[i] = death[i] - stepSize;
        value[i] = value[i] - stepSize;

        //error checking
        if (value[i] < 0) {
          value[i] = 0;
        }

        leds[i].r = (int)(value[i] * color_temp_factor_r);
        leds[i].g = (int)(value[i] * color_temp_factor_g);
        leds[i].b = (int)(value[i] * color_temp_factor_b);  
      }
      else {
        death[i] = death[i] - stepSize;        
        if (death[i] < 0)
        {
          direction[i] = 1;
          maxValue[i] = random(ledMax);
          death[i] = maxValue[i] + (stepSize / 2) + (0.5 * random(ledMax));
        }
      }
    }
  } // end for
    
  delay(30);  // TODO: Don't place me here
} // end shimmer_update_loop

