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
        'refresh_token': config['TWITCH']['REFRESH_TOKEN'],
        'client_id': config['TWITCH']['CLIENT_ID'],
        'client_secret': config['TWITCH']['CLIENT_SECRET']
    })

    data = response.json()

    # Check if the response was successful and contains the expected keys
    if response.status_code == 200 and 'access_token' in data and 'refresh_token' in data:
        # Update config with new tokens
        config['TWITCH']['OAUTH_TOKEN'] = data['access_token']
        config['TWITCH']['REFRESH_TOKEN'] = data['refresh_token']

        with open('config.cfg', 'w') as file:
            config.write(file)

        print("Tokens refreshed!")
        return data['access_token'], data['refresh_token']
    else:
        print(f"Error refreshing tokens. Status Code: {response.status_code}")
        return None, None

