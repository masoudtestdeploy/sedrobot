import asyncio
from cgitb import text
from pyrogram import Client , filters
from pyrogram.types import Message , messages_and_media
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton , ReplyKeyboardMarkup , CallbackQuery
from typing import Any, Optional
import re
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import quote_plus
from seedr import SeedrAPI
import math, os, time, shutil


api_id = 2669389
api_hash = "59f112100d19186dc03cd93fb7f2904a"
bot_token = "1026408788:AAHVhIKmeboveGZ6x8peMnv0Ts2FvR38b_0"

bot = Client(
    "withrap",
    api_id=api_id, 
    api_hash=api_hash,
    bot_token=bot_token
)
START_BUTTONS = InlineKeyboardMarkup(

    [[    
    InlineKeyboardButton('💡Help💡', callback_data='help')
    ]]
 )
two_BUTTONS = InlineKeyboardMarkup(

    [
        [
            InlineKeyboardButton('💡Help💡', callback_data='help')
        ],
        [    
            InlineKeyboardButton('🔐Close🔐', callback_data='close')
        ]
    ]
)
help_tetx = '''

ارسال عکس  : /photo 
ارسال اهنگ : /audio
راهنما : /help
'''

start_time = time.time()
seedr = SeedrAPI(email="masoudakhoondi1@gmail.com", password="12345678")

# Def Get Info
def human_readable_size(size, decimal_places=3):
    for unit in ['B','KiB','MiB','GiB','TiB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f}{unit}"
def Get_Folders_ID():
    num = 0 
    output = ''
    Get_Drives = seedr.get_drive()
    #foldercount = len(Get_Drives["folders"])
    folders = Get_Drives["folders"]
    for i in folders:
        idd = folders[num]["id"]
        name = folders[num]["name"]

        size = human_readable_size(folders[num]["size"])

        out = "نام فایل :\n{} \nدانلود فولدر : /get_{} \nحجم فولدر : {} \n\n++++++++++++++\n\n".format(name,idd,size)
        num = num+1
        output = str(out + output)

    space_used = human_readable_size(Get_Drives["space_used"])
    space_max = human_readable_size(Get_Drives["space_max"])
    siz = "کل فضای شما : {} \nفضای مصرفی شما : {}".format(space_max,space_used)
    output = str(output + siz)
    return output
def Get_Files_ID(ID):
    num = 0 
    output = []
    Get_Folder = seedr.get_folder(ID)
    #foldercount = len(Get_Drives["folders"])
    filesss = Get_Folder["files"]
    for i in filesss:
        idd = filesss[num]["folder_file_id"]
        name = filesss[num]["name"]

        sizz = human_readable_size(filesss[num]["size"])
        out = {"id" : idd , "name" : name , "size" : sizz}
        num = num+1
        output.append(out)
        
    return output
def Get_Link(ID):
    Get_File_link = seedr.get_file(ID)["url"]
    return Get_File_link
def resualt_text(ID_File):
    All = Get_Files_ID(ID_File)
    num = 0 
    output = ''
    for i in All:
        name = All[num]["name"]
        ids =  All[num]["id"]
        size =  All[num]["size"]

        Link = Get_Link(ids)
        text = "نام فایل : {} \nلینک دانلود : \n{}\nحجم فایل : {}\nدانلود فایل : /dl_{}\n\n++++++++++++++\n\n".format(name,Link,size,ids)
        num = num+1
        output = output + str(text)


    return output
def Add_TR(Magnet):
    output = seedr.add_torrent(Magnet)
    if output["result"] == 'not_enough_space_added_to_wishlist':
        title = output['wt']["title"]
        res = {'stat':'not_enough_space_added_to_wishlist',"name":title}
    elif output["code"] == 200 :
        title = output["title"]
        res = {'stat':'ok',"name": title}
    else :
        res = {'stat':'no',"name": ""}
    
    return res

async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


@bot.on_message(filters.command("start"))
async def start_command(bot, message):
    await bot.send_message(message.chat.id , "سلام \n شروع مجدد : /start\n دیدن پوشه ها : /showfile")
@bot.on_message(filters.command("showfile"))
async def getfile_command(bot, message):
    textt = Get_Folders_ID()
    await message.reply_text(textt)

@bot.on_message(filters.private & filters.regex(pattern=".*get.*"))
async def get_file_info(bot, message):
    await message.reply_text('لطفا کمی صبر کنید ...')
    pattern_link = re.compile(r'^\/get_(.*)')
    matches_link = pattern_link.search(str(message.text))
    p_id = matches_link.group(1)
    texttt = resualt_text(p_id)
    await message.reply_text(texttt)

@bot.on_message(filters.private & filters.regex(pattern=".*del.*"))
async def del_file_info(bot, message):
    await message.reply_text('این فولدر با موفقیت حذف شد')
    pattern_link = re.compile(r'^\/del_(.*)')
    matches_link = pattern_link.search(str(message.text))
    p_id = matches_link.group(1)
    seedr.delete_folder(p_id)

@bot.on_message(filters.private & filters.regex(pattern=".*dl.*"))
async def del_file_info(bot, message):
    await message.reply_text('000')
    pattern_link = re.compile(r'^\/dl_(.*)')
    matches_link = pattern_link.search(str(message.text))
    p_id = matches_link.group(1)
    

@bot.on_message(filters.private & filters.regex(pattern=".*magnet.*"))
async def add_file(bot, message):
    await message.reply_text('فایل شما برای تبدیل ثبت شد ... تا زمان دانلود میتوانید از بخش /showfile پیگیری کنید')
    Add_TR(message.text)
    
    stat = Add_TR['stat']
    if stat == 'ok':
        name = Add_TR['name']
        await message.reply_text("فایل با نام ")

        await message.reply_text("فایل با نام "+'{}'+" ثبت شد ".format(name))
    elif stat == 'not_enough_space_added_to_wishlist':
        await message.reply_text("فضای کافی ندارید")
    else:
        await message.reply_text("خطایی رخ داده است ")

@bot.on_message(filters.command("help"))
async def help_command(bot, message):
    await message.reply_text(help_tetx,reply_markup=START_BUTTONS)

@bot.on_message(filters.command("photo"))
async def photo_command(bot, message):
    await bot.send_photo(message.chat.id , "https://img.freepik.com/free-vector/cute-white-cat-cartoon-vector-illustration_42750-808.jpg?w=740")

@bot.on_message(filters.command("audio"))
async def audio_command(bot, message):
    await bot.send_audio(message.chat.id , "CQACAgQAAxkBAAMwYqRcGlQyS2Df1-Xv2D5dO9UAAa4TAALBIgACMHk4UETTPPye8HEeHgQ")

#@bot.on_message(filters.text)
#async def echobot(client, message):
#    await message.reply_text(message.text)


@bot.on_callback_query()
async def callbackuery(client,CallbackQuery):
    if CallbackQuery.data == "about" :

        await CallbackQuery.edit_message_text(
            "این یک ربات تستی از کتابخانه پایروگرام میباشد ",
            reply_markup=two_BUTTONS
        )
    elif CallbackQuery.data == "help" :
        await CallbackQuery.edit_message_text(
            help_tetx,
            reply_markup=two_BUTTONS
        )
    else :
        async def dels(bot, message):
            await message.delete()


#@bot.on_message((filters.text))
#async def private_receive_handler(c: Client, m: Message):

#    await m.reply_text(

#        text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link),
#        parse_mode="HTML", 
#        quote=True,
#        disable_web_page_preview=True
#    )


print('im alive')
bot.run()
