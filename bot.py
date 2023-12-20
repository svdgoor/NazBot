import discord
import json
import threading
import time
import os 
import asyncio

settings = json.load(open("settings.json", "r"))

DATABASE_FILE = "db.json"
DB_MUTEX = False
VERSION = "1.0.2"
CLIENT = discord.Client(intents=discord.Intents(messages=True, reactions=True, guilds=True, members=True, message_content=True))
EMOJI_ID = 1105963549479669852
NEW_NAME = "Impostor"
IMPOSTOR_TIME = 60 * 60 * 24 # 24h
EMPTY_DB = {

}
SERVER_ID = 421763840938606592
IMPOSTOR_WARNING_CHANNEL_ID = 421763840938606594

if not os.path.exists(DATABASE_FILE):
    json.dump(EMPTY_DB, open(DATABASE_FILE, "w"))

def impostor_name_from_member(member):
    name = member.nick if member.nick else member.name
    name = name.replace(NEW_NAME, "").strip().replace("  ", " ")
    return NEW_NAME + " " + name[:32 - len(NEW_NAME) - 1]

# async def unnick_member(member, new_nick):
#     try:
#         await member.edit(nick=new_nick)
#     except discord.errors.Forbidden:
#         pass

# # Unnick
# def unnick():
#     time.sleep(1)
#     print("Unnick thread started.")
#     while True:
#         DB_MUTEX = True
#         data = json.load(open(DATABASE_FILE, "r"))
#         print("Checking for unnicks...")
#         for member_id in data:
#             member_stats = data[member_id]
#             if time.time() > member_stats["time"]:
#                 member = None
#                 for guild in CLIENT.guilds:
#                     if guild.get_member(int(member_id)):
#                         member = guild.get_member(int(member_id))
#                 if member:
#                     print("Unnicking " + str(member.name) + " ")
#                     if member.nick and member.nick.startswith(NEW_NAME):
#                         new_nick = member.nick.replace(NEW_NAME + " ", "").strip()
#                         asyncio.run(unnick_member(member, new_nick))
#                 data.pop(member_id)
#         print("Done.")
#         json.dump(data, open(DATABASE_FILE, "w"))
#         DB_MUTEX = False
#         time.sleep(15)

### Main function :)
async def on_sus(message):
    DB_MUTEX = True
    data = json.load(open(DATABASE_FILE, "r"))
    if str(message.author.id) in data:
        member_stats = data[str(message.author.id)]
        member_stats["time"] = time.time() + IMPOSTOR_TIME
        data[str(message.author.id)] = member_stats
    else:
        data[str(message.author.id)] = {"time": time.time() + IMPOSTOR_TIME}
    json.dump(data, open(DATABASE_FILE, "w"))
    DB_MUTEX = False
    await message.add_reaction(CLIENT.get_emoji(EMOJI_ID))
    try:
        name = impostor_name_from_member(message.author)
        print("Nicknaming " + str(message.author.name) + " to " + name)
        await message.author.edit(nick=name)
    except discord.errors.Forbidden:
        pass
    
@CLIENT.event
async def on_member_update(old_member, new_member):
    if not new_member.nick or not new_member.nick.startswith(NEW_NAME):
        DB_MUTEX = True
        data = json.load(open(DATABASE_FILE, "r"))
        if str(new_member.id) in data:
            member_stats = data[str(new_member.id)]
            ## if time is up dont renick and remove from database
            if time.time() > member_stats["time"] - 10:
                data.pop(str(new_member.id))
                json.dump(data, open(DATABASE_FILE, "w"))
                return
            else:
                # shame on you
                # reset timer
                member_stats["time"] = time.time() + IMPOSTOR_TIME
                data[str(new_member.id)] = member_stats
                json.dump(data, open(DATABASE_FILE, "w"))
                await new_member.edit(nick=impostor_name_from_member(new_member))
                # Send warning message to channel
                channel = CLIENT.get_channel(IMPOSTOR_WARNING_CHANNEL_ID)
                await channel.send("### " + new_member.mention + " tried to unnick! Shame on you! Time reset to 24h.")
        DB_MUTEX = False

@CLIENT.event
async def on_message(message: discord.Message):
    print("Message from " + str(message.author) + ": " + message.content)
    if 'sus' in message.content.lower() or message.content.lower() == "https://tenor.com/view/among-us-twerk-twerking-mason-stupid-dumb-fat-gif-19411661":
        await on_sus(message)
    if ('this' in message.content or 'This' in message.content) and not message.author.bot:
        new_message = message.content.replace('this', '**shit**').replace('This', '**Shit**')
        await message.reply("### Did you mean shit?\n" + new_message + "*")


print("Running version " + VERSION)
# threading.Thread(target=unnick).start()
CLIENT.run(settings["token"])