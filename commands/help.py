import discord
from discord import ApplicationContext

from main import bot

help_text = '**Beep Bot Beeps!**\n' \
            'I was made to generate music from textual input. Use /beep and input some text while in a voice chat.\n\n' \
            'To spice things up:\n' \
            '- Wrap letters in [square brackets] to create a sequence\n' \
            '- Wrap letters in (parentheses) to play them all at once\n' \
            '- Add underscore(s) (_) after anything to make it last longer\n' \
            '- Use dashes (-) to add silence'


def setup(_: discord.Bot) -> None:
    pass


@bot.slash_command(name='help', description='Show help')
async def instruments(ctx: ApplicationContext) -> None:
    await ctx.respond(help_text, ephemeral=True)
