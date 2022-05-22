import tempfile

import discord
from discord import ApplicationContext, Option
from pretty_midi import INSTRUMENT_MAP

from beep.generate import create_beeps
from beep.config import BeepConfig, BeepParseError
from main import bot

normalized_instruments = [instrument.lower() for instrument in INSTRUMENT_MAP]


def setup(_: discord.Bot) -> None:
    pass


# TODO: Add logging instead of prints

@bot.slash_command(name='beep', description='Generate some beeps')
async def beep(ctx: ApplicationContext,
               notes: Option(str, 'From Q to /', required=True),
               instrument: Option(str, 'Instrument to use', default='Acoustic Grand Piano')) -> None:
    voice = ctx.author.voice

    if not voice:
        await ctx.respond('You need to be connected to a voice channel to use BeepBot', ephemeral=True, delete_after=5)
        return

    if instrument.lower() not in normalized_instruments:
        await ctx.respond(f'I don\'t know about the instrument {instrument}, perhaps try /instruments', ephemeral=True,
                          delete_after=5)
        return

    try:
        config = BeepConfig(
            notes_input=notes,
            instrument=instrument,
        )
    except BeepParseError as e:
        await ctx.respond(f'Something is wrong with your input: {e.message}', ephemeral=True, delete_after=5)
        return
    except Exception as e:
        print(e)
        await ctx.respond('Something was wrong with your input', ephemeral=True, delete_after=5)
        return

    with tempfile.NamedTemporaryFile(suffix='.wav') as temp_wav:
        create_beeps(config, temp_wav.name)

        # Check if the bot is already in the channel, if not, join it
        if any(bot.user.id == member.id for member in voice.channel.members):
            vc = next(client for client in bot.voice_clients if client.client.user.id == bot.user.id)
        else:
            vc = await voice.channel.connect()

        try:
            vc.play(discord.FFmpegPCMAudio(temp_wav.name))
        except Exception as e:
            print(e)
            await ctx.respond('Something went wrong, please try again in a bit', ephemeral=True, delete_after=5)
            return

        await ctx.send(f'{ctx.author.mention} played: {notes}')
