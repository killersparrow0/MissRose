# © Mr_D_P

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
from config import Config

bot = Client(
    'MissRose',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    darkprince = f'👋 Hello @{message.from_user.username}\n\n [👋🌺](https://telegra.ph/file/04828a131605f87a0cc7b.gif)\n I\'m Meenuty, I can download songs from YouTube. Type /s song name:'
    message.reply_text(
        text=darkprince, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Owner🌺', url='https://t.me/tom_jerry_m'),
                    InlineKeyboardButton('Source💿', url='https://github.com/killersparrow0/MissRose/edit/prince/MissRoseSong_Bot.py')
                ]
            ]
        )
    )

@bot.on_message(filters.command(['s']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 Searching the song...')
    ydl_opts = {"format": "bestaudio[ext=flac]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Found nothing. Try changing the spelling a little.')
            return
    except Exception as e:
        m.edit(
            "✖️ Found Nothing. Sorry.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    m.edit("⏳Processing..")
    m.edit("⌛️Processing..")
    m.edit("⏳Processing..")
    m.edit("⌛️Processing..")
    m.edit("□ □ □ □ □ □ □ □ □ □ 0%")
    m.edit("■ □ □ □ □ □ □ □ □ □ 10%")
    m.edit("■ ■ □ □ □ □ □ □ □ □ 20%")
    m.edit("■ ■ ■ □ □ □ □ □ □ □ 30%")
    m.edit("■ ■ ■ ■ □ □ □ □ □ □ 40%")
    m.edit("■ ■ ■ ■ ■ □ □ □ □ □ 50%")
    m.edit("■ ■ ■ ■ ■ ■ □ □ □ □ 60%")
    m.edit("■ ■ ■ ■ ■ ■ ■ □ □ □ 70%")
    m.edit("■ ■ ■ ■ ■ ■ ■ ■ □ □ 80%")
    m.edit("■ ■ ■ ■ ■ ■ ■ ■ ■ □ 90%")
    m.edit("■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 100%")
   
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎧 **Title**: [{title[:35]}]({link})\n⌛️ **Duration**: `{duration}`\n👁 **Views**: `{views}`\n🎬 𝐒𝐨𝐮𝐫𝐜𝐞 : [Youtube](https://youtube.com/channel/UC8zUxxo11sqJZTkVyqj3OwQ)\n💌 𝐁𝐲 : @tom_jerry_m '
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('E____')
        m.edit('E_R_R')
        m.edit('ERROR')
        m.edit('❌ ERROR REPORT HERE NOW ⬇️')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
