import configparser
import httpx


def refresh_twitch_token():
    TOKEN_ENDPOINT = 'https://id.twitch.tv/oauth2/token'

    # Load current config
    config = configparser.ConfigParser()
    config.read('config.cfg')

    # Request new tokens
    response = httpx.post(TOKEN_ENDPOINT, data={
        'grant_type': 'refresh_token',
        'refresh_token': config['DEFAULT']['TWITCH_REFRESH_TOKEN'],
        'client_id': config['DEFAULT']['TWITCH_CLIENT_ID'],
        'client_secret': config['DEFAULT']['TWITCH_CLIENT_SECRET']
    })

    data = response.json()

    # Update config with new tokens
    config['DEFAULT']['TWITCH_OAUTH_TOKEN'] = data['access_token']
    config['DEFAULT']['TWITCH_REFRESH_TOKEN'] = data['refresh_token']

    with open('config.cfg', 'w') as file:
        config.write(file)

    print("Tokens refreshed!")
