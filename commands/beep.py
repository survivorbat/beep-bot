import logging
import tempfile

import discord
from discord import ApplicationContext, Option
from discord.utils import get
from pretty_midi import INSTRUMENT_MAP

from beep.generate import create_beeps
from beep.config import BeepConfig, BeepParseError
from main import bot

normalized_instruments = [instrument.lower() for instrument in INSTRUMENT_MAP]


def setup(_: discord.Bot) -> None:
    pass


@bot.slash_command(name='beep', description='Generate music!')
async def beep(ctx: ApplicationContext,
               notes: Option(str, 'From /notes, use /help for all options/effects', required=True),
               instrument: Option(str, 'Instrument from /instruments', default='Acoustic Grand Piano')) -> None:
    voice = ctx.author.voice

    if not voice:
        await ctx.respond('You need to be connected to a voice channel to use BeepBot', ephemeral=True, delete_after=5)
        return

    if instrument.lower() not in normalized_instruments:
        await ctx.respond(f'I don\'t know about the instrument {instrument}, perhaps try /instruments', ephemeral=True,
                          delete_after=5)
        return

    logging.info(f'Creating music for guild {ctx.guild.name}: {notes}')

    try:
        config = BeepConfig(
            notes_input=notes,
            instrument=instrument,
        )
    except BeepParseError as e:
        await ctx.respond(f'Something is wrong with your input: {e.message}', ephemeral=True, delete_after=5)
        return
    except Exception as e:
        logging.exception(e)
        await ctx.respond('Something was wrong with your input', ephemeral=True, delete_after=5)
        return

    with tempfile.NamedTemporaryFile(suffix='.wav') as temp_wav:
        create_beeps(config, temp_wav.name)

        # Check if the bot is already in the channel, if not, join it
        vc = get(bot.voice_clients, guild=ctx.guild)

        if vc is None:
            vc = await voice.channel.connect()

        try:
            vc.play(discord.FFmpegPCMAudio(temp_wav.name), after=lambda: (await vc.disconnect() for _ in '_').__anext__())
        except Exception as e:
            logging.exception(e)
            await ctx.respond('Something went wrong, please try again in a bit', ephemeral=True, delete_after=5)
            return

        await ctx.respond(f'{ctx.author.mention} on _{instrument}_ played: {notes}')
