import discord


def create_live_embed(stream_data, custom_message):
    embed = discord.Embed(
        title=stream_data["title"],  # Stream title as the embed title
        color=0x00ff00,
        url=f"https://twitch.tv/{stream_data['user_name']}"
    )

    # Twitch account name, custom message, and category in the description
    embed.description = f"**{stream_data['user_name']}**\n\n{custom_message}\n\n**Category:** {stream_data['game_name']}"

    # Large thumbnail of the stream
    embed.set_image(url=stream_data["thumbnail_url"].format(width=1920, height=1080))

    # Profile picture to the right
    embed.set_thumbnail(url=stream_data["user_profile_image_url"])

    return embed
