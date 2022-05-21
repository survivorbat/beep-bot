import os
import tempfile

import discord
from discord import ApplicationContext, Option
from pretty_midi import INSTRUMENT_MAP

from beep.cache import get_beep_instance
from beep.config import CreateConfig
from beep.notes import key_notes

bot = discord.Bot(debug_guilds=[902261535194349578, 787651775825313833])

normalized_instruments = [instrument.lower() for instrument in INSTRUMENT_MAP]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} to {len(bot.guilds)} guilds!')


@bot.slash_command(name='instruments', description='Show available instruments')
async def instruments(ctx: ApplicationContext) -> None:
    await ctx.respond(f'Available instruments: {", ".join(INSTRUMENT_MAP)}')


@bot.slash_command(name='beep', description='Generate some beeps')
async def beep(ctx: ApplicationContext,
               notes: Option(str, 'From Q to /', required=True),
               instrument: Option(str, 'Instrument to use', default='Acoustic Grand Piano'),
               note_length: Option(float, 'How long a note should last', default=0.25)) -> None:
    voice = ctx.author.voice

    if not voice:
        await ctx.respond('You need to be connected to a voice channel to use BeepBot!', ephemeral=True, delete_after=5)
        return

    if instrument.lower() not in normalized_instruments:
        await ctx.respond(f'I don\'t know about the instrument {instrument}, perhaps try /instruments', ephemeral=True, delete_after=5)
        return

    instance = get_beep_instance(ctx.guild.id)

    result = [key_notes[note.lower()] for note in str(notes) if note.lower() in key_notes]

    config = CreateConfig(
        notes=result,
        instrument=instrument,
        note_length=note_length,
    )

    with tempfile.NamedTemporaryFile(suffix='.wav') as temp_wav:
        instance.create(config, temp_wav.name)

        if any(bot.user.id == member.id for member in voice.channel.members):
            vc = next(client for client in bot.voice_clients if client.client.user.id == bot.user.id)
        else:
            vc = await voice.channel.connect()

        vc.play(discord.FFmpegPCMAudio(temp_wav.name))
        await ctx.respond(f'Playing: {", ".join(result)}', ephemeral=True)


bot.run(os.environ.get('DISCORD_TOKEN'))
