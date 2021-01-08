
import os
from sys import exit
import subprocess

FOLDER = "Assets/"


def p3_ex1():
    cut_video = 'ffmpeg -ss 00:00:00.0 -i {}BBB.mp4 -c copy -t 00:01:00.0 {}1minBBB.mp4'.format(
        FOLDER, FOLDER)

    # Two codec options for audio
    export_audio_mp4 = 'ffmpeg -i {}1minBBB.mp4 -map 0:a -ac 1 {}mono_audio_1minBBB.mp4'.format(
        FOLDER, FOLDER)
    export_audio_aac = 'ffmpeg -i {}1minBBB.mp4 -map 0:a -ac 1 {}mono_audio_1minBBB.aac'.format(
        FOLDER, FOLDER)

    bit_rate = "ffmpeg -i {}1minBBB.mp4 -b:a 16k -vn {}1minBBB_16k.mp4".format(
        FOLDER, FOLDER)

    # This solution doesn't "burns the subtitles" into the video, so that every viewer of the video will be forced to see them.
    convert_subtitles = "ffmpeg -i {}subtitles.srt {}subtitles.ass".format(
        FOLDER, FOLDER)

    # package everything in a .mp4 file and add subtitles using a video filter:
    package = 'ffmpeg -i {}1minBBB.mp4 -i {}mono_audio_1minBBB.mp4 -i {}1minBBB_16k.mp4 -map 0:0 -map 0:1 -map 1:0 -map 2:0 -vf "ass={}subtitles.ass" {}cont_BBB.mp4'.format(
        FOLDER, FOLDER, FOLDER, FOLDER, FOLDER)

    os.system(cut_video)
    os.system(export_audio_mp4)
    os.system(bit_rate)
    os.system(convert_subtitles)
    os.system(package)


if __name__ == "__main__":
    p3_ex1()
