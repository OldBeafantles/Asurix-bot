# Asurix-bot

> *Asurix-bot is a basic Discord bot basically made for Asurix#4727 who needed a feature*

## Requirements

* Python 3+ version
* pip module
* Others requirements will be automatically installed

## Features list

* Inter-channels communication

## Improvments to do

### General improvments

* [ ] A safe system to handle rate limits
* [X] Use of json files to store data
* [X] Auto-checking of bot updates according to the github repo
* [ ] A guide for installing the bot
* [X] A script to install the bot's requirements easily

### Inter-channels communication

* [ ] Update edited / deleted messages
* [ ] Unlimited number of channels
* [ ] Unlimited number of communications
* [ ] Notify the user if the bot doesn't have the permissions to send messages / attachments in at least one of the channel of its different registered communications
* [ ] Group several messages in a row from a same user in an unique embed ![Example](http://i.imgur.com/84PjK2D.png)
* [X] Proper handler for messages containing attachments

## Bugs

* Inter-channels communication
  * [X] Bug#1 - Cannot send messages with only attachments/embeds
  * [ ] Bug#2 - Embed's color isn't always correct
* General
  * [X] Bug#3 - Infinite loop when the bot can't log in
  * [X] Bug#4 - Can't detect if the git repo is outdated
  * [X] Bug#5 - Clear function doesn't work on non-Windows OS

## Upcoming features

* Bot's profile customization
* Moderating commands