import discord
from discord import ApplicationContext
from pretty_midi import INSTRUMENT_MAP

from main import bot

instrument_return = '**Available instruments**:\n' + ', '.join(INSTRUMENT_MAP)


def setup(_: discord.Bot) -> None:
    pass


@bot.slash_command(name='instruments', description='Show available instruments')
async def instruments(ctx: ApplicationContext) -> None:
    await ctx.respond(instrument_return, ephemeral=True)
