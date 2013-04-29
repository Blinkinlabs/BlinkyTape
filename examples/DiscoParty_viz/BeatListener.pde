class BeatListener implements AudioListener
{
  private BeatDetect beat;
//  private AudioPlayer source;
  private AudioInput source;
  
//  BeatListener(BeatDetect beat, AudioPlayer source)
  BeatListener(BeatDetect beat, AudioInput source)
  {
    this.source = source;
    this.source.addListener(this);
    this.beat = beat;
  }
  
  void samples(float[] samps)
  {
    beat.detect(source.mix);
  }
  
  void samples(float[] sampsL, float[] sampsR)
  {
    beat.detect(source.mix);
  }
  
  void draw(PApplet p) {
    beat.drawGraph(p);
  }
}
