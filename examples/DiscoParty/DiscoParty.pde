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

BeatDetect beat;
BeatListener bl;
LedOutput led;

float kickSize, snareSize, hatSize;

int numberOfChannels = 8*4;
int[] values;

void setup()
{
  frameRate(40);
  size(512, 200, P3D);
  
  minim = new Minim(this);
  audioin = minim.getLineIn(Minim.STEREO, 2048);
    
  led = new LedOutput(this, "/dev/cu.usbmodemfd121", 32);
  values = new int[numberOfChannels];
  
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
  
  textFont(createFont("Helvetica", 16));
  textAlign(CENTER);
}

int col = 0;

void draw()
{
  background(0);
  fill(255);
  if ( beat.isKick() ) kickSize = 32;
  if ( beat.isSnare() ) snareSize = 32;
  if ( beat.isHat() ) hatSize = 32;
  textSize(kickSize);
  text("KICK", width/4, height/2);
  textSize(snareSize);
  text("SNARE", width/2, height/2);
  textSize(hatSize);
  text("HAT", 3*width/4, height/2);
  
  for(int i = 0; i < numberOfChannels; i++) {
    switch(i%16) {
      case 0:
        values[i] = (int)((snareSize-16+.2)*2045);
        break;
      case 1:
        values[i] = (int)((kickSize-16)*2045);
        break;
      case 2:
        values[i] = (int)((hatSize-16+.2)*2045);
        break;
      case 8:
        values[i] = (int)((kickSize-16+.2)*2045);
        break;
      case 9:
        values[i] = (int)((hatSize-16+.2)*2045);
        break;
      case 10:
        values[i] = (int)((snareSize-16)*2045);
        break;
      default:
        values[i] = 0;
        break;
    }
    
//    bl.draw(this);
  }

  if( hatSize == 32) {
    col = (col+1)%3;
  }
    
  
  color colors[] = { color(255,255,0), color(0,255,255), color(255,0,255) };
  stroke(colors[col]);
  line(1,0,0,(kickSize - 16)*2);

  led.sendUpdate(0,0,0,32);
  
  float fadePercent = .95;
  kickSize = constrain(kickSize * fadePercent, 16, 32);
  snareSize = constrain(snareSize * fadePercent, 16, 32);
  hatSize = constrain(hatSize * fadePercent, 16, 32);

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
