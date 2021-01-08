import os
import subprocess
from p3_create_container import print_available_files

FOLDER = "Assets/"

BROADCAST_STD = {
    "DTMB": {"audio": ["aac", "ac3", "mp2", "mp3"], "video": ["avs", "mpeg2video", "h264"]},
    "ATSC": {"audio": ["ac3"], "video": ["mpeg2video", "h264"]},
    "ISDB": {"audio": ["aac"], "video": ["mpeg2video", "h264"]},
    "DVB": {
        "audio": ["aac", "ac3", "mp3"],
        "video": ["mpeg2video", "h264"],
    }
}


def select_file():
    file = raw_input("\nWhat's the full name of the container?: ")
    assert os.path.isfile(FOLDER + file), "file not found"
    return file


def read_output(command):
    # read output instead of printing it
    out = subprocess.Popen(command.split(' '),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    return stdout, stderr


def get_valid_standard(codecs):
    codecs.pop()
    # we chech the boradcasting standards matches in our dict and append them into a list
    valid_std = [B_STD for B_STD in BROADCAST_STD.keys() if (
        codecs[0] in BROADCAST_STD[B_STD]["video"]
        and codecs[1] in BROADCAST_STD[B_STD]["audio"]
    )]
    return valid_std


def show_results(valid_std, file):
    if len(valid_std) > 0:
        print("{} fits the {} Bradcasting Standards".format(
            file, ' '.join(valid_std)))
    else:
        print("{} doesn't fit any Broadcasting Standard".format(
            file))


def check_standard(file):
    stdout, stderr = read_output(
        "ffprobe -v error -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {}".format(FOLDER + file))
    valid_std = get_valid_standard(str(stdout).split('\n'))
    show_results(valid_std, file)


if __name__ == "__main__":
    print_available_files()
    file = select_file()
    check_standard(file)
