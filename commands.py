from discord.ext import commands
from database import add_data_to_guild_table, remove_data_from_guild_table, retrieve_all_data_from_guild_table


def setup_commands(bot):
    @bot.command(name='adduser')
    async def add_user(ctx, username: str, *, comment: str = "Hey, I'm live now!"):
        """Add or update a user in the database with an optional comment."""
        guild_id = ctx.guild.id
        data = retrieve_all_data_from_guild_table(guild_id)
        usernames = [row[0] for row in data]

        add_data_to_guild_table(guild_id, username, comment)
        if username in usernames:
            await ctx.send(f"Updated {username}'s comment to: {comment}")
        else:
            await ctx.send(f"Added {username} with comment: {comment}")

    @bot.command(name='removeuser')
    async def remove_user(ctx, username: str):
        """Remove a user from the database based on their username."""
        guild_id = ctx.guild.id
        data = retrieve_all_data_from_guild_table(guild_id)
        usernames = [row[0] for row in data]

        if username in usernames:
            remove_data_from_guild_table(guild_id, username)
            await ctx.send(f"Removed {username} from the database.")
        else:
            await ctx.send(f"{username} does not exist in the database.")

    @bot.command(name='listusers')
    async def list_users(ctx):
        """List all usernames in the database."""
        guild_id = ctx.guild.id
        data = retrieve_all_data_from_guild_table(guild_id)
        usernames = [row[0] for row in data]
        await ctx.send(", ".join(usernames) or "No users in the database.")

    # Error handling for missing arguments
    @add_user.error
    @remove_user.error
    async def user_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing arguments! Please provide the necessary information.")
