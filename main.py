from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
SPOTIFY_USERNAME = os.environ["SPOTIFY_USERNAME"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)
BILLBOARD_WEBSITE = response.text

# Scraping Billboard 100
soup = BeautifulSoup(BILLBOARD_WEBSITE, "html.parser")
titles = soup.select(selector="li ul li h3")
song_title = [song.getText().strip() for song in titles]

# Spotify Authentication
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                    client_secret=SPOTIFY_CLIENT_SECRET,
                                                    redirect_uri=SPOTIFY_REDIRECT_URI,
                                                    scope="playlist-modify-private",
                                                    show_dialog=True,
                                                    cache_path="./token.txt",
                                                    username=SPOTIFY_USERNAME,
                                                    )
                          )


user_id = spotify.current_user()["id"]
year = date.split("-")[0]

# Searching Spotify for songs by title
song_uris = []
for song in song_title:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


# Creating Playlist in Spotify
playlist = spotify.user_playlist_create(user=user_id,
                                        name=f"Billboard Hot 100 as at {date}",
                                        public=False
                                        )


# Adding songs to playlist.
spotify.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

