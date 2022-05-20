import os

import discord
from discord import ApplicationContext, Option
from pretty_midi import INSTRUMENT_MAP

from beep.cache import get_beep_instance
from beep.config import CreateConfig
from beep.notes import key_notes

bot = discord.Bot(debug_guilds=[902261535194349578, 787651775825313833])


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

    if instrument not in INSTRUMENT_MAP:
        await ctx.respond(f'I don\'t know about the instrument {instrument}, perhaps try /instruments', ephemeral=True, delete_after=5)
        return

    instance = get_beep_instance(ctx.guild.id)

    result = [key_notes[note] for note in str(notes)]

    config = CreateConfig(
        notes=result,
        instrument=instrument,
        note_length=note_length,
    )

    instance.create(config, 'test.wav')

    vc = await voice.channel.connect()
    vc.play(discord.FFmpegPCMAudio('test.wav'))
    await ctx.respond(f'Playing: {", ".join(result)}', ephemeral=True)


bot.run(os.environ.get('DISCORD_TOKEN'))
