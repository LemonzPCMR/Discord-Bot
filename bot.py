import discord
from discord.ext import commands, tasks
import configparser
from twitch_alert import start_twitch_alerts
from twitch_auth import refresh_twitch_token
from twitch_api import update_headers_with_new_token
from database import initialize_guild_tables
from commands import setup_commands


# Load configuration
config = configparser.ConfigParser()
config.read('config.cfg')

TOKEN = config['DISCORD']['TOKEN']

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)
setup_commands(bot)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected!')
    auto_refresh_token.start()

    # Initialize tables for each guild
    initialize_guild_tables(bot.guilds)

    # Check if Twitch alerts are enabled in the config
    if config['TWITCH'].getboolean('ENABLE_TWITCH_ALERTS', fallback=False):
        await start_twitch_alerts(bot, config)


# doesn't refresh the token correctly.
@tasks.loop(hours=3.5)  # Run every 3.5 hours to be safe
async def auto_refresh_token():
    new_access_token, new_refresh_token = refresh_twitch_token()
    update_headers_with_new_token(new_access_token)


bot.run(TOKEN)
