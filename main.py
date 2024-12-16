from pyrogram import Client,filters
from async_eval import eval as async_eval
import pyrogram
from pyrogram.enums import ChatMemberStatus,ChatType
import logging
logging.basicConfig(level=logging.INFO)
bot = "7369768633:AAEqkFbPqID4eLCdn34rjj9MaQzDvvwMsSI"
users = [8012832528]
app = Client("my_account",api_id=20892750,api_hash="b0241677a3a2958667e93fa9a632c350")
@app.on_message(filters.command("eval",prefixes=[".","!","$"]) & filters.user(users))
async def pm(client,message):
  global c,m,r
  c,m,r = client,message,message.reply_to_message
  text = m.text[6:]
  try:
    vc = str(async_eval(text))
  except Exception as e:
    vc = str(e)
  try:
    await message.reply(f"""**Input :** `{m.text}`\n\n**Output :** ```json\n{str(vc)}```""",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
  except Exception as e:
   print(e)
   try:
    await message.reply(f"""**Input :** `{m.text}`\n\n**Output :** ```json\n{str(e)}```""",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
   except:
     pass
   with open("Result.txt" , "w") as g:
    g.writelines(str(vc))
    g.close()
   x = (await app.get_chat_member(m.chat.id,(await app.get_me()).id)).status if (m.chat.type == ChatType.SUPERGROUP) else None
   if (x == ChatMemberStatus.MEMBER) or (x == ChatMemberStatus.RESTRICTED):
     return
   try:
     await message.reply_document("Result.txt")
   except:
     return

app.run()
