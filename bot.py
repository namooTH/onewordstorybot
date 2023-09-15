from discord.ext import commands
import discord
import asyncio
import logging

print("enter your bot token")
token = input()


print("enter the channel id u want this thing to work in")
workingchannelid = input()

bot = commands.Bot(command_prefix='^',intents=discord.Intents.all())
logging.basicConfig(level=logging.INFO)

endsen = True
currentsen = ""
lastmessage = ""
lastguy = ""

@bot.event
async def on_ready():
    print('Logged in as {0.user}!'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    
    global lastguy
    global endsen
    global lastmessage
    global currentsen
    
    if message.channel.id == workingchannelid:

        if message.author == lastguy:
            warn = await message.channel.send("Please wait for someone else to write a word.", reference=message)
            await asyncio.sleep(3)
            await warn.delete()
            await message.delete()
            return

        if len(message.content.split(" ")) > 1:
            warn = await message.channel.send("Please write a single valid word.", reference=message)
            await asyncio.sleep(3)
            await warn.delete()
            await message.delete()
            return

        lastguy = message.author

        if not endsen:
            if message.content != ".":
                currentsen = currentsen + f" {message.content}"
                await lastmessage.edit(content=f"[The Content of this message is from users unfiltered and may contain offensive content the bot creator does not approve.]\nEnd the sentence with a .\n\n**{currentsen}**", allowed_mentions=discord.AllowedMentions.none())
                await message.delete()
            else:
                currentsen = currentsen + message.content
                await lastmessage.edit(content=f"[The Content of this message is from users unfiltered and may contain offensive content the bot creator does not approve.]\nEnd the sentence with a .\n\n**{currentsen}**", allowed_mentions=discord.AllowedMentions.none())
                endsen = True
                await message.delete()
        else:
             currentsen = (message.content).capitalize()
             sended = await message.channel.send(f"[The Content of this message is from users unfiltered and may contain offensive content the bot creator does not approve.]\nEnd the sentence with a .\n\n**{currentsen}**", allowed_mentions=discord.AllowedMentions.none())
             endsen = False
             lastmessage = sended
             await message.delete()


async def setup():
    async with bot:
        await bot.start(token)
asyncio.run(setup())