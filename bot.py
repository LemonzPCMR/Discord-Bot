import discord
from discord import app_commands
from discord.ext import tasks
import configparser
from twitch_auth import refresh_twitch_token
from twitch_api import update_headers_with_new_token
from database import initialize_guild_tables, load_guild_data_into_memory
from commands import setup
from twitch_alert import start_twitch_alerts

# Load configuration
config = configparser.ConfigParser()
config.read('config.cfg')

TOKEN = config['DISCORD']['TOKEN']

# Initialize bot
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True
intents.presences = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
# setup commands
setup(tree)


@bot.event
async def on_ready():

    # Start commands
    await tree.sync()

    auto_refresh_token.start()

    # Initialize tables for each guild
    initialize_guild_tables(bot.guilds)

    # Load guild settings into memory
    load_guild_data_into_memory()

    # Initialize Twitch alerts
    await start_twitch_alerts(bot)


@tasks.loop(hours=3.5)  # Run every 3.5 hours to be safe
async def auto_refresh_token():
    new_access_token, new_refresh_token = refresh_twitch_token()
    update_headers_with_new_token(new_access_token)

bot.run(TOKEN)
