import discord
from discord import ApplicationContext

from beep.notes import key_notes
from main import bot

available_notes = '**Notes:**\n' + ', '.join([f'{key} = {key_notes[key]}' for key in key_notes])


def setup(_: discord.Bot) -> None:
    pass


@bot.slash_command(name='notes', description='Show available notes')
async def notes(ctx: ApplicationContext) -> None:
    await ctx.respond(available_notes, ephemeral=True)
