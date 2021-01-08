import os

FOLDER = "Assets/"


def get_files(directory=None):
    # get files in a directoy
    if(directory):
        arr = os.listdir(directory)
    else:
        arr = os.listdir('.')

    files = [i for i in arr if i != '.DS_Store']  # ignore random files
    return files


def get_indexed_files(directory=None):
    files = get_files(directory)
    return [(s + 1, i) for (s, i) in enumerate(files)]  # files and index


def print_available_files():
    print('\n\nAll files must be in the {} folder. Available files:'.format(FOLDER))
    indexed_files = get_indexed_files(FOLDER)
    for file in indexed_files:
        print('{}'.format(file[1]))


def convert_subs(filename):
    # If we have srt subtitle as input we'll convert it to ass
    convert_subtitles = "ffmpeg -i {}{}.srt {}{}.ass".format(
        FOLDER, filename, FOLDER, filename)
    os.system(convert_subtitles)
    return filename + '.ass'


def select_files():
    n_files = int(raw_input("How many files do you want to include (i.e 4): "))
    files = []
    subs = []
    for n in range(n_files):
        file = raw_input("\nWhat's the full name of the file?: ")
        assert os.path.isfile(FOLDER + file), "file not found"
        if file.split('.')[1] == 'ass':
            subs.append(FOLDER + file)
        elif file.split('.')[1] == 'srt':
            subs.append(FOLDER + convert_subs(file.split('.')[0]))
        else:
            channels = int(raw_input("\nHow many channels do you want?: "))
            files.append((FOLDER + file, channels))

    return files, subs


def container_name():
    return FOLDER + \
        raw_input("\nWhat's the name of the container?: ").split(
            '.')[0] + '.mp4'


def create_command(files, subs):

    # line up input files
    command = "ffmpeg {}".format(
        ''.join(["-i {} ".format(file[0]) for file in files])) + "{}".format(
            ''.join(["-i {} ".format(sub) for sub in subs]))

    # add copy commands for sub audio and video
    command += '-c:s mov_text -c:a copy -c:v copy '

    # map into streams
    for (i, channel) in enumerate(files):
        for ch in range(int(channel[1])):
            command += ''.join(["-map {}:{} ".format(i, ch)])
            latest = i

    # map subtitles
    subs_comm = "{}".format(
        ''.join(["-map {} ".format(s + latest + 1) for (s, sub) in enumerate(subs)])) + "{}".format(
        ''.join(["-metadata:s:s:{} language=eng ".format(s) for (s, sub) in enumerate(subs)]))

    command += subs_comm
    return command  # return final command


if __name__ == "__main__":
    print_available_files()
    files, subs = select_files()
    name = container_name()
    command = create_command(files, subs) + name
    os.system(command)
