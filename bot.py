import discord

VERSION = "1.0.2"
CLIENT = discord.Client(intents=discord.Intents(messages=True, reactions=True, guilds=True, members=True, message_content=True))
EMOJI_ID = 1105963549479669852
NEW_NAME = "Impostor"

@CLIENT.event
async def on_message(message: discord.Message):
    if 'sus' in message.content.lower():
        on_sus(message)
    if ('this' in message.content or 'This' in message.content) and not message.author.bot:
        new_message = message.content.replace('this', '**shit**').replace('This', '**Shit**')
        await message.reply("### Did you mean shit?\n" + new_message + "*")


async def on_sus(message):
    await message.add_reaction(CLIENT.get_emoji(EMOJI_ID))
    try:
        await message.author.edit(nick=NEW_NAME + " " + message.author.nick if message.author.nick else message.author.name)
    except discord.errors.Forbidden:
        pass


print("Running version " + VERSION)
CLIENT.run('OTM0MDM2ODU2OTc3Mzc5MzQ4.GnEJua.Z4ElqxOo-wdEgAXo6fvOoIBRzF5jU0riGHy2hc')
