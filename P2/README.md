# SCAV-P2
The script `p2.py` integrates all the previous exercises, which allows you to choose which variables of the input video you’d like to change.

When you launch the script 5 options appear
```
What do you want to do?:
 1- Get specs from video
 2- Rename resized videos
 3- Resize a video
 4- Transcode input
 0- Exit
Write the number of the choice:
```

## Option 1: Get specs from video
When selecting option 1 all files available in the `Assets` folder appear and you need to select which file you wish to inspect
```
All files must be in the Assets folder. Available files:
160x120_10BBB.mp4
480p_10BBB.mp4
360x240_10BBB.mp4
10BBB.mp4
720p_10BBB.mp4

What file do you want to inspect?:
```

Once you select what file you wish to inspect 4 commands are executed that parse 4 specs of the video into variables. The command `ffprobe -v error -select_streams v:0 -show_entries stream=<wished specs> -of csv=s=x:p=0 <input>` selects the wished specs from the stream 0 which is the video stream. The selected specs are read from terminal and stored into variables. <br>
In the case of the file `160x120_10BBB.mp4` we get `Video Assets/160x120_10BBB.mp4 duration is: 10.050000, dimensions are: 160x120, bit rate is: 230253 and codec: h264 video`. 

Once the limitted specs are shown another prompt appears to print in terminal the full data specs of the file in a json format such as `ffprobe -v quiet -print_format json -show_format -show_data -show_streams <input>`.

## Option 2: Rename resized videos
When selecting option 1 all files available in the `Assets` folder appear and you need to select which file you wish to rename
```
What file do you want to rename?:
1- 160x120_10BBB.mp4
2- 480p_10BBB.mp4
3- 360x240_10BBB.mp4
4- 10BBB.mp4
5- 720p_10BBB.mp4
Write the number of the choice:
```

Once you select what file you wish to rename a prompt asking for the new name appears `What's the new name?:`. If the new name includes a new extension, a prompt asking if you want to transcode the file shows .
```
What's the new name?: test.mov
Are you sure you want to change the extension from mp4 to mov? [Y/N]:
```
If you answer Y, then the video is renamed and transcoded, if you select N then the video is renamed but it keeps the old extension.

## Option 3: Resize a video
When selecting option 3 all files available in the `Assets` folder appear and you need to select which file you wish to resize
```
All files must be in the Assets folder. Available files:
160x120_10BBB.mp4
480p_10BBB.mp4
360x240_10BBB.mp4
10BBB.mp4
720p_10BBB.mp4

Write the full name of the file do you want to resize:
``` 
Once you select what file you wish to resize a prompt asking for the new dimensions appears. The acceptable new dimensions are of the `720p` format, or else the `360x360` format. Deppending on the format a different scale command `scale=<dim>:-1` or `scale='min(<width>,iw)':'min(<height>,ih)` respectively. The new resized file is stored along with the original dimension file.


## Option 4: Transcode input
When selecting option 4 all files available in the `Assets` folder appear and you need to select which file you wish to transcode.
```
All files must be in the Assets folder. Available files:
160x120_10BBB.mp4
480p_10BBB.mp4
360x240_10BBB.mp4
10BBB.mp4
720p_10BBB.mp4

Write the full name of the file do you want to transcode:
```
Once you select what file you wish to resize a prompt asking for the new extension appears and it transcodes the file without erasing the original one through 
`ffmpeg -i <input> -c:v libx264 -crf 18 -preset veryslow -c:a copy <output>`. The explanation for this command can be found in the readme for seminar 2 https://github.com/mireiaespuga/SCAV-S2/blob/main/README.md.


## Option 5: Exit
Stops the execution and exits.

