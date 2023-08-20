from discord.ext import tasks
from twitch_api import check_if_live
from embed_handler import create_live_embed

# This set will keep track of streams we've alerted for.
alerted_streams = set()


@tasks.loop(minutes=1)
async def check_twitch_streams(bot, config):
    print("Checking Twitch streams.")

    ALERT_CHANNEL_ID = int(config['DEFAULT']['DISCORD_ALERT_CHANNEL_ID'])
    ROLE_TO_PING = int(config['DEFAULT']['ROLE_TO_PING'])
    TWITCH_ACCOUNTS = [section for section in config.sections()]

    channel = bot.get_channel(ALERT_CHANNEL_ID)
    role = bot.get_guild(channel.guild.id).get_role(ROLE_TO_PING)

    for account in TWITCH_ACCOUNTS:
        username = account
        custom_message = config[account]['custom_message']
        is_live, stream_data = check_if_live(username)

        if is_live and username not in alerted_streams:
            embed = create_live_embed(stream_data, custom_message)
            await channel.send(f"{role.mention}", embed=embed)
            alerted_streams.add(username)

        elif not is_live and username in alerted_streams:
            alerted_streams.remove(username)


async def start_twitch_alerts(bot, config):
    check_twitch_streams.start(bot, config)
