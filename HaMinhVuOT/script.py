import queue
import discord
import os
import requests
import json
import gspread
import datetime
from dotenv import load_dotenv
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
#print(dict(os.environ))
#print(os.environ)
queue = []
def get_quote():
    response= requests.get("https://zenquotes.io/api/random")
    data=json.loads(response.text)
    quote=data[0]['q']+" -"+data[0]['a']
    return (quote)
bot = commands.Bot(command_prefix='$',intents=intents)
@bot.command()
async def tst(ctx):
    await ctx.send(f'Ping: {round(bot.latency*1000)}ms')
    print("check")
@bot.command()
async def inspire(ctx):
    await ctx.send(get_quote())
@bot.event
async def on_message(message):
    if(message.author==bot.user): return
    list= message.content.split("\n")
    #print(list)
    marked="[PASSED]"
    cnt=0
    for i in list:
        if marked in i:
            place=cnt
            break
        cnt=cnt+1
    sub_list=list[place].split("[PASSED]")[1]
    username_list=sub_list.split(", ")
    gs=gspread.service_account()
    sh=gs.open("Copy of |AAC| Database V2")
    wsh=sh.worksheet("3rd Wing")
    print(username_list)
    for i in username_list:
        cell=wsh.find(i.replace(" ",""))
        if(wsh.cell(cell.row,14+datetime.datetime.today().weekday()).value is None):
            wsh.update_cell(cell.row,14+datetime.datetime.today().weekday(),1)
        else:
            wsh.update_cell(cell.row,14+datetime.datetime.today().weekday(),float(wsh.cell(cell.row,14+datetime.datetime.today().weekday()).value)+1)
    await bot.process_commands(message)
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and on!")
bot.run(os.environ['TOKEN2'])