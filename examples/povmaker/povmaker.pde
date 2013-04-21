import processing.serial.*;
LedOutput led;

LedSaver saver;

PFont myFont;

void setup() {
  size(400, 60, P2D);
  frameRate(60);

  led = new LedOutput(this, "/dev/cu.usbmodemfd121", 60);
  
  saver = new LedSaver("pov", 60);
  
  myFont = createFont("FFScala", 50);
}

float pos = 0;
float rate = 2;

void draw() {
  background(0);
  
  fill(255,0,0);
  rect(0,0,15,height);
  rect(30,0,15,height);
  
  String message = new String("Blinkiverse!");
  textFont(myFont);

  fill(155,0,255);
  text(message, 100, 48);

  fill(0,255,255);
  text(message, 105, 53);


//  led.sendUpdate(pos,height-1,pos,0);
  saver.sendUpdate(pos,height-1,pos,0);

  stroke(255,128);
  line(pos, 0,pos, height);
  
//  rate = (float)mouseX/width*4;
  pos = (pos + rate)%width;
  
  if(pos< rate) {
    saver.writeRLE();
  }
}
