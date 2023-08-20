import configparser
from discord.ext import commands


def load_config():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    return config


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload_config')
    @commands.is_owner()
    async def reload_config_command(self, ctx):
        global config
        config = load_config()
        await ctx.send("Config reloaded!")


def setup(bot):
    bot.add_cog(BotCommands(bot))
