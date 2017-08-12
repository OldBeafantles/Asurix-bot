import discord
import asyncio
import requests
from io import BytesIO

#CONFIGURATION
c1ID = '291941571081928704'
c2ID = '345548753366810625'

with open("token.txt", "r") as f:
    token = f.read()

client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as " + client.user.name + "#" + client.user.discriminator)
    print("Looking for the 2 channels...")

    global c1
    global c2
    for s in client.servers:
        c1 = discord.utils.find(lambda c: c.id == c1ID, s.channels)
        if c1:
            break
    for s in client.servers:
        c2 = discord.utils.find(lambda c: c.id == c2ID, s.channels)
        if c2:
            break
    
    if c1:
        print("Found first channel --> " + c1.name + " in " + c1.server.name)
    else:
        print("The first channel wasn't found... The ID provided must be incorrect.")
    if c2:    
        print("Found second channel --> " + c2.name + " in " + c2.server.name)
    else:
        print("The second channel wasn't found... The ID provided must be incorrect.")

@client.event
async def on_message(msg):
    if (msg.channel.id == c1ID or msg.channel.id == c2ID) and msg.author.id != client.user.id:
        if msg.channel.id == c1ID:
            channelToSend = c2    
        elif msg.channel.id == c2ID:
            channelToSend = c1
        

        color = discord.Colour(sorted(msg.author.roles, key = lambda r: r.position, reverse=True)[0].colour.value)
        
        if not ((len(msg.embeds) != 0 and sum(len(i["url"]) for i in msg.embeds) + msg.content.count(" ") == len(msg.content)) or (len(msg.content) == 0 and len(msg.attachments) != 0)):
            embedMsg = discord.Embed(description = msg.content, colour = color)
            embedMsg.set_author(name = msg.author.name + "#" + msg.author.discriminator, icon_url = msg.author.avatar_url)
            await client.send_message(channelToSend, embed = embedMsg)

        if len(msg.embeds) != 0:
            for e in msg.embeds:
                await client.send_message(channelToSend, "`From " + msg.author.name + "#" + msg.author.discriminator + ":\n\n`" + e["url"])
                
        if len(msg.attachments) != 0:
            for a in msg.attachments:
                r = requests.get(a["url"])
                if r.status_code == 200:
                    await client.send_file(destination = channelToSend, fp = BytesIO(r.content), filename = a["filename"], content = "`From " + msg.author.name + "#" + msg.author.discriminator + "`:")

        


client.run(token)