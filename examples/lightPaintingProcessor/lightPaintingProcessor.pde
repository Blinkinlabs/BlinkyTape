int imageX = 1920;
int imageY = 1080;

PGraphics brightImage;

ArrayList<File> filesList;
int index = 0;

String inputPath;

ArrayList filesToArrayList(String folderPath) {
  ArrayList<File> filesList = new ArrayList<File>();
  if (folderPath != null) {
    File file = new File(folderPath);
    
    File[] files = file.listFiles();
    
    if(files != null) {
      for (File f : files) {
        filesList.add(f);
      }
    }
  }
  return(filesList);
}

void setup() {
  frameRate(999);
  
  size(imageX/2, imageY/2); // Change size to 320 x 240 if too slow at 640 x 480
  strokeWeight(5);
  
  brightImage = createGraphics(imageX, imageY, P2D);

  inputPath = sketchPath("") + "inputFrames/";
  println(inputPath);
  filesList = filesToArrayList(inputPath);
  for(File f : filesList){
    println(f.getName());
  }
  
  noCursor();
}

void draw() {
  if(index < filesList.size()) {
    println(filesList.get(index).getName());
    PImage inFrame = loadImage(inputPath + filesList.get(index).getName());

    inFrame.loadPixels();
    
    brightImage.beginDraw();
    
    loadPixels();
    for (int i = 0; i < imageX*imageY; i++) {
      float videoBrightness = brightness(inFrame.pixels[i]);
      float imageBrightness = brightness(brightImage.pixels[i]);      
      
      if (videoBrightness > imageBrightness | index == 0) { // If the pixel is brighter than the
        brightImage.pixels[i] = inFrame.pixels[i]; // threshold value, make it white
      } 
      else { // Otherwise,
        // nothing.
      }
    }
    brightImage.endDraw();
    image(brightImage,0,0,width,height);
    brightImage.save("outputFrames/out" + filesList.get(index).getName());
 
    index++;
  }
}

