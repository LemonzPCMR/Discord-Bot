from database import add_or_update_account, remove_account, update_settings
from discord import Object, utils
from database import guild_settings, guild_accounts
from twitch_alert import start_twitch_alerts_for_guild, stop_twitch_alerts_for_guild


def setup(tree):
    @tree.command(name="twitch_adduser", description="Add or update a user in the database with an optional comment.")
    async def twitch_adduser(interaction, username: str, comment: str = "Hey, I'm live now!"):
        guild_id = interaction.guild.id
        add_or_update_account(guild_id, username, comment)
        await interaction.response.send_message(f"Added/Updated {username} with comment: {comment}")

    @tree.command(name="twitch_removeuser", description="Remove a user from the database based on their username.")
    async def twitch_removeuser(interaction, username: str):
        guild_id = interaction.guild.id
        remove_account(guild_id, username)
        await interaction.response.send_message(f"Removed {username} from the database.")

    @tree.command(name="twitch_list", description="List all usernames in the database.")
    async def twitch_list(interaction):
        guild_id = interaction.guild.id
        data = guild_accounts.get(guild_id, [])
        usernames = [row[1] for row in data]  # Assuming the username is the second column
        await interaction.response.send_message(", ".join(usernames) or "No users in the database.")

    @tree.command(name="twitch_channel", description="Update the Twitch alert channel.")
    async def twitch_channel(interaction, channel_id: str):
        guild_id = interaction.guild.id
        update_settings(guild_id, "twitch_alert_channel", channel_id)
        await interaction.response.send_message(f"Updated Twitch alert channel to: {channel_id}")

    @tree.command(name="twitch_role", description="Update the Twitch ping role.")
    async def twitch_role(interaction, role_id: str):
        guild_id = interaction.guild.id
        update_settings(guild_id, "twitch_ping_role", role_id)
        await interaction.response.send_message(f"Updated Twitch ping role to: {role_id}")

    @tree.command(name="twitch_ping", description="Enable or disable Twitch pings.")
    async def twitch_ping(interaction, enable: bool):
        guild_id = interaction.guild.id
        update_settings(guild_id, "enable_twitch_ping", enable)
        await interaction.response.send_message(f"Set Twitch ping to: {enable}")

    @tree.command(name="twitch_enable", description="Enable or disable Twitch alerts.")
    async def twitch_enable(interaction, enable: bool):
        guild_id = interaction.guild.id
        current_settings = guild_settings.get(guild_id, {})

        # Check if the guild has a channel set in the globals
        if not current_settings.get("twitch_alert_channel"):
            await interaction.response.send_message(
                "Please set a Twitch alert channel first using the twitch_channel command.")
            return

        # Update the settings
        update_settings(guild_id, "enable_twitch_alerts", enable)

        # Start or stop the Twitch alerts based on the enable argument
        if enable:
            await start_twitch_alerts_for_guild(guild_id)
        else:
            await stop_twitch_alerts_for_guild(guild_id)

        await interaction.response.send_message(f"Set Twitch alerts to: {enable}")

    @tree.command(name="flower", description="Type of flower.", guild=Object(id=891586139922776094))
    async def flower(interaction, type: str):
        guild_id = interaction.guild.id

        # Replace with your role's ID
        role_id = 1142668726186037258
        role = utils.get(interaction.guild.roles, id=role_id)

        if not role:
            await interaction.response.send_message("Role not found.", ephemeral=True)
            return

        if type == "daddys":
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Welcome back little flower.", ephemeral=True)
        else:
            # Remove the role from everyone
            for member in interaction.guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
            await interaction.response.send_message("Error handling argument.", ephemeral=True)

