import processing.opengl.*;
 
// Draw a rectangle which can have differently colored edges
// @param x X coordinate of the top-left corner of the rectangle (pixels)
// @param y X coordinate of the top-left corner of the rectangle (pixels)
// @param widt Width of the rectangle (pixels)
// @param heigh Height of the rectangle (pixels)
// @param tlcolor Color of the top-left rectangle corner
// @param trcolor Color of the top-right rectangle corner
// @param brcolor Color of the bottom-right rectangle corner
// @param blcolor Color of the bottom-left rectangle corner
// 
void makeRectangle(int x, int y, int widh, int heigh,
                   color tlcolor, color trcolor,
                   color brcolor, color blcolor) {
  beginShape(POLYGON);
    fill(tlcolor);
      vertex(x, y);
    fill(trcolor);
      vertex(x+widh, y);
    fill(brcolor);
      vertex(x+widh, y+heigh);
    fill(blcolor);
      vertex(x, y+heigh);
  endShape(CLOSE);
}
 
// Draw a gradient corner by making triangles
// TODO: do this directly somehow; a shader?
// @param x X coordinate of the center of the semicircle (pixels)
// @param y Y coordinate of the center of the semicircle (pixels)
// @param rad Radius of the semicircle (pixels)
// @param divisions Number of triangle divisions to make (more=smoother)
// @param quadrant Which quadrant to draw in 
// @param insideColor Color to use for the center of the semicircle
// @param outsideColor Color to use for the outside of the semicircle
void makeGradientCorner(int x, int y, int rad,
                int divisions, int quadrant,
                color insideColor, color outsideColor) {
  beginShape(TRIANGLES); 
    for(float angle = quadrant*PI/2;
        angle < (quadrant + 1)*PI/2 - .001;
        angle += PI/divisions/2) {
      fill(insideColor);
        vertex(x, y);
      fill(outsideColor);
        vertex(x+cos(angle)*rad,                y-sin(angle)*rad);
        vertex(x+cos(angle+PI/divisions/2)*rad, y-sin(angle+PI/divisions/2)*rad);
    }
  endShape(CLOSE);
}
 
// Draw a fuzzy rectangle at the specified position
// @param x X coordinate of the top-left corner of the rectangle (pixels)
// @param y X coordinate of the top-left corner of the rectangle (pixels)
// @param widt Width of the rectangle (pixels)
// @param heigh Height of the rectangle (pixels)
// @param radius Radius of the fuzzing (pixels)
// @param fgcolor color of the rectangle
void drawFuzzyRectangle(int x, int y, int widt, int heigh,
                        int rad, color fgcolor, color bgcolor) {
  // Handle the case where the radius is too big, by clipping it to 1/2 the max height or width.
  int max_rad = int(min(widt/2, heigh/2));
  rad = min(rad, max_rad);
 
  // Uncomment this to see how the gradients are being drawn
  //stroke(0);
 
  makeRectangle(x+rad, y+rad,        widt-2*rad, heigh-2*rad, fgcolor, fgcolor, fgcolor, fgcolor);
  makeRectangle(x+rad, y,            widt-2*rad, rad,   bgcolor, bgcolor, fgcolor, fgcolor);
  makeRectangle(x, y+rad,            rad, heigh-2*rad,  bgcolor, fgcolor, fgcolor, bgcolor);
  makeRectangle(x+rad, y+rad+heigh-2*rad,  widt-2*rad, rad,   fgcolor, fgcolor, bgcolor, bgcolor);
  makeRectangle(x+widt-rad, y+rad,   rad, heigh-2*rad,  fgcolor, bgcolor, bgcolor, fgcolor);
  makeGradientCorner(x+widt-rad, y+rad,       rad, 8,  0,   fgcolor, bgcolor);
  makeGradientCorner(x+rad, y+rad,            rad, 8,  1,   fgcolor, bgcolor);
  makeGradientCorner(x+rad, y+heigh-rad,      rad, 8,  2,   fgcolor, bgcolor);
  makeGradientCorner(x+widt-rad, y+heigh-rad, rad, 8,  3,   fgcolor, bgcolor);
}
