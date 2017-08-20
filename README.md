# Asurix-bot

> *Asurix-bot is a basic Discord bot basically made for Asurix#4727 who needed a feature*

## Installing

The guide for installing the bot is [here](INSTALLING.md)

## Features list

* Inter-channels communication
* Python code evaluating system (from Danny's bot)

## Improvments to do

### General improvments

* [ ] A safe system to handle rate limits
* [X] Use of json files to store data
* [X] Auto-checking of bot updates according to the github repo
* [X] A guide for installing the bot
* [X] A script to install the bot's requirements easily

### Inter-channels communication

* [X] Update edited / deleted messages
* [X] Unlimited number of channels
* [X] Unlimited number of communications
* [X] Notify the user if the bot doesn't have the permissions to send messages / attachments in at least one of the channel of its different registered communications
* [X] Send a warning if an event (kicks / bans / leaves / channels deletions / channels permissions changes / servers deletions / roles changes) would impact conversations
* [ ] Group several messages in a row from a same user in an unique embed ![Example](http://i.imgur.com/84PjK2D.png)
* [X] Proper handler for messages containing attachments
* [ ] Handling messages reactions

## Bugs

* Inter-channels communication
  * [X] Bug#1 - Cannot send messages with only attachments/embeds
  * [ ] Bug#2 - Embed's color isn't always correct
  * [X] Bug#6 - Tuple format instead of list when adding a new communication
* General
  * [X] Bug#3 - Infinite loop when the bot can't log in
  * [X] Bug#4 - Can't detect if the git repo is outdated
  * [X] Bug#5 - Clear function doesn't work on non-Windows OS

## Upcoming features

* Bot's profile customization
* Moderating commands

## Troubleshooting

If you have any problems installing/running the bot, please consult [this](TROUBLESHOOTING.md).

## Development server

If you wanna join the development server:
<iframe src="https://discordapp.com/widget?id=348276754693095425&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0"></iframe>