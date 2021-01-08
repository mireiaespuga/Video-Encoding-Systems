
# -*- coding: utf-8 -*-
import os
from sys import exit
import subprocess

EXIT = 0
BBB_CONTAINER = 1
CUSTOM_CONTAINER = 2
BROADCAST = 3
TEST_CONT_BR = 4


# Litle menu with a class inside (required)
class Menu_P3:
    def bbb_container(self):
        os.system("python p3_container.py")

    def custom_container(self):
        os.system("python p3_create_container.py")

    def check_broadcast(self):
        os.system("python p3_check_broadcast.py")

    def test(self):
        os.system("python p3_testing_script.py")


if __name__ == "__main__":
    options = Menu_P3()
    choice = None

    while choice != EXIT:
        # input parameters from terminal
        print('\n\nWhat do you want to do?: \n 1- Create a predefined BigBuckBunny container \n 2- Create a custom container \n 3- Check validity of Broadcasting Standards \n 4- Create a container and test the BC standard  \n 0- Exit')
        choice = int(raw_input("Write the number of the choice: "))

        if choice == BBB_CONTAINER:
            options.bbb_container()
        elif choice == CUSTOM_CONTAINER:
            options.custom_container()
        elif choice == BROADCAST:
            options.check_broadcast()
        elif choice == TEST_CONT_BR:
            options.test()
        elif choice == EXIT:
            exit(1)
        else:
            print('Invalid choice')
