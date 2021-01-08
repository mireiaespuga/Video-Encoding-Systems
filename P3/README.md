# SCAV-P3
For this lab, you'll need to download the Big Buck Bunny video from http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_60fps_normal.mp4. Then rename it to `BBB.mp4` and put it in the `Assets/`folder.

In this repo you'll find a python script `p3_class.py` that englobes all the proposed execises into a class. When you launch `p3_class.py` a menu appears showcasing the different options you have:
```
What do you want to do?:
 1- Create a predefined BigBuckBunny container
 2- Create a custom container
 3- Check validity of Broadcasting Standards
 4- Create a container and test the BC standard
 0- Exit
Write the number of the choice:
```

Each option calles method of a python class called `Menu_P3` that will launch each script individually.


## Option 1: Create a predefined BigBuckBunny container
For this option we had to create a .mp4 container with specified tracks of the BigBuckBunny container such as a 1 minute cut version of the original video, a mono track of the 1 minute video, a lower bitrate of the audio and the subtitles for the video found in the `subtitles.srt` file. 

To **cut the original video into a 1 minute video** we executed the command `ffmpeg -ss 00:00:00.0 -i BBB.mp4 -c copy -t 00:01:00.0 1minBBB.mp4` and obtained the 1 minute video we'll be using for the entire lab. 

To **export a mono track of the 1 minute video** we executed the `ffmpeg -i 1minBBB.mp4 -map 0:a -ac 1 mono_audio_1minBBB.mp4` command. The `-ac 1` is used so both channels of the stereo stream will be downmixed into the mono stream. 
If we get the specs of the output file we see that indeed the audio is mono `Stream #0:0(und): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, mono, fltp, 69 kb/s (default)` 

To **export a lower bitrate audio track of the 1 minute video** we executed the command `ffmpeg -i 1minBBB.mp4 -b:a 16k -vn 1minBBB_16k.mp4`. To choose the lower bitrate we analyzed the specs of the original audio track and chose half the original bitrate `32k / 2 = 16k`.

To **add the subtitles** we considered two different options. First, we have the option to burn the subtitles into the video with the `mov_text` codec; and then we have the option to add the subtitles using a video filter so the user won't be forced to see them. In this excercise I chose the latter. To execute it first we'll have to convert the `.srt` file into a `.ass` file through `ffmpeg -i subtitles.srt subtitles.ass` and then add them onto the final container using the video filter `-vf "ass={}subtitles.ass"`.

Finally, **to package everything into a .mp4 container** we have to take into consideration the different mapping we want to perform. For instance, in the command we execute `ffmpeg -i 1minBBB.mp4 -i mono_audio_1minBBB.mp4 -i 1minBBB_16k.mp4 -map 0:0 -map 0:1 -map 1:0 -map 2:0 -vf "ass=subtitles.ass" cont_BBB.mp4` we see how the first file `1minBBB.mp4` will be mapped onto the Stream #0:0 and the stream  Stream #0:1.


## Option 2: Create a custom container
For this option I implemented the same logic as in option 1 but now the container is fully customizable. When executing the script an option menu appears displaying the available files in the Assets folder and asking how many files you'll want to include in the container.
```
All files must be in the Assets/ folder. Available files:
1minBBB_sub.mp4
1minBBB.mp4
subtitles.srt
mono_audio_1minBBB.mp4
subtitles.ass
1minBBB_16k.mp4
mono_audio_1minBBB.aac
BBB.mp4
How many files do you want to include (i.e 4):
```

Then deppending on the type of file you select (not `.srt` or `.ass`) you'll be asked how many channels do you want for the file. Finally it will ask you for the name of the container. In the `create_command()` we'll construct the command iterating through and mapping the different files selected in concordance with the specified channels. <br>
For example if we were to select the following files: `1minBBB.mp4` with 2 channels, `mono_audio_1minBBB.mp4` with 1 channel and `subtitles.ass` <br> We'd execute the following command `ffmpeg -i Assets/1minBBB.mp4 -i Assets/mono_audio_1minBBB.mp4 -i Assets/subtitles.ass -c:s mov_text -c:a copy -c:v copy -map 0:0 -map 0:1 -map 1:0 -map 2 -metadata:s:s:0 language=eng Assets/container_example.mp4`

And obtain the `container_example.mp4` container with the following specs:
```
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'Assets/container_example.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    title           : Big Buck Bunny, Sunflower version
    artist          : Blender Foundation 2008, Janus Bager Kristensen 2013
    composer        : Sacha Goedegebure
    encoder         : Lavf58.64.100
    comment         : Creative Commons Attribution 3.0 - http://bbb3d.renderfarming.net
    genre           : Animation
  Duration: 00:01:00.02, start: 0.000000, bitrate: 4826 kb/s
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 1920x1080 [SAR 1:1 DAR 16:9], 4426 kb/s, 60 fps, 60 tbr, 60k tbn, 120 tbc (default)
    Metadata:
      handler_name    : GPAC ISO Video Handler
    Stream #0:1(und): Audio: ac3 (ac-3 / 0x332D6361), 48000 Hz, 5.1(side), fltp, 320 kb/s (default)
    Metadata:
      handler_name    : GPAC ISO Audio Handler
    Side data:
      audio service type: main
    Stream #0:2(und): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, mono, fltp, 69 kb/s (default)
    Metadata:
      handler_name    : GPAC ISO Audio Handler
    Stream #0:3(eng): Subtitle: mov_text (tx3g / 0x67337874), 0 kb/s (default)
    Metadata:
      handler_name    : SubtitleHandler
```

## Option 3: Check validity of Broadcasting Standards
In this option we'll want to see, given a container, which Broadcasting Standards it would fit if any. To do so we create a dictionary with the different standards and their respective acodecs and vcodecs such as
```
BROADCAST_STD = {
    "DTMB": {"audio": ["aac", "ac3", "mp2", "mp3"], "video": ["avs", "mpeg2video", "h264"]},
    "ATSC": {"audio": ["ac3"], "video": ["mpeg2video", "h264"]},
    "ISDB": {"audio": ["aac"], "video": ["mpeg2video", "h264"]},
    "DVB": {
        "audio": ["aac", "ac3", "mp3"],
        "video": ["mpeg2video", "h264"],
    }
}
```

Once we have this dict, we'll ask the user for a container to inspect through the same menu as in Option 2. Once selected, we'll get the codec specs through `ffprobe -v error -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 <FILE>` and read and store the output from the terminal. Then we'll go through the dict and select the valid standards and display them. If none are valid we'll display that too.


## Option 4: Create a container and test the BC standard
In this option we'll launch the custom container script from Option 2. Once the container is created we'll get the latest file from the Assets folder (the container we just created) and perform the Broadcasting Standard from Option 3 but without asking for the container you want, it's more straightforward.
