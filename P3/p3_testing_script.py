import os
import subprocess
from p3_check_broadcast import check_standard

FOLDER = "Assets/"


def get_latest_file(directory=None):
    files = os.listdir(directory)
    paths = [os.path.join(directory, basename) for basename in files]
    return max(paths, key=os.path.getctime)


if __name__ == "__main__":
    print("\nFirst you have to create a container")
    os.system("python p3_create_container.py")
    newest = get_latest_file(FOLDER)
    print('\n\n')
    check_standard(newest.strip(FOLDER))
    print('\n')
