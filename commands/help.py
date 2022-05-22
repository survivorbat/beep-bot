import discord
from discord import ApplicationContext

from main import bot

help_text = '**Beep Bot Beeps!**\n' \
            'I was made to generate music from textual input. Use /beep and input some text while in a voice chat.\n\n' \
            'To spice things up:\n' \
            '- Wrap letters in [square brackets] to create a sequence\n' \
            '- Create chords with (parentheses)\n' \
            '- Add underscore(s) (_) after a letter to make them last longer'


def setup(_: discord.Bot) -> None:
    pass


@bot.slash_command(name='help', description='Show help')
async def instruments(ctx: ApplicationContext) -> None:
    await ctx.respond(help_text, ephemeral=True)
