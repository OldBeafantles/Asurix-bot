# Installing

The installation guide has 3 steps:

* [Creating a bot account](#botAccount)
* [Installing requirements](#requirements)
* [Launching the bot](#launch)

Having troubleshoots? Check the [Troubleshooting](#troubleshooting) section!

## Creating a bot account <a id = "botAccount"></a>

1. Log into Discord **on your browser** using this [link](https://discordapp.com/login).

1. Then, go to this [url](https://discordapp.com/developers/applications/me).

1. Create a new app clicking on the `+` button. ![example](http://i.imgur.com/QtiAkzn.png)

1. Configure your new application, then click on the `Create App` button. ![example](http://i.imgur.com/3I4tz0P.png)<br>

Here's, this application would have these caracteristics:

* name: `Beaftek's bot`
* description: `An awesome bot wow such very good. I bet you're jealous`
* icon: [this image](http://i.imgur.com/6xpTNLr.png)

**Note**: Changing app's icon / name wouldn't change your bot's avatar / name. It would change your *app's icon / name*. If you wanna change your bot's name / avatar, you would be able to do it directly using bot's commands. (module `Owner`).

1. Click on the `Create a Bot User` button. ![example](http://i.imgur.com/vLyRS0e.png)

1. Confirm your action clicking on the `Yes, do it!` button. ![example](http://i.imgur.com/tiK6jFt.png)

1. Click on `click to reveal`. ![example](http://i.imgur.com/p4EpyXD.png)

1. Note down your bot's token. ![example](http://i.imgur.com/rcWbpPS.png)

⚠️**WARNING**⚠️ **Do NOT spread your bot's token to ANYONE. NEVER**

## Installing requirements <a id = requirements></a>

Please follow the instructions for your OS:

* [Windows](#windows)
* [Linux](#Linux)

### Windows <a id = windows></a>

1. Download Python 3.6.2 [here](https://www.python.org/ftp/python/3.6.2/python-3.6.2.exe).

1. Install Python 3.6.2. Make sure the `Add Python 3.6 to PATH` box is checked. ![example](http://i.imgur.com/3RTYxVM.png)

1. To prevent any issues, please click on the `Disable path length limit` button at the end of the installation. ![example](http://i.imgur.com/qBjWq8t.png)

1. Download Git [here](https://git-scm.com/download/win).

1. Install Git. Just press `Next` at every steps, do not touch the installation configuration. ![example](http://i.imgur.com/J3pz2ea.png)

1. Press Windows keyboard button + R. ![keyboard](http://i.imgur.com/V6IojR6.png)

1. Write `cmd` in the new window at the bottom left of your screen then press the `OK` button. ![execute](http://i.imgur.com/kYbtMo8.png)

1. Type `cd Desktop`, then `git clone https://www.github.com/Beafantles/Asurix-bot` in the command prompt. ![clone](http://i.imgur.com/RIiAD9z.png)

👍 **You just installed `Asurix-bot` on your desktop!** 🎉

### Linux <a id = linux></a>

1. Install git package using `sudo apt-get install git` command in a terminal.

1. You may also need the `libffi` package (depending on your Linux distribution). You can install it running this command: `sudo apt-get install libffi-dev`.

1. You may also need the `zlib` package (depending on your Linux distribution). You can install it running this command: `sudo apt-get install zlib1g-dev`.
1. Install Python 3.6.2 and pip module using the following commands:

```bash
wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz
tar xJf Python-3.6.2.tar.xz
cd Python-3.6.2/
./configure --enable-optimizations
make
make install
cd ..
wget https://bootstrap.pypa.io/get-pip.py
python3.6 get-pip.py
```

## Launching the bot <a id = launch></a>

1. Go to the directory `Asurix-bot`.

1. If you're on Windows, just double-click on the file `start.bat`. If you're on Linux, open a terminal in this directory and type `python3.6 launcher.py`.

1. If it's your first time running the bot, type `1` to install all the requirements for the bot. ![example](http://i.imgur.com/LTwHOE3.png)

1. Then, type `2` if you want to start the bot and you want it to run all the time, even after being switched off. Type `3` if you want to run the bot *normally*.
1. If it's your first time running the bot, you would need to configure it. ![example](http://i.imgur.com/DRE8MIW.png)<br><br>**Note**: If you don't know how could you get your Discord ID, please check the gif below. ![getID](http://i.imgur.com/tgjEleS.gif)

1. If everything went well, you should have something similar to that: ![yay](http://i.imgur.com/CSXcSO2.png)

1. To invite your bot in your server, open your `bot invitation link` (see screenshot above) in your browser.

⚠️**WARNING**⚠️**You need the `Manage server` permission to invite the bot into the server**

## Troubleshooting <a id = "troubleshooting"></a>

Not done yet.