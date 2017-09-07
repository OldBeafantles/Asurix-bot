# Asurix-bot

> *Asurix-bot is a basic Discord bot basically made for Asurix#4727 who needed a feature*

## Installing

The guide for installing the bot is [here](INSTALLING.md)

## Features list

* Inter-channels communication
* Basic bot's configuration
* Roles self-assignment / self-removal (with very complete configuration)

## Improvments to do

### General improvments

* [ ] A safe system to handle rate limits
* [X] Use of json files to store data
* [X] Auto-checking of bot updates according to the github repo
* [X] A guide for installing the bot
* [X] A script to install the bot's requirements easily

### Communications modules

* [X] Update edited / deleted messages
* [X] Unlimited number of channels
* [X] Unlimited number of communications
* [X] Notify the user if the bot doesn't have the permissions to send messages / attachments in at least one of the channel of its different registered communications
* [X] Send a warning if an event (kicks / bans / leaves / channels deletions / channels permissions changes / servers deletions / roles changes) would impact conversations
* [X] Proper handler for messages containing attachments
* [X] Handling messages reactions

### Base module

* [ ] Show the delay between local bot's version and official bot's version (on Github)
* [ ] Remember bot's game / stream status

### Admin module

* [X] Kick / Unban / Ban commands
* [X] Warn command
* [X] b1nzy_ban command
* [ ] Mute system
* [X] Moderation logs system
* [ ] Allows reasons edits
* [ ] Checks for audit logs and updates

### Roles module

* [ ] A more intuitive system
* [ ] More conditions types
* [ ] Notify the user who's changing the bot's permissions if these changes are affecting bot's roles assignements / removals

### Hungers games modules (not released yet)

* [X] Translating system
* [ ] More possibilities

## Bugs

* Inter-channels communication
  * [X] Bug#1 - Cannot send messages with only attachments/embeds
  * [X] Bug#2 - Embed's color isn't always correct
  * [X] Bug#6 - Tuple format instead of list when adding a new communication
* General
  * [X] Bug#3 - Infinite loop when the bot can't log in
  * [X] Bug#4 - Can't detect if the git repo is outdated
  * [X] Bug#5 - Clear function doesn't work on non-Windows OS
  * [X] Bug#7 - Can't load remaining modules at bot's start if one of them was wrong
* Base
  * [X] Bug#8 - `info` isn't triggered
  * [X] Bug#9 - `info` wasn't showing correct info about the runtimes + time since bot's creation

## Upcoming features

* Moderating commands
* Hunger games module

## Troubleshooting

If you have any problems installing/running the bot, please consult [this](TROUBLESHOOTING.md).

## Development server

If you wanna join the development server, click [here](https://discord.gg/nXHZF53).