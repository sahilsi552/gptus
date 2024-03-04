usrs = ["me",491634139,52670120]
owner = 59350387
bot_token = "61914g71K4dTrTlUYfZ0sF4LYNpks_yc"
api_id = 7305
api_hash = "59c3069583a89016571ba9eb9d"
gptkey = "sk-RYz6jrsHTV2QOSqpQy"

import websockets
from collections import Counter
from pyrogram import Client, filters 
from pyrogram.raw import functions, types
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import telethon
from telethon import TelegramClient, sync
from pyrogram.enums import ChatMemberStatus,ChatType
from async_eval import eval
import datetime
import telegram
from telegram.ext import Application
from telegram.constants import ParseMode
import os
import io
import sys
import platform
import qrcode
import asyncio
import yt_dlp
from io import StringIO
import emoji
import math
import calendar
import socket
import requests
import random
import pickle
from SafoneAPI import SafoneAPI
import json
import gtts
import wget
import re
from gtts import gTTS as tts
import speedtest
import pyrogram
from dotmap import DotMap
from tinydb import TinyDB, Query,where
from currency_converter import CurrencyConverter
import sqlite3
import pytz
from openai import AsyncOpenAI

sql = sqlite3.connect("sqlite.db")
fdb = TinyDB('filters.json')
db = TinyDB('db.json')
cc = CurrencyConverter()

sapi = SafoneAPI()

web = websockets.connect('ws://127.0.0.1:8000/ws/chat/score/')
app = Client("spider",api_id,api_hash,workers=50) #pyrogram userbot client 
bot = Client("spider_bot",api_id,api_hash,bot_token=bot_token) # pyrogram bot client 
ptb = Application.builder().token(bot_token).concurrent_updates(8).connection_pool_size(16).build() #python-telegram-bot client 
tlbot = TelegramClient("telethon", api_id, api_hash)
client = AsyncOpenAI(api_key=gptkey)
tlbot.start(bot_token=bot_token)
bot.start()
  

from urllib.request import urlopen,Request
def headurl(url,xx="Noe",yy="Noe"):
  urlx = BeautifulSoup(urlopen(Request(url,headers={'User-Agent': 'Mozilla/5.0'})).read(),'html.parser').text.replace("Play Games","").replace("View all games","").replace("Roulette","").replace("Blackjack","").replace("Match Over","").replace("Slots","").replace("Trending","").replace("In-Play","").replace("Match view   Match Stats          Live on Sky Sports Cricket & Sky Sports Main Event","").replace("Play Now","").split("\n")
  list = []
  for x in urlx:   
   if x.strip():
     list.append(x)
  urlx = "\n".join(list).split("Your bets have changed.")[-1].split("View odds as:")[0]
  if not (x == "Noe" and y == "Noe"):
   return "\n".join(urlx.split("\n")[xx:yy])
  else:
   return urlx


async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")



@app.on_message(filters.text & filters.regex("^#gpt")) #& (filters.user(usrs) | filters.channel)
async def chatgpt(c,m):
 if m.from_user.id == c.me.id:
  reply=await m.edit("🖥️ Generating...")
 else:
  reply=await m.reply("🖥️ Generating...")
 response = await client.chat.completions.create(messages=[{"role": "user","content": " ".join(m.text.split(" ")[1:])}],model="gpt-3.5-turbo")
 answer = "**Que. :** `" + " ".join(m.text.split(" ")[1:]) + "`\n\n**Result :** " + response.choices[0].message.content
 if len(answer) > 4090:
  return await reply.edit("❌ Result is exceed 4096 character limit..")
 await reply.edit(answer)

@app.on_edited_message(filters.text & filters.regex("^#ask") & (filters.user(usrs) | filters.channel))
async def edit(c,m):
  await chatgpt(c,m)

import time
@app.on_message(filters.command("dialog",prefixes=[".","!","/"]) & (filters.user(usrs) | filters.channel))
async def dialog(c,m):
 async for dialog in app.get_dialogs():
  if dialog.chat.type == pyrogram.enums.ChatType.PRIVATE and (await app.get_users(dialog.chat.id)).is_deleted == True:
   async for msg in app.get_chat_history(dialog.chat.id,limit=1):
    try:
     await app.invoke(pyrogram.raw.functions.messages.DeleteHistory(peer=(await app.resolve_peer(dialog.chat.id)),max_id=msg.id))
     print("Deleted")
     time.sleep(10)
    except Exception as a:
     print(a)
     time.sleep(10)
     continue


