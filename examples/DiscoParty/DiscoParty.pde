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
AudioOutput audioout;  // Need to run soundflower for this to work...

FFT fft;
BeatDetect beat;
BeatListener bl;

ArrayList<LedOutput> leds = new ArrayList<LedOutput>();

float kickSize, snareSize, hatSize;

int numberOfLEDs = 60;
int[] values;

// A bunch of dynamic pulsers
ArrayList<Pulser> pulsers = new ArrayList<Pulser>();


// A couple of static pulsers
Pulser kickPulser;
Pulser hatPulser;


void setup()
{
  frameRate(30);
  size(15, 200, OPENGL);
//  size(screen.width, screen.height, OPENGL);

  println(this);
  minim = new Minim(this);
  audioin = minim.getLineIn(Minim.STEREO, 2048);

  
  leds.add(new LedOutput(this, "/dev/cu.usbmodemfd1221", numberOfLEDs));
  leds.add(new LedOutput(this, "/dev/cu.usbmodemfd1211", numberOfLEDs));

  //  song = minim.loadFile("Fog.mp3", 2048);
  //  song.play();
  // a beat detection object that is FREQ_ENERGY mode that 
  // expects buffers the length of song's buffer size
  // and samples captured at songs's sample rate
  //  beat = new BeatDetect(song.bufferSize(), song.sampleRate());
  beat = new BeatDetect(audioin.bufferSize(), audioin.sampleRate());

  // set the sensitivity to 300 milliseconds
  // After a beat has been detected, the algorithm will wait for 300 milliseconds 
  // before allowing another beat to be reported. You can use this to dampen the 
  // algorithm if it is giving too many false-positives. The default value is 10, 
  // which is essentially no damping. If you try to set the sensitivity to a negative value, 
  // an error will be reported and it will be set to 10 instead. 
  beat.setSensitivity(100);  
  kickSize = snareSize = hatSize = 16;
  // make a new beat listener, so that we won't miss any buffers for the analysis
  //  bl = new BeatListener(beat, song);  
  bl = new BeatListener(beat, audioin); 

  fft = new FFT(audioin.bufferSize(), audioin.sampleRate());
  fft.logAverages(10,1);

  for (int i = 0; i < fft.avgSize(); i++) {
    Pulser p = new Pulser();
    p.m_band = i;
    
//    if(random(0,1) > .5) {
//      p.m_h = 70;
//      p.m_s = random(100,100);
//      p.m_yv = random(.1,1.5);
//    }
//    else {
      p.m_h = 49;
      p.m_s = random(100,100);
      p.m_yv = random(-.1,-1.5);
//    }
    
    p.m_xv = 0;

    pulsers.add(p);
  }
  
//  kickPulser = new Pulser(width/2, height, 50);
//  kickPulser.m_band = 5;
//  kickPulser.m_falloff = .90;
//
//  hatPulser = new Pulser(width/2, 0, 50);
//  hatPulser.m_band = 18;
//  hatPulser.m_falloff = .90;

  textFont(createFont("Helvetica", 16));
  textAlign(CENTER);
}

float col = 0;

float backgroundAngle = 0;

void draw()
{
//  loadPixels();
  
//  background(color(1+cos(backgroundAngle), 
//  1+cos(backgroundAngle+6.28/3), 
//  1+cos(backgroundAngle+6.28*2/3)));
//  backgroundAngle += .01;

  background(0);

  fft.forward(audioin.mix);

  color(255);
  stroke(255);
  if ( beat.isKick() ) kickSize = min(32, kickSize+1.5);
  if ( beat.isSnare() ) snareSize = min(32, snareSize+1.5);
  if ( beat.isHat() ) hatSize = 32;

//  if ( hatSize == 32) {
//    col = col + 3.14159*.05;
//  }
//  for (int i = 0; i < numberOfLEDs/4 + 1; i++) {
//    float bright = (kickSize*2 - numberOfLEDs/2 - i)/8;
//    stroke(color((sin(col + i*.05              )+1)*128, 
//    (sin(col + i*.05 + 3.14159*2/3)+1)*128, 
//    (sin(col + i*.05 + 3.14159*4/3)+1)*128, 
//    bright*255
//      ));
//    point(0, numberOfLEDs/4+i);
//    point(0, numberOfLEDs/4-i);
//
//
//
//    bright = (snareSize*2 - numberOfLEDs/2 - i)/8;
//    stroke(color((sin(col + i*.05 + 3.14159*2/3)+1)*128, 
//    (sin(col + i*.05 + 3.14159*4/3)+1)*128, 
//    (sin(col + i*.05              )+1)*128, 
//    bright*255
//      ));
//    point(0, numberOfLEDs*3/4+i);
//    point(0, numberOfLEDs*3/4-i);
//  }

  if ( beat.isKick() ) {
      for(Pulser p : pulsers) {
        for(int i = 0; i < random(0,3); i++) {
          p.draw(fft);
        }
    }
  }
  
  background(0);

  for(Pulser p : pulsers) {
    p.draw(fft);
  }
  
//  pulsers.get(0).draw(fft);
  
//  kickPulser.draw(fft);
//  hatPulser.draw(fft);


  for(int i = 0; i < leds.size(); i++) {
    float pos = width/2 + 5*i;
    leds.get(i).sendUpdate(pos, 0, pos, height);
    
    stroke(255);
    line(pos, 0, pos, height);
  }

  float fadePercent = .98;
  kickSize  = constrain(kickSize  * fadePercent, 16, 32);
  snareSize = constrain(snareSize * fadePercent, 16, 32);
  hatSize   = constrain(hatSize   * fadePercent, 16, 32);
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

