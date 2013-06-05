import processing.serial.*;
import controlP5.*;
//import processing.opengl.*;
//import javax.media.opengl.GL;

ControlP5 controlP5;
LedOutput led = null;

PFont myFont;
ColorPicker cp;

PGraphics buffer;
PImage img;
int buffOffX = 120;
int buffOffY = 10;
int buffScale = 6;

LineTool tool;

void setup() {
  buffer = createGraphics(60, 60, JAVA2D);
  size(windowWidthForBuffer(buffer), 380, JAVA2D);

//  noSmooth();
//  // Turn on vsync to prevent tearing
//  PGraphicsOpenGL pgl = (PGraphicsOpenGL) g; //processing graphics object
//  GL gl = pgl.beginGL(); //begin opengl
//  gl.setSwapInterval(2); //set vertical sync on
//  pgl.endGL(); //end opengl
  
  frameRate(60);
  frame.setResizable(true);

  cp = new ColorPicker( 10, 10, 100, 100, 255 );
  myFont = createFont("FFScala", 12);
  textFont(myFont);
  drawInitialArt();

  tool = new LineTool(buffer, cp,
                      buffOffX, buffOffY,
                      buffScale * buffer.width,
                      buffScale * buffer.height);
                      
  for(String p : Serial.list()) {
//    if(p.startsWith("/dev/cu.usbmodem")) {
//      led = new LedOutput(this, p, 60);
//      break;  // TODO: does this work?
//    }
  }

  controlP5 = new ControlP5(this);

  controlP5.Slider s = controlP5.addSlider("toolSize")
    .setPosition(10,160)
    .setSize(100,15)
    .setRange(1, 50)
    .setValue(1)
    .setId(1);  
  s.getValueLabel()
      .align(ControlP5.RIGHT,ControlP5.CENTER);
  s.getCaptionLabel()
      .align(ControlP5.LEFT,ControlP5.CENTER);

  controlP5.Slider speed = controlP5.addSlider("speed")
    .setPosition(10,190)
    .setSize(100,15)
    .setRange(0, 5)
    .setValue(1)
    .setId(2);
  speed.getValueLabel()
      .align(ControlP5.RIGHT,ControlP5.CENTER);
  speed.getCaptionLabel()
      .align(ControlP5.LEFT,ControlP5.CENTER);

  controlP5.addButton("pause")
    .setPosition(10, 215)
    .setSize(100,15)
    .setId(3);

  controlP5.addButton("load_image")
    .setPosition(10, 235)
    .setSize(100,15)
    .setId(4)
    .getCaptionLabel().set("Load PNG Image");

  controlP5.addButton("save_as_png")
    .setPosition(10, 265)
    .setSize(100,15)
    .setId(5)
    .getCaptionLabel().set("Save PNG Image");

  controlP5.addButton("save_to_strip")
    .setPosition(10, 295)
    .setSize(100,15)
    .setId(5)
    .getCaptionLabel().set("Save to BlinkyTape");
    
    
}

float pos = 0;
boolean scanning = true;
float rate = 1;

void draw() {
  background(80);

  cp.render();
  drawBuffer();
  tool.update();
  drawPos();
  updatePos();
  
  drawCrosshair();
  
  if(led != null) {
    led.sendUpdate(buffer, pos, 0, pos, buffer.height);
  }
}

void keyPressed() {
  switch(keyCode) {
    case KeyEvent.VK_SPACE:
      pause(0);
      break;
    case KeyEvent.VK_LEFT:
      pos--; 
      if (pos < 0) {
        pos = buffer.width - 1;
      }
      break;
    case KeyEvent.VK_UP:
      rate+=.2;
      scanning = true;
      break;
    case KeyEvent.VK_RIGHT:
      pos++; 
      if (pos >= buffer.width) {
        pos = 0;
      }
      break;
    case KeyEvent.VK_DOWN:
      rate-=.2; 
      if (rate < 0) {
        rate = 0;
      }
      break;
    case KeyEvent.VK_S: // save
      savePattern();
      break;
    case KeyEvent.VK_O: // open
      importImage();
      break;
    case KeyEvent.VK_L: // launch, for testing
      launchProcess();
      break;
  }
}

