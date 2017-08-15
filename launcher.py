import os
import subprocess
import sys
import requests


# USEFUL FUNCTIONS
if sys.platform == "win32" or sys.platform == "win64":
    clear = lambda: os.system("cls")
else:
    clear = lambda: os.system("clear")

# Install & update the requirements for the bot according to the needed modules listed in requirements.txt
def installUpdate():

    if subprocess.call('pip', shell = True) != 0:
        
    else:
        os.system("pip install --upgrade pip")

    #Get the requirements
    f = open("requirements.txt", "r")
    requirements = f.readlines()
    f.close()

    # Update the requirements
    for r in requirements:
        os.system(r)



# LAUNCHING THE BOT
clear()

returnValue = subprocess.call('git fetch', shell = True)
if returnValue != 0:
    answer = input("The bot isn't up-to-date, please type 'yes' to update it!\n\n> ")
    if answer.upper() == "YES":
        os.system('git pull')

answer = ""
while answer != "4":
    
    clear()

    answer = input( "What do you want to do?\n\n" + 
                    "1. Install & update requirments\n" +
                    "2. Launch the bot with autorestart\n" +
                    "3. Launch the bot\n" +
                    "4. Quit\n\n> ")

    if answer == "1":
        installUpdate()
    elif answer == "2":
        while True:
            import bot_asurix
    elif answer == "3":
        import bot_asurix
