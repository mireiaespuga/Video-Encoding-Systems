
# -*- coding: utf-8 -*-
import os
from sys import exit


class Direct(object):
    inp = ''
    outp = ''

    def __init__(self, inp, outp):
        self.inp = inp
        self.outp = outp


choice = None

# cut original video
command = "ffmpeg -ss 00:00:30.0 -i BBB.mp4 -c copy -t 00:00:10.0 10BBB.mp4"
os.system(command)  # execute the terminal command

while choice != 0:
    # input parameters from terminal
    print('\n\nWhat do you want to do?: \n 1- Extract YUV histogram \n 2- Resize video \n 3- Change the audio to mono and type of codec \n 0- Exit')
    choice = int(raw_input("Write the number of the choice: "))

    direc = Direct('10BBB.mp4', "Results/")
    if choice == 1:
        output = direc.outp + "hist10BBB.mp4"  # set histogram output name
        command = "ffmpeg -i {} -vf ".format(direc.inp) + "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay" + \
            " -c:v libx264 -crf 18 -preset veryslow -c:a copy {}".format(
                output)
    elif choice == 2:
        # input size parameters from terminal
        print(
            '\n\nWhat size do you want?: \n 1- 720p \n 2- 480p \n 3- 360x240 \n 4- 160x120')
        size_choice = int(raw_input("Write the number of the choice: "))
        if size_choice == 1:
            output = direc.outp + "720p_10BBB.mp4"  # set resize name
            command = "ffmpeg -i {} -vf scale=-1:720 -c:v libx264 -crf 18 -preset veryslow -c:a copy {}".format(
                direc.inp, output)
        elif size_choice == 2:
            output = direc.outp + "480p_10BBB.mp4"  # set resize name
            command = "ffmpeg -i {} -vf scale=480:-1: -c:v libx264 -crf 18 -preset veryslow -c:a copy {}".format(
                direc.inp, output)
        elif size_choice == 3:
            output = direc.outp + "360x240_10BBB.mp4"  # set resize name
            command = "ffmpeg -i {} -vf ".format(direc.inp) + '"' + "scale='min(360,iw)':'min(240,ih)'" + \
                '"' + \
                " -c:v libx264 -crf 18 -preset veryslow -c:a copy {}".format(
                    output)
        elif size_choice == 4:
            output = direc.outp + "160x120_10BBB.mp4"  # set resize name
            command = "ffmpeg -i {} -vf ".format(direc.inp) + '"' + "scale='min(160,iw)':'min(120,ih)'" + \
                '"' + \
                " -c:v libx264 -crf 18 -preset veryslow -c:a copy {}".format(
                    output)
        else:
            print('Invalid choice')
    elif choice == 3:
        output = direc.outp + "10BBB_mono.mov"  # set mono.mov name
        command = "ffmpeg -i {} -ac 1 {}".format(direc.inp, output)
    elif choice == 0:
        exit(1)
    else:
        print('Invalid choice')

    os.system(command)  # execute the terminal command
