import processing.opengl.*;

import processing.serial.*;

/**
 * This sketch demonstrates how to use the BeatDetect object in FREQ_ENERGY mode.<br />
 * You can use <code>isKick</code>, <code>isSnare</code>, </code>isHat</code>, <code>isRange</code>, 
 * and <code>isOnset(int)</code> to track whatever kind of beats you are looking to track, they will report 
 * true or false based on the state of the analysis. To "tick" the analysis you must call <code>detect</code> 
 * with successive buffers of audio. You can do this inside of <code>draw</code>, but you are likely to miss some 
 * audio buffers if you do this. The sketch implements an <code>AudioListener</code> called <code>BeatListener</code> 
 * so that it can call <code>detect</code> on every buffer of audio processed by the system without repeating a buffer 
 * or missing one.
 * <p>
 * This sketch plays an entire song so it may be a little slow to load.
 */

import ddf.minim.*;
import ddf.minim.analysis.*;

Minim minim;
AudioPlayer song;
AudioInput audioin;

FFT leftFft;
FFT rightFft;

ArrayList<LedOutput> leds = new ArrayList<LedOutput>();

float kickSize, snareSize, hatSize;

int numberOfLEDs = 60;
int[] values;

Pulser leftPulser;
Pulser rightPulser;

ArrayList<Pulser> bgPulsers = new ArrayList<Pulser>();

void setup()
{
  frameRate(30);
  size(400, 200, OPENGL);

  println(this);
  minim = new Minim(this);
  audioin = minim.getLineIn(Minim.STEREO, 2048);

  leds.add(new LedOutput(this, "/dev/cu.usbmodemfa131", numberOfLEDs));
//  leds.add(new LedOutput(this, "/dev/cu.usbmodemfd121", numberOfLEDs));
//  leds.add(new LedOutput(this, "/dev/cu.usbmodemfa131", numberOfLEDs));

  leftFft = new FFT(audioin.bufferSize(), audioin.sampleRate());
  leftFft.logAverages(100,1);
  
  rightFft = new FFT(audioin.bufferSize(), audioin.sampleRate());
  rightFft.logAverages(100,1);
  
  for (int i = 0; i < leftFft.avgSize(); i++) {
    Pulser p = new Pulser();
    p.m_band = i;
    p.m_x = width/4;
    p.m_size = 10;
    p.m_scale = 1;
    
    if(random(0,1) > .5) {
      p.m_h = 70;
      p.m_s = 100;
      p.m_yv = random(.2,2);
    }
    else {
      p.m_h = 49;
      p.m_s = 100;
      p.m_yv = random(-.2,-2);
    }
    
    p.m_xv = 0;

    bgPulsers.add(p);
  }

  leftPulser = new Pulser();
    leftPulser.m_band  = 1;
    leftPulser.m_h     = 5;
    leftPulser.m_s     = 60;
    leftPulser.m_size  = 5;
    leftPulser.m_scale = 18;
    leftPulser.m_x     = width/4;
    leftPulser.m_y     = 56;
    leftPulser.m_xv    = 0;
    leftPulser.m_yv    = 0;
  
  rightPulser = new Pulser();
    rightPulser.m_band  = 1;
    rightPulser.m_h     = 96;
    rightPulser.m_s     = 60;
    rightPulser.m_size  = 5;    
    rightPulser.m_scale = 18; 
    rightPulser.m_x     = width/4;
    rightPulser.m_y     = 155;
    rightPulser.m_xv    = 0;
    rightPulser.m_yv    = 0;
}

float col = 0;

float backgroundAngle = 0;

void draw()
{
  background(0);

  leftFft.forward(audioin.left);
  rightFft.forward(audioin.right);

  color(255);
  stroke(255);

  for(Pulser p : bgPulsers) {
    p.draw(leftFft);
  }
  
  leftPulser.draw(leftFft);
  rightPulser.draw(rightFft);

  for(int i = 0; i < leds.size(); i++) {
    float pos = width/4 + i*width/2;
    leds.get(i).sendUpdate(pos, 0, pos, height);
    
    stroke(255);
    line(pos, 0, pos, height);
  }
  
}

void stop()
{
  // always close Minim audio classes when you are finished with them
  //  song.close();
  audioin.close();

  // always stop Minim before exiting
  minim.stop();
  // this closes the sketch
  super.stop();
}

