usrs = ["me",491634139,705138975]
owner = 5935034287
bot = "6191486476:AAFwd_ePg71K4dTrTlUYfZ0sF4LYNpks_yc"
api_id = 728044
api_hash = "a41ddadc9696482aff94a4b37221574a"


from pyrogram import Client, filters 
from pyrogram.raw import functions, types
import time
from pyrogram.enums import ChatMemberStatus,ChatType
from async_eval import eval
import datetime
import telegram
import os
import asyncio
import platform
import yt_dlp
import emoji
import math
import calendar
import socket
import requests
import webbrowser
import random
import pickle
from SafoneAPI import SafoneAPI
import json
import gtts
import wget
import re
import googletrans
from gtts import gTTS as tts
import speedtest
import pyrogram
from dotmap import DotMap
from tinydb import TinyDB, Query

db = TinyDB('db.json')
sapi = SafoneAPI()

app = Client("spider",api_id,api_hash,workers=50) #spider_s
bot = Client("spider_bot",api_id,api_hash,bot_token=bot) 
bot.start()

async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")

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
    await m.edit("Code : `" + text + "`\n\nResult : " + str(vc),disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
  except Exception as e:
   try:
     await m.edit("Code : `" + text + """`\n\nResult : """ + str(e),disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
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

app.run()
