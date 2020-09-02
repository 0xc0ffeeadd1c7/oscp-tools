#!/usr/bin/env python3
import discord
from discord.ext import commands, tasks
import asyncio
import requests
import requests.auth
import praw
from bs4 import BeautifulSoup
import json
import random
import time
import os

bot = commands.Bot(command_prefix='#')

print(discord.__version__)


async def get_destiny_memes(ctx):
    reddit = praw.Reddit(client_id="",
                         client_secret="",
                         password="",
                         user_agent="destinymemes bot 0.1",
                         username="")

    subreddit = reddit.subreddit("destiny2")

    dankest_meme = ""
    most_updoots = 0

    for submission in subreddit.stream.submissions():
        if submission.link_flair_text == "Meme / Humour":
            embed = discord.Embed(title = submission.title, color=0x00ff00)
            embed.set_image(url=submission.url)
            await bot.get_channel('').send(embed = embed)
    await asyncio.sleep(60*60*24)


@bot.event
async def on_ready():
    print("Bot is ready")
    print("Bot running on " + bot.user.name)
    print("With the id {}".format(str(bot.user.id)))

@bot.event
async def on_voice_state_update(member, before, after):
    if str(member) == "BloodyMany#0585":
        time.sleep(random.randrange(60, 300))
        for guild in bot.guilds:
            chann = random.choice(guild.voice_channels)
            await member.edit(voice_channel=chann)


@bot.command()
async def ping(ctx):
    await ctx.send("Hello {}".format(ctx.message.author.mention))


@bot.command()
async def findxur(ctx):
    r = requests.get("https://whereisxur.com")

    # Parse whereisxur.com for link to xur image
    soup = BeautifulSoup(r.text, "lxml")
    location = soup.find("div", {"class": "et_pb_countdown_timer_container clearfix"}).h4.contents[0]
    img = soup.find("div", {"class": "et_pb_module et_pb_image et_pb_image_0"}).span.img['data-lazy-src']

    if "Xûr is on" in location:
        try:
            embed = discord.Embed(title = location, color=0x00ff00)
            embed.set_image(url=img)
            await ctx.send(embed = embed)
            #await ctx.send(file=discord.File(".\\img\\" + filename))
        except Exception as e:
            print(e)
            await ctx.send("Beep Boop whoever coded me sucks. I can't find Xur right now :(")
    else:
        await ctx.send("Xûr isn't available rn")

@bot.loop.create_task(get_destiny_memes)

bot.run("<secret here>")
