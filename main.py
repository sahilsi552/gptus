usrs = ["me",491634139,705138975]
owner = 5935034287
bot_token = "1234566:djsjfjhkfkskaskdkdk"
api_id = 793567
api_hash = "gjdkgjmfmssmdmfmfmcmdxxn"


from collections import Counter
from pyrogram import Client, filters 
from pyrogram.raw import functions, types
import time
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
import cv2
import sys
import platform
import qrcode
import asyncio
import yt_dlp
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
from tinydb import TinyDB, Query

fdb = TinyDB('filters.json')
db = TinyDB('db.json')

sapi = SafoneAPI()

app = Client("spider",api_id,api_hash,workers=50) #pyrogram userbot client 
bot = Client("spider_bot",api_id,api_hash,bot_token=bot_token) # pyrogram bot client 
ptb = Application.builder().token(bot_token).concurrent_updates(8).connection_pool_size(16).build() #python-telegram-bot client 
tlbot = TelegramClient("telethon", api_id, api_hash)
tlbot.start(bot_token=bot_token)
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



@app.on_message(filters.command("addfilter",prefixes=[".","!","/"]) & (filters.user("me") | filters.channel))
async def addfilter(c,m):
  if len(m.text.split(" ")) > 1 and m.reply_to_message and m.reply_to_message.text:
    try:
     result = fdb.search(Query().cmd == m.text.split(" ")[1])[0]["result"]
    except:
     result = None
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
  if m.chat.type == pyrogram.enums.ChatType.CHANNEL and (await c.get_chat_member(m.chat.id,(await app.get_me()).id)).status == pyrogram.enums.ChatMemberStatus.MEMBER:
    return
  if m.entities:
   is_urls = []
   for entitys in m.entities:
    if entitys.type == pyrogram.enums.MessageEntityType.URL:
     is_urls = True
     break
   if is_urls:
    text = m.text
    entities = []
    for entity in m.entities:
      if entity.type == pyrogram.enums.MessageEntityType.URL:
         entities.append(m.text[entity.offset:(entity.offset+entity.length)])
    entities = [e for e in Counter(entities)]
    for entitynies in entities:
       text = text.replace(entitynies,f"""<a href="{entitynies}">check link</a>""")
    await m.edit(text,disable_web_page_preview=True)
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
