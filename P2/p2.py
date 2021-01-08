
# -*- coding: utf-8 -*-
import os
from sys import exit
import subprocess

EXIT = 0
SPECS = 1
RENAME = 2
RES_CHANGE = 3
TRANSCODE = 4
choice = None
transcode = False


class Direct(object):
    inp = ''
    outp = ''

    def __init__(self, inp, outp):
        self.inp = inp
        self.outp = outp


def print_available_files():
    print('\n\nAll files must be in the Assets folder. Available files:')
    indexed_files = get_files("Assets/")
    # input size parameters from terminal
    for file in indexed_files:
        print('{}'.format(file[1]))


def remove_file(file_name):
    if os.path.exists(file_name):  # we check if it exists
        os.remove(file_name)
    else:
        print("The file does not exist")


def transcode(old_filename, new_file, delete_old=False):
    command = "ffmpeg -i {} -c:v libx264 -crf 18 -preset veryslow -c:a copy {}".format(
        old_filename, new_file)
    os.system(command)
    if(delete_old):  # if we want to delete the old file
        remove_file(old_filename)


def read_output(command):
    # read output instead of printing it
    out = subprocess.Popen(command.split(' '),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    return stdout, stderr


def get_files(directory=None):
    # get files in a directoy
    if(directory):
        arr = os.listdir(directory)
    else:
        arr = os.listdir('.')

    files = [i for i in arr if i != '.DS_Store']  # ignore random files
    return [(s + 1, i) for (s, i) in enumerate(files)]  # files and index


def get_duration(video_name):
    command = create_data_command('duration', video_name)
    stdout, stderr = read_output(command)
    return stdout.split('\n')[0]


def get_bit_rate(video_name):
    command = create_data_command('bit_rate', video_name)
    stdout, stderr = read_output(command)
    return stdout.split('\n')[0]


def get_codec_type(video_name):
    command = create_data_command('codec_name,codec_type', video_name)
    stdout, stderr = read_output(command)
    split = stdout.split('x')
    split[1] = split[1].split('\n')[0]
    return split  # returns [codec name ,  codec type]


def get_dataspecs(video_name):
    # individually parse data specs into variables
    duration = get_duration(video_name)
    dimension = get_video_dim(video_name)
    bit_rate = get_bit_rate(video_name)
    codec = get_codec_type(video_name)

    print('\nVideo {} duration is: {}, dimensions are: {}x{}, bit rate is: {} and codec: {} {}'.format(
        video_name, duration, dimension[0], dimension[1], bit_rate, codec[0], codec[1]))


def create_data_command(wishes, video_name):
    return "ffprobe -v error -select_streams v:0 -show_entries stream={} -of csv=s=x:p=0 {}".format(wishes,
                                                                                                    video_name)


def print_data_json(video_name):
    # print in terminal json format of all data specs
    command = "ffprobe -v quiet -print_format json -show_format -show_data -show_streams {}".format(
        video_name)
    os.system(command)


def get_video_dim(video_name):
    command = create_data_command('width,height', video_name)
    stdout, stderr = read_output(command)
    split_dim = stdout.split('x')
    split_dim[1] = split_dim[1].split('\n')[0]
    return split_dim  # returns [width, height]


def format_input(new_filename):
    # we want to avoid double the extension
    split = new_filename.split('.')
    file_name = split[0]
    extension_new = None
    if(len(split) > 1):
        extension_new = split.pop()  # we consider last element to be the new extension
    return file_name, extension_new


while choice != EXIT:
    direc = Direct('', "Assets/")
    # input parameters from terminal
    print('\n\nWhat do you want to do?: \n 1- Get specs from video \n 2- Rename resized videos \n 3- Resize a video \n 4- Transcode input  \n 0- Exit')
    choice = int(raw_input("Write the number of the choice: "))

    get_files(direc.outp)

    if choice == SPECS:
        print_available_files()
        video = direc.outp + \
            raw_input('\n\nWhat file do you want to inspect?:')
        get_dataspecs(video)

        yes_no = raw_input(
            "Do you want to see all the data specs [Y/N]: ")
        if(yes_no.upper() == 'Y'):
            print_data_json(video)

    elif choice == RENAME:
        indexed_files = get_files(direc.outp)
        # input size parameters from terminal
        print('\n\nWhat file do you want to rename?:')
        for file in indexed_files:
            print('{}- {}'.format(file[0], file[1]))

        size_choice = int(raw_input("Write the number of the choice: "))

        # set filename to change deppending on the choice
        if size_choice > len(indexed_files) or size_choice < 1:
            print('Invalid choice')
        else:
            name_input = raw_input("\nWhat's the new name?: ")

            file_name, extension_new = format_input(name_input)
            old_filename = [direc.outp + name for i,
                            name in indexed_files if i == size_choice].pop()

            extension_old = old_filename.split('.').pop()
            if(extension_new and extension_new != extension_old):
                change_ext = raw_input(
                    "Are you sure you want to change the extension from {} to {}? [Y/N]: ".format(extension_old, extension_new))
                if(change_ext.upper() == 'Y'):
                    transcode = True
                    new_filename = direc.outp + file_name + '.' + extension_new
                elif(change_ext.upper() == 'N'):
                    new_filename = direc.outp + file_name + '.' + extension_old
            else:
                new_filename = direc.outp + file_name + '.' + extension_old

        # rename or rename and transcode
        if transcode is True:
            # we want to delete the old file
            transcode(old_filename, new_filename, True)
        else:
            os.rename(old_filename, new_filename)

    elif choice == RES_CHANGE:

        print_available_files()
        resize_file = raw_input(
            "\nWrite the full name of the file do you want to resize: ")
        dim_input = raw_input("\nWhat are the new dimensions?: ")

        wanted_dim = dim_input.split('x')
        real_dim = get_video_dim(direc.outp + resize_file)
        if len(wanted_dim) == 1:  # dimension must be 720p or similar
            scale = None
            wanted_dim = dim_input.split('p')
            # check compatibility of dimensions
            if int(wanted_dim[0]) == 720:
                scale = "-1:{}".format(wanted_dim[0])
            if int(wanted_dim[0]) == 480:
                scale = "{}:-1".format(wanted_dim[0])

            if scale:
                command = "ffmpeg -i Assets/{} -vf scale={} -c:v libx264 -crf 18 -preset veryslow -c:a copy Assets/{}_{}".format(
                    resize_file, scale, dim_input, resize_file)
                os.system(command)
            else:
                print("Dimensions are not valid for size input {}x{}".format(
                    real_dim[0], real_dim[1]))

        elif len(wanted_dim) == 2:  # dimension must be widthxheight or similar
            command = "ffmpeg -i Assets/{} -vf ".format(resize_file) + '"' + "scale='min({},iw)':'min({},ih)'".format(wanted_dim[0], wanted_dim[1]) + \
                '"' + \
                " -c:v libx264 -crf 18 -preset veryslow -c:a copy Assets/{}_{}".format(
                dim_input, resize_file)
            os.system(command)

    elif choice == TRANSCODE:

        print_available_files()
        transcode_file = direc.outp + raw_input(
            "\nWrite the full name of the file do you want to transcode: ")
        new_ext = raw_input(
            "\nWrite the new extension (i.e .mov): ")
        new_filename = transcode_file.split('.')[0] + new_ext
        transcode(transcode_file, new_filename, False)

    elif choice == EXIT:
        exit(1)
    else:
        print('Invalid choice')
