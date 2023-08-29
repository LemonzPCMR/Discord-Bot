from database import add_or_update_account, remove_account, update_settings
from discord import Object
from database import guild_settings, guild_accounts


def setup(tree):
    @tree.command(name="twitch_adduser", description="Add or update a user in the database with an optional comment.", guild=Object(id=956285726738219098))
    async def twitch_adduser(interaction, username: str, comment: str = "Hey, I'm live now!"):
        guild_id = interaction.guild.id
        add_or_update_account(guild_id, username, comment)
        await interaction.response.send_message(f"Added/Updated {username} with comment: {comment}")

    @tree.command(name="twitch_removeuser", description="Remove a user from the database based on their username.", guild=Object(id=956285726738219098))
    async def twitch_removeuser(interaction, username: str):
        guild_id = interaction.guild.id
        remove_account(guild_id, username)
        await interaction.response.send_message(f"Removed {username} from the database.")

    @tree.command(name="twitch_list", description="List all usernames in the database.", guild=Object(id=956285726738219098))
    async def twitch_list(interaction):
        guild_id = interaction.guild.id
        data = guild_accounts.get(guild_id, [])
        usernames = [row[0] for row in data]
        await interaction.response.send_message(", ".join(usernames) or "No users in the database.")

    @tree.command(name="twitch_channel", description="Update the Twitch alert channel.", guild=Object(id=956285726738219098))
    async def twitch_channel(interaction, channel_id: str):
        guild_id = interaction.guild.id
        current_settings = guild_settings[guild_id]
        update_settings(guild_id, current_settings["enable_twitch_alerts"], current_settings["enable_twitch_ping"], channel_id, current_settings["twitch_ping_role"])
        await interaction.response.send_message(f"Updated Twitch alert channel to: {channel_id}")

    @tree.command(name="twitch_role", description="Update the Twitch ping role.", guild=Object(id=956285726738219098))
    async def twitch_role(interaction, role_id: str):
        guild_id = interaction.guild.id
        current_settings = guild_settings[guild_id]
        update_settings(guild_id, current_settings["enable_twitch_alerts"], current_settings["enable_twitch_ping"], current_settings["twitch_alert_channel"], role_id)
        await interaction.response.send_message(f"Updated Twitch ping role to: {role_id}")

    @tree.command(name="twitch_ping", description="Enable or disable Twitch pings.", guild=Object(id=956285726738219098))
    async def twitch_ping(interaction, enable: bool):
        guild_id = interaction.guild.id
        current_settings = guild_settings[guild_id]
        update_settings(guild_id, current_settings["enable_twitch_alerts"], enable, current_settings["twitch_alert_channel"], current_settings["twitch_ping_role"])
        await interaction.response.send_message(f"Set Twitch ping to: {enable}")

    # @tree.command(name="twitch_enable", description="Enable or disable Twitch alerts.", guild=Object(id=956285726738219098))
    # async def twitch_enable(interaction, enable: bool):
    #     guild_id = interaction.guild.id
    #     current_settings = guild_settings[guild_id]
    #     update_settings(guild_id, enable, current_settings["enable_twitch_ping"], current_settings["twitch_alert_channel"], current_settings["twitch_ping_role"])
    #     await interaction.response.send_message(f"Set Twitch alerts to: {enable}")
