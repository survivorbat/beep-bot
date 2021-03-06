import logging
import tempfile

import discord
from discord import ApplicationContext, Option
from pretty_midi import INSTRUMENT_MAP

from beep.config import BeepConfig, BeepParseError
from beep.generate import create_beeps
from main import bot

normalized_instruments = [instrument.lower() for instrument in INSTRUMENT_MAP]


def setup(_: discord.Bot) -> None:
    pass


@bot.slash_command(name='beep', description='Generate music!')
async def beep(ctx: ApplicationContext,
               notes: Option(str, 'From /notes, use /help for all options/effects', required=True),
               instrument: Option(str, 'Instrument from /instruments', default='Acoustic Grand Piano')) -> None:
    author_voice = ctx.author.voice

    if not author_voice:
        await ctx.respond('You need to be connected to a voice channel to use BeepBot', ephemeral=True)
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
        await ctx.respond(f'{notes}: {e.message}', ephemeral=True)
        return
    except Exception as e:
        logging.exception(e)
        await ctx.respond(f'{notes}: Something was wrong with your input', ephemeral=True)
        return

    with tempfile.NamedTemporaryFile(suffix='.wav') as temp_wav:
        create_beeps(config, temp_wav.name)

        # Check if the bot is already in the channel, if not, join it
        vc = ctx.guild.voice_client

        if vc is not None and vc.channel != author_voice.channel:
            # TODO: Figure out how to properly switch
            await ctx.respond(f'I\'m already connected to another voice channel, switching is scary :(')
            return

        if vc is None:
            logging.info(f'Not yet connected, connecting to: {author_voice.channel.name}')
            vc = await author_voice.channel.connect()
        else:
            logging.info(f'Using existing voice connection to channel: {author_voice.channel.name}')

        try:
            logging.info(f'Playing {temp_wav.name} in {author_voice.channel.name}')
            vc.play(discord.FFmpegPCMAudio(temp_wav.name))
        except Exception as e:
            logging.exception(e)
            await ctx.respond('Something went wrong, please try again in a bit', ephemeral=True)
            return

        await ctx.respond(f'{ctx.author.mention} on _{instrument}_ played: {notes}')
