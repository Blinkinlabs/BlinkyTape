import processing.serial.*;
LedOutput led;

PFont myFont;
ColorPicker cp;

PGraphics buffer;
PImage img;
int buffOffX = 120;
int buffOffY = 10;
int buffScale = 6;

LineTool tool;

void setup() {
  buffer = createGraphics(120, 60, JAVA2D);

  size((buffScale * buffer.width) + buffOffX + 10, 500, JAVA2D);
  frameRate(60);

  cp = new ColorPicker( 10, 10, 100, 100, 255 );
  myFont = createFont("FFScala", 12);
  textFont(myFont);
  drawInitialArt();

  tool = new LineTool(buffer, cp, buffOffX, buffOffY, buffScale * buffer.width, buffScale * buffer.height);
  led = new LedOutput(this, "/dev/cu.usbmodem1d11", 60);
}

float pos = 0;
boolean scanning = true;
float rate = 1;

void drawInitialArt() {
  buffer.beginDraw();
  buffer.noSmooth();
  buffer.background(0);
  buffer.endDraw();
}

void draw() {
  background(80);

  cp.render();
  drawToolState(tool);
  drawBuffer();
  tool.render();
  drawPos();
  updatePos();
  led.sendUpdate(buffer, pos, 0, pos, buffer.height);
}

void keyPressed() {
  println("Pressed " + keyCode);
    
    switch(keyCode) {
  case 32:
    scanning = !scanning;
    if (rate == 0) {
      scanning = true;
      rate = 1;
    }
    break;
  case 37:
    pos--; 
    if (pos < 0) pos = buffer.width - 1;
    break;
  case 38:
    rate++;
    scanning = true;
    break;
  case 39:
    pos++; 
    if (pos >= buffer.width) pos = 0;
    break;
  case 40:
    rate--; 
    if (rate < 0) rate = 0;
    break;
  case 45: // -
    tool.size -= 1; 
    if (tool.size < 1) tool.size = 1;
    break;
  case 61: // +
    tool.size += 1;
    break;
  case 83: // save
    savePattern();
    break;
  case 79: // open
    importImage();
    break;
  }
}

void drawBuffer() {
  noSmooth();  
  //img = buffer.get(0,0, buffer.width, buffer.height);
  img = tool.toolBuff.get(0, 0, buffer.width, buffer.height);
  image(img, buffToScreenX(0), buffToScreenY(0), buffScale * buffer.width, buffScale * buffer.height);
  // draw a nice grid to show the pixel separation
  stroke(80);
  for (int x = 0; x < buffer.width; x++) {
    line(buffToScreenX(x), buffToScreenY(0), buffToScreenX(x), buffToScreenY(buffer.height));
  }
  for (int y = 0; y < buffer.height; y++) {
    line(buffToScreenX(0), buffToScreenY(y), buffToScreenX(buffer.width), buffToScreenY(y));
  }
}

void drawPos() {
  stroke(255, 255);
  fill(255, 64);
  rect(buffToScreenX(pos), buffToScreenY(0), buffScale, (buffScale* buffer.height) - 1);
}

void drawToolState(LineTool tool) {
  fill(255, 255);
  text("Line Size: " + tool.size
    + "\n    +/- to adjust", 10, 150, 100, 100);
}

void updatePos() {
  if (scanning)
    pos = (pos + rate) % buffer.width;
}

float buffToScreenX(float buffX) {
  return (buffScale * buffX) + buffOffX;
}

float buffToScreenY(float buffY) {
  return (buffScale * buffY) + buffOffY;
}

void savePattern() {
  LedSaver saver = new LedSaver("pov", 60);
  for (int x = 0; x < buffer.width; x++) {
    saver.sendUpdate(buffer, x, 0, x, buffer.height);
  }
  saver.write16bitRLE();
}

void importImage() {
  String imgPath = selectInput("Select a file to import (120x60)");
  if (imgPath != null) {
    PImage img = loadImage(imgPath);
    buffer.beginDraw();
    buffer.image(img, 0, 0, buffer.width, buffer.height);
    buffer.endDraw();
  }
}


