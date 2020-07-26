import discord
from discord.ext import commands
import asyncio
import requests
from bs4 import BeautifulSoup
import json
import random
import time
import os

bot = commands.Bot(command_prefix='#')

print(discord.__version__)

heroes_list = []
moved = False

@bot.event
async def on_ready():
    print("Bot is ready")
    print("Bot running on " + bot.user.name)
    print("With the id {}".format(str(bot.user.id)))


@bot.command()
async def ping(ctx):
    await ctx.send("Hello {}".format(ctx.message.author.mention))


@bot.command()
async def findxur(ctx):
    r = requests.get("https://whereisxur.com")

    # Parse whereisxur.com for link to xur image
    soup = BeautifulSoup(r.text, "lxml")
    img = soup.find("div", {"class": "et_pb_module et_pb_image et_pb_image_0"}).span.img['data-lazy-src']

    # Get filename from last characters of the img url
    filename = img[139:]

    # Check if file already exists on disk - if not, download image to file
    if not os.path.isfile("./img/" + filename):
        with open("./img/" + filename, "wb") as f:
            response = requests.get(img, stream=True)

            if response.ok:
                for block in response.iter_content(1024):
                    if not block:
                        break                  
                    f.write(block)           
            else:
                await ctx.send("Couldn't download image image of Xur's location :( pls try again later")   
    try:
        await ctx.send(file=discord.File(".\\img\\" + filename))
    except Exception as e:
        print(e)
        await ctx.send("Beep Boop whoever coded me sucks. I can't find Xur right now :(")


bot.run("<secret here>")