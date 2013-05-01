Note: The included mencoder is for OS/X only, sorry. It's easy to install in Linux ;-)

mkdir inputFrames outputFrames

To devolve a video into stills (in the inputFrames directory):
mplayer -vo png -nosound MVI_9103.MOV

And stills back to a video:
./mencoder \
-of lavf -lavfopts format=mp4 -sws 9 -af volnorm -srate 44100 -channels 2 \
-vf-add harddup -oac faac -faacopts br=96:mpeg=4:object=2:raw \
-ovc x264 -x264encopts crf=24:threads=2:level_idc=13:bframes=0:frameref=2:nocabac:global_header:partitions=all \
mf://outputFrames/*.png -mf w=800:h=600:fps=25:type=png \
-o output.MOV

