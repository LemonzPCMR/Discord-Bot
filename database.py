import sqlite3
import os

DB_DIRECTORY = "data"
DB_PATH = os.path.join(DB_DIRECTORY, "twitch_alerts.db")


def initialize_guild_tables(guilds):
    # SQLite logic to create tables for each guild
    if not os.path.exists(DB_DIRECTORY):
        os.makedirs(DB_DIRECTORY)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for guild in guilds:
        table_name = str(guild.id)
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT NOT NULL,
            comment TEXT
        )
        ''')

    conn.commit()
    conn.close()


def add_data_to_guild_table(guild_id, username, comment):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    table_name = str(guild_id)
    cursor.execute(f'SELECT account FROM "{table_name}" WHERE account = ?', (username,))
    data = cursor.fetchone()

    if data:
        update_data_in_guild_table(guild_id, username, comment)
    else:
        cursor.execute(f'''
        INSERT INTO "{table_name}" (account, comment)
        VALUES (?, ?)
        ''', (username, comment))
        conn.commit()

    conn.close()


def update_data_in_guild_table(guild_id, username, comment):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    table_name = str(guild_id)
    cursor.execute(f'''
    UPDATE "{table_name}" SET comment = ? WHERE account = ?
    ''', (comment, username))

    conn.commit()
    conn.close()


def remove_data_from_guild_table(guild_id, username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    table_name = str(guild_id)
    cursor.execute(f'''
    DELETE FROM "{table_name}" WHERE account = ?
    ''', (username,))

    conn.commit()
    conn.close()


def retrieve_all_data_from_guild_table(guild_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    table_name = str(guild_id)
    cursor.execute(f'''
    SELECT account, comment FROM "{table_name}"
    ''')

    data = cursor.fetchall()
    conn.close()

    return data