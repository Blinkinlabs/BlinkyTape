class LineTool {
  float startX, startY, endX, endY;
  int x, y, w, h;
  int size = 1;
  boolean active = false;

  PGraphics buff;
  PGraphics toolBuff;
  PImage img;

  public LineTool (PGraphics buff, ColorPicker cp, int x, int y, int w, int h) {
    this.buff = buff;
    this.toolBuff = createGraphics(buff.width, buff.height, JAVA2D);
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    img = buff.get(0, 0, buff.width, buff.height);
    toolBuff.beginDraw();
    toolBuff.background(img);
    toolBuff.endDraw();
  }

  protected void finalize() {
    img = toolBuff.get(0, 0, toolBuff.width, toolBuff.height);
    buff.background(img);
  }

  public void update() {
    if ( !mousePressed && active ) {
      finalize();
      active = false;
    }
    if ( mousePressed &&
      mouseX >= x && 
      mouseX < x + w &&
      mouseY >= y &&
      mouseY < y + h )
    {
      if (! active) {
        active = true;
        startX = screenToBuffX(mouseX);
        startY = screenToBuffY(mouseY);
      }
      endX = screenToBuffX(mouseX);
      endY = screenToBuffY(mouseY);
      img = buff.get(0, 0, buff.width, buff.height);
      toolBuff.beginDraw();
      toolBuff.background(img);
      toolBuff.strokeWeight(size);
      toolBuff.stroke(cp.c);
      toolBuff.line(startX, startY, endX, endY);
      toolBuff.endDraw();
    }
  }

  float screenToBuffX(float scrX) {
    return (scrX - x - 4) / (w/toolBuff.width);
  }

  float screenToBuffY(float scrY) {
    return (scrY - y - 4) / (h/toolBuff.height);
  }
}

