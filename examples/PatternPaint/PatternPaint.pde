import processing.serial.*;
import controlP5.*;

ControlP5 controlP5;
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

  controlP5 = new ControlP5(this);
  controlP5.addNumberbox("toolSize")
    .setPosition(10,160)
    .setSize(100,15)
    .setRange(1, 50)
    .setScrollSensitivity(1)
    .setDirection(Controller.VERTICAL)
    .setValue(1)
    .setId(1)
    .getCaptionLabel().align(ControlP5.LEFT, ControlP5.TOP_OUTSIDE).setPaddingX(0);

  controlP5.addButton("pause")
    .setPosition(10, 185)
    .setSize(100,15)
    .setId(2);

  controlP5.addButton("load_image")
    .setPosition(10, 210)
    .setSize(100,15)
    .setId(3);

  controlP5.addButton("save_to_strip")
    .setPosition(10, 230)
    .setSize(100,15)
    .setId(4);
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
  drawBuffer();
  tool.update();
  drawPos();
  updatePos();
  led.sendUpdate(buffer, pos, 0, pos, buffer.height);
}

void keyPressed() {
  println("Pressed " + keyCode);
    
    switch(keyCode) {
  case 32:
    pause(0);
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
  println("Saved to 'pov.h'");
}

void importImage() {
  String imgPath = selectInput("Select a file to import (120x60)");
  if (imgPath != null) {
    PImage img = loadImage(imgPath);
    buffer.beginDraw();
    buffer.image(img, 0, 0, buffer.width, buffer.height);
    buffer.endDraw();
    // reinit tool to get new buffer
    tool = new LineTool(buffer, cp, buffOffX, buffOffY, buffScale * buffer.width, buffScale * buffer.height);
  }
}

/** ControlP5 callbacks */
void toolSize(int newSize){
  tool.size = newSize;
}

void pause(int val){
  scanning = !scanning;
  if (rate == 0) {
    scanning = true;
    rate = 1;
  }
}

void load_image(int val){
  importImage();
}

void save_to_strip(int val){
  savePattern();
}
