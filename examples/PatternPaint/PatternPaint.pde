import processing.serial.*;
LedOutput led;

PFont myFont;
ColorPicker cp;

PGraphics buffer;
PImage img;
int buffOffX = 120;
int buffOffY = 10;
int buffScale = 6;

void setup() {
  buffer = createGraphics(120, 60, JAVA2D);
  
  size((buffScale * buffer.width) + buffOffX + 10, 500, JAVA2D);
  frameRate(60);

  led = new LedOutput(this, "/dev/cu.usbmodem1a21", 60);
  
  myFont = createFont("FFScala", 50);
  cp = new ColorPicker( 10, 10, 100, 100, 255 );
  drawInitialArt();
}

float pos = 0;
boolean scanning = true;
float rate = 1;

void drawInitialArt() {
  buffer.beginDraw();
  buffer.noSmooth();
  buffer.background(0);
  /*
  buffer.fill(255,0,0);
  buffer.stroke(255,0,0);
  buffer.rect(0,0,15,buffer.height);
  buffer.rect(30,0,15,buffer.height);
  String msg = new String("Blinkiverse");
  buffer.textFont(myFont);
  buffer.fill(155,0,255);
  buffer.text(msg, 100, 48);
  buffer.fill(0,255,0);
  buffer.text(msg, 105, 53);
  */
  buffer.endDraw();
}

void draw() {
  background(80);

  cp.render();
  drawBuffer();
  updateBuffer();
  drawPos();
  updatePos();
  led.sendUpdate(buffer, pos, 0, pos, buffer.height);  
}

void keyPressed() {
  println("Pressed " + int(key) + " " + keyCode);  
  switch(keyCode){
    case 32:
      scanning = !scanning;
      if(rate == 0) {
        scanning = true;
        rate = 1;
      }
      break;
    case 37:
      pos--; if(pos < 0) pos = buffer.width - 1;
      break;
    case 38:
      rate++;
      scanning = true;
      break;
    case 39:
      pos++; if(pos >= buffer.width) pos = 0;
      break;
    case 40:
      rate--; if(rate < 0) rate = 0;
      break;
  }
}

void drawBuffer() {
  noSmooth();  
  img = buffer.get(0,0, buffer.width, buffer.height);
  image(img, buffToScreenX(0), buffToScreenY(0), buffScale * buffer.width, buffScale * buffer.height);
}

void drawPos() {
  stroke(255,255);
  fill(255,64);
  rect(buffToScreenX(pos), buffToScreenY(0), buffScale, (buffScale* buffer.height) - 1);
}

void updatePos() {
  if(scanning)
    pos = (pos + rate) % buffer.width; 
}

void updateBuffer() {
 if( mousePressed )
 {
   float buffX = screenToBuffX(mouseX - 4);
   float buffY = screenToBuffY(mouseY - 3);
   if(buffX >= 0 && 
     buffX < buffer.width &&
     buffY >= 0 &&
     buffY < buffer.height )
    {
      buffer.beginDraw();
      buffer.noSmooth();
      buffer.stroke(cp.c);
      buffer.point(buffX, buffY);
      buffer.endDraw();
    }
  }
}

float buffToScreenX(float buffX){
  return (buffScale * buffX) + buffOffX;
}

float buffToScreenY(float buffY){
  return (buffScale * buffY) + buffOffY;
}

float screenToBuffX(float scrX){
  return (scrX - buffOffX) / buffScale;
}

float screenToBuffY(float scrY){
  return (scrY - buffOffY) / buffScale;
}
