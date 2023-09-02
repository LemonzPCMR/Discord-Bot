import httpx
import configparser
from backoff_module import custom_backoff

# Load configuration
config = configparser.ConfigParser()
config.read('config.cfg')

TWITCH_STREAMS_ENDPOINT = "https://api.twitch.tv/helix/streams"
TWITCH_USERS_ENDPOINT = "https://api.twitch.tv/helix/users"
HEADERS = {
    "Client-ID": config['TWITCH']['CLIENT_ID'],
    "Authorization": f"Bearer {config['TWITCH']['OAUTH_TOKEN']}"
}

# Create a persistent httpx client
client = httpx.Client()

def update_headers_with_new_token(new_token):
    global HEADERS
    HEADERS["Authorization"] = f"Bearer {new_token}"

@custom_backoff
def check_if_live(username):
    params = {"user_login": username}
    response = client.get(TWITCH_STREAMS_ENDPOINT, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            # Stream is live
            stream_data = data["data"][0]

            # Fetch user profile image
            user_response = client.get(f"{TWITCH_USERS_ENDPOINT}?login={username}", headers=HEADERS)
            print(f"Fetching data for streamer: {username}")
            if user_response.status_code == 200:
                user_data = user_response.json()
                if user_data["data"]:
                    profile_image_url = user_data["data"][0]["profile_image_url"]
                    stream_data["user_profile_image_url"] = profile_image_url
                print(user_data)
            return True, stream_data
        else:
            # Stream is not live
            return False, None
    else:
        print(f"Error fetching data for {username}. Status Code: {response.status_code}")
        return False, None
