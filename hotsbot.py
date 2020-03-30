# hotsbot created by Apra

import discord
from discord.ext import commands
import asyncio
import requests
from bs4 import BeautifulSoup
import json
import random
import time

bot = commands.Bot(command_prefix='#')

print(discord.__version__)

heroes_list = []
moved = False

@bot.event
async def on_ready():
    print("HotsBot is ready")
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
async def patch(ctx):
  target = "https://heroespatchnotes.com"
  #store html from HTTPGET request to specified URL
  r = requests.get(target)
  #check that connection to target url was successful
  if (r.status_code != 200):
      raise ValueError("Failed to connect to target url: %s" %target)
  else:
      #parse html from request to BeautifulSoup for indexing
      soup = BeautifulSoup(r.text, 'html.parser')
      #find the patch list in the page
  #patch_list = soup.find("table", {"class":"table table-striped table-hover"})
  latest_url = soup.find("a", {'class':'hpn'})
  r2 = requests.get(target + "/patch/2018-05-09-balance-update.html")
  if (r2.status_code != 200):
    raise ValueError("Failed to connect to target url: %s" %target)
  else: 
    await ctx.send("Fetching latest patch notes...\n" + target + latest_url['href'])  


@bot.command()
async def builds(ctx, hero):
  # ************************** DO SOME INPUT VALIDATION HERE - HEROES_LIST - *********************************
  target = "http://hotsbuilds.info/" + hero
  r = requests.get(target)
  if(r.status_code != 200):
    raise ValueError("error conecting to " + target)  
  else:
    print("successfully connected to http://hotsbuilds.info")
    soup = BeautifulSoup(r.content, "html.parser")
    builds = soup.find('div', id="icyveins").find('div', class_="talents").find_all('tbody')
    for build in builds:
      embed = discord.Embed(title = "IcyVeins {} for {}".format(build['id'], hero), color=0x00ff00)
      for tr in build.find_all('tr'):
        for td in tr.find_all('td'):
          if(td.has_attr('class')):
            embed.add_field(name="Level {}".format(td.text), value="{}".format(td.find_next().text))
      await ctx.send(embed=embed)


@bot.command()
async def tierlist(ctx):
  r = requests.get("http://robogrub.com/silvertierlist_api")
  if(r.status_code != 200):
    raise ValueError("Error connecting to http://robogrub.com/silvertierlist_api")
  else:
    json_data = json.loads(r.text)
    tiers = [["s", "S Tier"], ["t1", "Tier 1"], ["t2", "Tier 2"], ["t3", "Tier 3"]]
    embed = discord.Embed(title = "Grubby's HotS Tier List", color=0x00ff00)
    for tier in tiers:
      heroes = []
      for hero in json_data[tier[0]]:
        heroes.append(hero["id"])
      embed.add_field(name="{}".format(tier[1]), value="{}".format(heroes))
  await ctx.send(embed=embed)




bot.run("")
