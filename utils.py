import configparser

def load_config(config_file='config.cfg'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def get_discord_settings(config):
    try:
        if 'DISCORD' not in config:
            raise KeyError("DISCORD section not found in config!")

        ALERT_CHANNEL_ID = int(config['DISCORD']['alert_channel_id'])
        ROLE_TO_PING = int(config['DISCORD']['role_to_ping'])
        return ALERT_CHANNEL_ID, ROLE_TO_PING

    except KeyError as e:
        print(f"Error in config: {e}")
        return None, None
