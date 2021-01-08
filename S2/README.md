# SCAV-S2
In this README document you'll find the guidelines to the given exercices as well as the pertinent results and comments. For the scripts, the code is explained inside the .py files.

**NOTE: The Big Buck Bunny video is not included in the repo and its refered as `BBB.mp4` in the code**. You can find it in http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_60fps_normal.mp4 

## 1. Cut 10 seconds of the BBB video
To cut the original video into a shorter 10 second clip we use the following command

 `ffmpeg -ss 00:00:30.0 -i BBB.mp4 -c copy -t 00:00:10.0 10BBB.mp4`

We use the `-ss` option to specify a start timestamp, and the `-t` option to specify the encoding duration. This command clips the first 30 seconds, and then clips everything that is 10 seconds after that and saves the output in the 10 second .mp4 file `10BBB.mp4`.

## 2. Extract the YUV histogram from the previous 10 second video and overlap them
We use the following command  <br>
`fmpeg -i 10BBB.mp4 -vf “split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay” -c:v libx264 -crf 18 -preset veryslow -c:a copy hist10BBB.mp4`

The main aspect about the overlayed histograms is the use of the split, format, histogram, and overlay filters. The split makes two copies of the input: one for the histogram and the other for the overlay. The histogram computes the histogram of the 3 channels and then formats as a chroma 4:4:4 progressive. Then, through the overlay we place the histogram over the copy of the original image.

Another thing we are interested in is getting a "visually lossless" quality. To do this, we use the `-crf` option. The range of the quantizer scale is 0-51: where 0 is lossless, 23 is default, and 51 is worst possible. We consider 18 to be visually lossless or nearly so: it should look the same or nearly the same as the input but it isn't technically lossless.
You control the tradeoff between video encoding speed and compression efficiency with the `-preset` options. The veryslow option offers the best compression efficiency (resulting in a smaller file size for the same quality) but it is very slow – as the name says. The audio will be stream copied directly from the input file to the output file without any changes.

## 3. Resize the BBB video into 4 differents video outputs
* **720p** <br>
To scale the video to 720p we use <br>
`ffmpeg -i 10BBB.mp4 -vf scale=-1:720 -c:v libx264 -crf 18 -preset veryslow -c:a copy 720p_10BBB.mp4` <br>
The scale video filter is for resizing the video. We set the height to 720p and use -1 for the other dimension. The ffmpeg will recalculate the correct value automatically while preserving the aspect ratio.

* **480p** <br>
To scale the video to 480p we use <br>
`ffmpeg -i 10BBB.mp4 -vf scale=480:-1 -c:v libx264 -crf 18 -preset veryslow -c:a copy 480p_10BBB.mp4` <br>
In this case we set the width to 480p and use -1 for the height.

* **360x240** <br>
To scale the video to 360x240 we use <br>
`ffmpeg -i 10BBB.mp4 -vf "scale='min(360,iw)':'min(240,ih)'" -c:v libx264 -crf 18 -preset veryslow -c:a copy 360x240_10BBB.mp4` <br>
To avoid upscaling if the original dimensions are to small the output width will be evaluated to be the minimum of 360 and the input width; the same for the height.

* **160x120** <br>
To scale the video to 160x120 we use <br>
`ffmpeg -i 10BBB.mp4 -vf "scale='min(160,iw)':'min(120,ih)'" -c:v libx264 -crf 18 -preset veryslow -c:a copy 160x120_10BBB.mp4`

## 4. Change the audio into mono output and in a different audio codec
To change the audio into mono and change the codec from .mp4 to .mov we use <br>
`ffmpeg -i 10BBB.mp4 -ac 1 10BBB_mono.mov`

The `-ac 1` is used so both channels of the stereo stream will be downmixed into the mono stream.
If we get the specs of the `10BBB_mono.mov` we see that indeed the audio is mono: <br>
`Stream #0:1: Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, mono, fltp, 69 kb/s (default)` 

## 5. Create a Python script able to launch any of the other exercices
The script created is a interactive script to choose what exercice you wish to apply over the 10 second cut video. The following choices propmt in the terminal:
```
What do you want to do?: 
 1- Extract YUV histogram 
 2- Resize video 
 3- Change the audio to mono and type of codec 
 0- Exit
Write the number of the choice: 
```
