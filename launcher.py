"""The launcher for the bot"""

import os
import subprocess
import sys
from run import run_bot


# USEFUL FUNCTIONS
if sys.platform == "win32" or sys.platform == "win64":
    CLEAR = lambda: os.system("cls")
else:
    CLEAR = lambda: os.system("clear")


def install_update():
    """Installs/Updates the requirements"""

    os.system("pip install --upgrade pip")

    #Get the requirements
    file = open("requirements.txt", "r")
    requirements = file.readlines()
    file.close()

    # Update the requirements
    for req in requirements:
        os.system(req)


# LAUNCHING THE BOT
CLEAR()

subprocess.call("git fetch", stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT, shell=True)
RESULT = subprocess.check_output("git status", shell=True)
if "Your branch is behind" in str(RESULT):
    ANSWER = input("The bot isn't up-to-date, please type 'yes' to update it!\n\n> ")
    if ANSWER.upper() == "YES":
        os.system("git pull")

ANSWER = ""
while ANSWER != "3":
    CLEAR()

    ANSWER = input("What do you want to do?\n\n" + \
                   "1. Install & update requirements\n" + \
                   "2. Launch the bot\n" + \
                   "3. Quit\n\n> ")

    if ANSWER == "1":
        install_update()
    elif ANSWER == "2":
        run_bot()
