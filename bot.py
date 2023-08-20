import discord
from discord.ext import commands, tasks
import configparser
from twitch_alert import start_twitch_alerts
from twitch_auth import refresh_twitch_token

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


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected!')
    auto_refresh_token.start()

    # Check if Twitch alerts are enabled in the config
    if config['TWITCH'].getboolean('ENABLE_TWITCH_ALERTS', fallback=False):
        await start_twitch_alerts(bot, config)


@tasks.loop(hours=3.5)  # Run every 3.5 hours to be safe
async def auto_refresh_token():
    refresh_twitch_token()


bot.run(TOKEN)
