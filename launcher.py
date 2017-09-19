"""The launcher for the bot"""

import os
import subprocess
import sys
import shutil


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

    if not os.path.exists("ffmpeg.exe"):
        if sys.platform == "win32":
            print("Downloading ffmpeg...")
            import requests
            req = requests.get("http://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-20170915-6743351-win32-static.zip") #pylint: disable=line-too-long
            path = "ffmpeg-20170915-6743351-win32-static/bin"
        elif sys.platform == "win64":
            print("Downloading ffmpeg...")
            import requests
            req = requests.get("http://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20170915-6743351-win64-static.zip") #pylint: disable=line-too-long
            path = "ffmpeg-20170915-6743351-win64-static/bin"
        else:
            os.system("sudo apt-get install libav-tools -y")
            return
        print("Copying ffmpeg on the repository...")
        with open("ffmpeg.zip", "wb") as code:
            code.write(req.content)
            print("Extracting ffmpeg...")
            import zipfile
            file = zipfile.ZipFile("ffmpeg.zip", "r")
            file.extract(member="ffmpeg-20170915-6743351-win32-static/bin/ffmpeg.exe")
            os.rename("ffmpeg-20170915-6743351-win32-static/bin/ffmpeg.exe", "ffmpeg.exe")
            file.close()
        print("Cleaning the directory...")
        os.remove("ffmpeg.zip")
        shutil.rmtree(path.split("/")[0])


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
        from run import run_bot
        run_bot()
