from discord.ext import tasks
from twitch_api import check_if_live
from embed_handler import create_live_embed
from database import guild_settings, guild_accounts

# This dictionary will keep track of streams' timestamps.
stream_timestamps = {}


@tasks.loop(minutes=1)  # Check every 1 minute
async def check_twitch_streams(bot):
    print("Checking Twitch streams.")

    for guild_id, settings in guild_settings.items():
        ALERT_CHANNEL_ID = settings["twitch_alert_channel"]
        ROLE_TO_PING = settings["twitch_ping_role"]
        ENABLE_TWITCH_PING = settings["enable_twitch_ping"]

        channel = bot.get_channel(ALERT_CHANNEL_ID)
        role = bot.get_guild(guild_id).get_role(ROLE_TO_PING)

        # Fetch usernames and comments from the global variable for the current guild
        guild_data = guild_accounts.get(guild_id, [])

        for _, username, custom_message in guild_data:

            is_live, stream_data = check_if_live(username)

            current_timestamp = stream_data["started_at"] if stream_data else None

            # Check if the timestamp has changed or if it's a new streamer we haven't seen.
            if is_live and (username not in stream_timestamps or stream_timestamps[username] != current_timestamp):
                embed = create_live_embed(stream_data, custom_message)
                message_content = f"{role.mention}" if ENABLE_TWITCH_PING else ""
                await channel.send(message_content, embed=embed)
                stream_timestamps[username] = current_timestamp

            elif not is_live and username in stream_timestamps:
                del stream_timestamps[username]  # Remove the streamer from the timestamp dict if they're offline.


async def start_twitch_alerts(bot):
    check_twitch_streams.start(bot)
