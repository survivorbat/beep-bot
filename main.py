import logging
import os

import discord

logging.basicConfig(level=logging.INFO)

bot = discord.Bot(debug_guilds=[902261535194349578, 787651775825313833])

bot.load_extension(name='commands.beep')
bot.load_extension(name='commands.instruments')
bot.load_extension(name='commands.help')
bot.load_extension(name='commands.notes')


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} to {len(bot.guilds)} guilds!')


bot.run(os.environ.get('DISCORD_TOKEN'))