int windowWidthForBuffer(PGraphics buff) {
  return  (buffScale * buff.width) + buffOffX + 10;
}

void drawInitialArt() {
  buffer.beginDraw();
  buffer.noSmooth();
  buffer.background(0);
  buffer.endDraw();
}

void drawBuffer() {
  noSmooth();  
  //img = buffer.get(0,0, buffer.width, buffer.height);
  img = tool.toolBuff.get(0, 0, buffer.width, buffer.height);
  image(img, buffToScreenX(0), buffToScreenY(0),
        buffScale * buffer.width, buffScale * buffer.height);
  // draw a nice grid to show the pixel separation
  stroke(80);
  for (int x = 0; x < buffer.width; x++) {
    line(buffToScreenX(x), buffToScreenY(0),
         buffToScreenX(x), buffToScreenY(buffer.height));
  }
  for (int y = 0; y < buffer.height; y++) {
    line(buffToScreenX(0), buffToScreenY(y),
         buffToScreenX(buffer.width), buffToScreenY(y));
  }
}

void drawPos() {
  fill(255, 64);
  stroke(255);
  rect(buffToScreenX(pos), buffToScreenY(0),
       buffScale, (buffScale* buffer.height) - 1);
}

void drawCrosshair() {
  pushStyle();
    noStroke();
    fill(255, 32);
    if(screenToBuffX(mouseX) > -1 && screenToBuffY(mouseY) > -1) {
      rect(buffToScreenX(screenToBuffX(mouseX)), buffToScreenY(0),
           buffScale+1, (buffScale* buffer.height)+1);
      rect(buffToScreenX(0), buffToScreenY(screenToBuffY(mouseY)),
           (buffScale* buffer.width)+1, buffScale+1);
    }
  popStyle();
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

float screenToBuffX(float screenX) {
  int buffX = (int)((screenX - buffOffX)/buffScale);
  if ((buffX < 0) | (buffX > buffer.width)) {
    return -1;
  }
  return buffX;
}

float screenToBuffY(float screenY) {
  int buffY = (int)((screenY - buffOffY)/buffScale);
  if ((buffY < 0) | (buffY > buffer.height)) {
    return -1;
  }
  return buffY;
}

void savePattern() {
  LedSaver saver = new LedSaver("pov", 60);
  for (int x = 0; x < buffer.width; x++) {
    saver.addFrame(buffer, x, 0, x, buffer.height);
  }
  saver.write16bitRLE();
  saver.write16bitRLEHex();
  println("Saved to 'pov.h'");
}

void launchProcess() {
  savePattern();
  ProcessLauncher p = new ProcessLauncher(sketchPath("program.sh") + " " + "/dev/cu.usbmodemfa131");
  delay(100);
  print(p.read());
}

void importImage() {
  String imgPath = selectInput("Select an imagefile to import");
  if (imgPath != null) {
    PImage img = loadImage(imgPath);
    // create a new buffer to fit this image
    buffer = createGraphics(img.width, img.height, JAVA2D);
    buffer.beginDraw();
    buffer.image(img, 0, 0, buffer.width, buffer.height);
    buffer.endDraw();
    // reinit tool to get new buffer
    tool = new LineTool(buffer, cp, buffOffX, buffOffY,
                        buffScale * buffer.width,
                        buffScale * buffer.height);
    // resize the window frame
    frame.setSize(windowWidthForBuffer(buffer), height);
    // reset scrubber
    pos = 0;
  }
}

void saveAsImage() {
  String imgPath = selectOutput("Save PNG file");
  if(imgPath != null) {
    PImage img = buffer.get(0, 0, buffer.width, buffer.height);
    img.save(imgPath);
    println("Saved PNG file to '" + imgPath + "'.");
  }
}

/** ControlP5 callbacks */
void toolSize(int newSize){
  tool.size = newSize;
}

void speed(float newSpeed){
  rate = newSpeed;
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

void save_as_png(int val){
  saveAsImage();
}

void save_to_strip(int val){
  savePattern();
}
