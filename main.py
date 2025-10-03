import streamlit as st
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import itertools

st.set_page_config(page_title="Spotify Time Machine", layout="wide")
st.title("🎵 Spotify Time Machine")
st.write("Travel back in time and listen to Billboard Hot 100 from any date!")

date = st.date_input("Select a date to travel to:")

if st.button("Create Playlist"):

    year = str(date.year)
    url = f"https://www.billboard.com/charts/hot-100/{date}/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/140.0.0.0 Safari/537.36"
    }

    response = requests.get(url=url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    songs = soup.select("li ul li h3")
    song_names = [song.getText().strip() for song in songs]

    st.write(f"Found **{len(song_names)}** songs on Billboard Hot 100.")

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id="1c6eb194a5c248bfba9d276265d59b61",
            client_secret="17a69f5cf4594239989f23f30e52a6f6",
            redirect_uri="https://example.com",  # must match dashboard
            scope="playlist-modify-private playlist-modify-public user-read-private",
            show_dialog=True,
            cache_path="token.txt"
        ),
        requests_timeout=10
    )

    user_id = sp.current_user()["id"]
    st.success(f"Logged in as: {user_id}")

    song_uris = []
    song_data = []
    status_text = st.empty()
    spinner = itertools.cycle(["🎵", "🎶", "🎧", "🎤"])
    progress_bar = st.progress(0)

    for i, song in enumerate(song_names, start=1):
        status_text.text(f"Searching Spotify for songs... {next(spinner)}")
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            track = result["tracks"]["items"][0]
            uri = track["uri"]
            song_uris.append(uri)

            song_data.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album_cover": track["album"]["images"][0]["url"],
                "preview_url": track["preview_url"],
                "spotify_url": track["external_urls"]["spotify"]
            })
        except IndexError:
            st.warning(f"'{song}' not found on Spotify. Skipped.")

        progress_bar.progress(i / len(song_names))
        time.sleep(0.05)

    status_text.empty()


    with st.spinner("Creating your playlist on Spotify... ⏳"):
        playlist = sp.user_playlist_create(
            user=user_id,
            name=f"{date} Billboard 100",
            public=False,
            description=f"Billboard Hot 100 from {date}"
        )
        sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
        time.sleep(0.5)
    st.success(f"🎉 Playlist created! [Open Full Playlist on Spotify]({playlist['external_urls']['spotify']})")
    st.info(f"{len(song_uris)} songs were added to the playlist successfully!")

    st.subheader("🎶 Playlist Preview (3 columns)")

    for i in range(0, len(song_data), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(song_data):
                song = song_data[i + j]
                with cols[j]:
                    st.image(song["album_cover"], width=150)
                    st.markdown(f"**{song['name']}** by *{song['artist']}*")
                    if song["preview_url"]:
                        st.audio(song["preview_url"])
                    st.markdown(f"[Open on Spotify]({song['spotify_url']})")
