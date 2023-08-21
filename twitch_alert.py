from discord.ext import tasks
from twitch_api import check_if_live
from embed_handler import create_live_embed
from database import retrieve_all_data_from_guild_table

# This dictionary will keep track of streams' timestamps.
stream_timestamps = {}


@tasks.loop(minutes=1)  # Check every 10 minutes
async def check_twitch_streams(bot, config):
    print("Checking Twitch streams.")

    ALERT_CHANNEL_ID = int(config['TWITCH']['ALERT_CHANNEL_ID'])
    ROLE_TO_PING = int(config['TWITCH']['ROLE_TO_PING'])

    channel = bot.get_channel(ALERT_CHANNEL_ID)
    role = bot.get_guild(channel.guild.id).get_role(ROLE_TO_PING)

    # Fetch usernames and comments from the database for the current guild
    guild_data = retrieve_all_data_from_guild_table(channel.guild.id)

    for username, custom_message in guild_data:
        is_live, stream_data = check_if_live(username)

        current_timestamp = stream_data["started_at"] if stream_data else None

        # Check if the timestamp has changed or if it's a new streamer we haven't seen.
        if is_live and (username not in stream_timestamps or stream_timestamps[username] != current_timestamp):
            embed = create_live_embed(stream_data, custom_message)
            await channel.send(f"{role.mention}", embed=embed)
            stream_timestamps[username] = current_timestamp

        elif not is_live and username in stream_timestamps:
            del stream_timestamps[username]  # Remove the streamer from the timestamp dict if they're offline.


async def start_twitch_alerts(bot, config):
    check_twitch_streams.start(bot, config)
