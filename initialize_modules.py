from twitch_alert import start_twitch_alerts
from database import guild_settings

async def initialize_twitch_alerts(bot):
    """Initialize the Twitch alerts for all guilds."""
    for guild_id, settings in guild_settings.items():
        if settings.get("enable_twitch_alerts"):
            await start_twitch_alerts(bot)
