import sqlite3
import os

TWITCH_DB_DIRECTORY = "data"
TWITCH_DB_PATH = os.path.join(TWITCH_DB_DIRECTORY, "twitch_alerts.db")

# Globals
guild_settings = {}
guild_accounts = {}


def initialize_guild_tables(guilds):
    """Initialize tables for each guild if they don't exist."""

    # Ensure the directory exists
    if not os.path.exists(TWITCH_DB_DIRECTORY):
        os.makedirs(TWITCH_DB_DIRECTORY)

    conn = sqlite3.connect(TWITCH_DB_PATH)
    cursor = conn.cursor()

    for guild in guilds:
        # Create accounts table
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{guild.id}_accounts" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT NOT NULL,
            comment TEXT DEFAULT "Hey, I'm live now!"
        )
        ''')

        # Create settings table
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{guild.id}_settings" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enable_twitch_alerts BOOLEAN DEFAULT FALSE,
            enable_twitch_ping BOOLEAN DEFAULT FALSE,
            twitch_alert_channel INTEGER DEFAULT 0000,
            twitch_ping_role INTEGER DEFAULT 0000
        )
        ''')

        # Insert a default row into the settings table
        cursor.execute(f'''
        INSERT OR IGNORE INTO "{guild.id}_settings" (id, enable_twitch_alerts, enable_twitch_ping, twitch_alert_channel, twitch_ping_role)
        VALUES (1, FALSE, FALSE, 0000, 0000)
        ''')

    conn.commit()
    conn.close()


def load_guild_data_into_memory():
    """Load all guild settings and users from the database into memory."""
    global guild_settings, guild_accounts

    # Get a list of all table names from the twitch_alerts.db
    conn_twitch = sqlite3.connect(TWITCH_DB_PATH)
    cursor_twitch = conn_twitch.cursor()
    cursor_twitch.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = [name for name, in cursor_twitch.fetchall() if name[0].isdigit()]  # Filter out non-guild tables
    conn_twitch.close()

    # Extract guild IDs from the table names
    all_guild_ids = list(set(int(name.split('_')[0]) for name in all_tables))

    # For each guild ID, fetch its settings and users from twitch_alerts.db and store in the global variables
    for guild_id in all_guild_ids:
        settings = get_general_settings(guild_id)
        if settings:
            guild_settings[guild_id] = settings

        users = retrieve_all_data_from_guild_table(guild_id, "_accounts")
        if users:
            guild_accounts[guild_id] = users


def get_general_settings(guild_id):
    """Retrieve general settings for a specific guild."""

    conn = sqlite3.connect(TWITCH_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        f'SELECT enable_twitch_alerts, enable_twitch_ping, twitch_alert_channel, twitch_ping_role FROM "{guild_id}_settings" WHERE id = 1')
    data = cursor.fetchone()

    conn.close()

    if data:
        return {
            "enable_twitch_alerts": data[0],
            "enable_twitch_ping": data[1],
            "twitch_alert_channel": data[2],
            "twitch_ping_role": data[3]
        }
    else:
        return None


def retrieve_all_data_from_guild_table(guild_id, table_suffix):
    """Retrieve all data from a specific guild table."""

    conn = sqlite3.connect(TWITCH_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM "{guild_id}{table_suffix}"')
    data = cursor.fetchall()

    conn.close()
    return data

    # Accounts Database Manipulation:


def add_or_update_account(guild_id, account, comment="Hey, I'm live now!"):
    """Add or update an account in the database."""
    print(f"adduser command used for guild {guild_id}")
    conn = sqlite3.connect(TWITCH_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM "{guild_id}_accounts" WHERE account = ?', (account,))
    data = cursor.fetchone()

    if data:
        cursor.execute(f'UPDATE "{guild_id}_accounts" SET comment = ? WHERE account = ?', (comment, account))
    else:
        cursor.execute(f'INSERT INTO "{guild_id}_accounts" (account, comment) VALUES (?, ?)', (account, comment))

    conn.commit()
    conn.close()

    # Update the global variable for this specific guild
    updated_users = retrieve_all_data_from_guild_table(guild_id, "_accounts")
    guild_accounts[guild_id] = updated_users
    print(f"updating globals for {guild_id} {guild_accounts[guild_id]}")


def remove_account(guild_id, account):
    """Remove an account from the database."""

    conn = sqlite3.connect(TWITCH_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f'DELETE FROM "{guild_id}_accounts" WHERE account = ?', (account,))

    conn.commit()
    conn.close()

    # Update the global variable for this specific guild
    updated_users = retrieve_all_data_from_guild_table(guild_id, "_accounts")
    guild_accounts[guild_id] = updated_users

    # Settings Database Manipulation:


def update_settings(guild_id, enable_twitch_alerts, enable_twitch_ping, twitch_alert_channel, twitch_ping_role):
    """Update the settings for a specific guild and update the global variable."""
    global guild_settings

    conn = sqlite3.connect(TWITCH_DB_PATH)
    cursor = conn.cursor()

    # Update the settings in the database
    cursor.execute(f'''
    UPDATE "{guild_id}_settings"
    SET enable_twitch_alerts = ?, enable_twitch_ping = ?, twitch_alert_channel = ?, twitch_ping_role = ?
    WHERE id = 1
    ''', (enable_twitch_alerts, enable_twitch_ping, twitch_alert_channel, twitch_ping_role))

    conn.commit()
    conn.close()

    # Update the global variable for this specific guild
    guild_settings[guild_id] = {
        "enable_twitch_alerts": enable_twitch_alerts,
        "enable_twitch_ping": enable_twitch_ping,
        "twitch_alert_channel": twitch_alert_channel,
        "twitch_ping_role": twitch_ping_role
    }