def watermark(img,png=None):
  media = img.split("/")[-1]
  if png:
    os.system(f"ffmpeg -i {media} -i {png} -filter_complex 'overlay' w_{media}")
  else:
    os.system(f"ffmpeg -i {media} -i sticker.png -filter_complex 'overlay' w_{media}")
  os.remove(media)
  res = f"w_{media}"
  return res


@app.on_message(filters.command("eval",prefixes=[".","!","/"]) & (filters.user(usrs) | filters.channel))
async def pm(client,message):
  global c,m
  c,m = client,message
  text = m.text[6:]
  try:
    vc = eval(text)
  except Exception as e:
    vc = str(e)
  try:
    await m.edit(f"Code : `{text}`\n\nResult : {str(vc)}",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
  except Exception as e:
   try:
    await m.edit(f"Code : `{text}`\n\nResult : {str(e)}",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
   except:
     pass
   with open("Result.txt" , "w") as g:
    g.writelines(str(vc))
    g.close()
   x = (await app.get_chat_member(m.chat.id,(await app.get_me()).id)).status if (m.chat.type == ChatType.SUPERGROUP) else None
   if (x == ChatMemberStatus.MEMBER) or (x == ChatMemberStatus.RESTRICTED):
     return
   try:
     await m.reply_document("Result.txt")
   except:
     return
@app.on_edited_message(filters.command("eval",prefixes=[".","!","/"]) & (filters.user(usrs) | filters.channel))
async def edit(c,m):
  await pm(c,m)

@app.on_message (filters.command("exec",prefixes=[".","!","/"]) & (filters.user(usrs) | filters.channel)) 
def compile_code(_,m): 
    output = StringIO() 
    sys.stdout= output
    code = m.text[6:]
    c = compile(code,"<string>","exec")
    try:
     exec(c)
    except:
     trace = traceback.format_exc()
     m.edit_text(f"Code:\n`{code}`\n\nTraceback: \n{trace}",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
    else:
        result = output.getvalue()
        m.edit_text(f"Code:\n`{code}`\n\nResult:\n{result if result else None}",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)


@app.on_message(filters.command("addfilter",prefixes=[".","!","/"]) & (filters.user("me") | filters.channel))
async def addfilter(c,m):
  if len(m.text.split(" ")) > 1 and m.reply_to_message and m.reply_to_message.text:
    result = fdb.get(Query().cmd == m.text.split(" ")[1])
    if result:
      fdb.update({'cmd': m.text.split(" ")[1], "result" : m.reply_to_message.text.html}, Query().cmd == m.text.split(" ")[1])
      await m.edit("**Filter successfully updated!**")
      return
    fdb.insert({'cmd': m.text.split(" ")[1], "result" : m.reply_to_message.text.html})
    await m.edit("**Filter successfully added!**")
  else:
   await m.edit("**Invalid use of command!**")
   return
@app.on_message(filters.command("rmfilter",prefixes=[".","!","/"]) & (filters.user("me") | filters.channel))
async def rmfilter(c,m):
  if len(m.text.split(" ")) < 2:
   await m.edit("**Invalid use of command!**")
   return  
  try:
   result = fdb.remove(Query().cmd == m.text.split(" ")[1])
  except:
   result = None
  if result:
    await m.edit("**Filter removed successfully!**")
    return
  await m.edit("**No filter Found!**")
  
@app.on_message(filters.command("filters",prefixes=[".","!","/"]) & (filters.user("me") | filters.channel))
async def filter(c,m):
  try:
   result = ""
   i = 1
   for item in fdb:
    result = result + str(i) + ". " + item["cmd"]+"\n"
    i += 1
   result = "**📙 Available filters: **\n" + result
  except:
   result = None
  if result:
    await m.edit(result)
    return
  await m.edit("**No filters Found!**")
  
@app.on_message(filters.command("del",prefixes=[".","!","/"]) & (filters.user("me") | filters.channel))
async def delete(c,m):
  try:
   await m.delete()
   await m.reply_to_message.delete()
  except:
   return



@app.on_message(filters.user(usrs) | filters.channel)
async def rfilter(c,m):
  if not m.reply_to_message:
    return
  try:
   result = fdb.search(Query().cmd == m.text)[0]["result"]
  except:
   result = None
  if result:
     await m.reply_to_message.reply(result,quote=True, disable_web_page_preview=True)
     await m.delete()

app.run()
