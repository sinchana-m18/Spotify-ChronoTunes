# Spotify-ChronoTunes
A Streamlit web app that lets you generate Spotify playlists from historical Billboard Hot 100 charts. Pick any date, and relive the hits of that era instantly on Spotify.
Spotify Time Machine
====================

Description
-----------
Spotify Time Machine allows users to generate Spotify playlists based on the Billboard Hot 100 chart from any historical date. 
The application scrapes Billboard data, searches for the corresponding songs on Spotify, and creates a playlist in the user's account. 
It is built with Streamlit, Spotipy (Spotify API client), and BeautifulSoup.

Features
--------
- Select any date from the past
- Scrape Billboard Hot 100 songs for that date
- Search for songs on Spotify
- Automatically create a Spotify playlist
- Preview songs with album cover, audio samples, and Spotify links

Installation
------------
1. Clone the repository:
   git clone https://github.com/sinchana-m18/Spotify-ChronoTunes.git
   cd Spotify-ChronoTunes

2. Install dependencies:
   pip install -r requirements.txt

3. Run the application locally:
   streamlit run main.py

Spotify API Setup
-----------------
1. Create an application on the Spotify Developer Dashboard:
   https://developer.spotify.com/dashboard/

2. Copy your Client ID and Client Secret.

3. Set the Redirect URI:
   - For local use: http://localhost:8501
   - For deployment: your Streamlit Cloud app URL

4. Provide your credentials securely:
   - For local: create a .streamlit/secrets.toml file with the following:
        SPOTIPY_CLIENT_ID = "your-client-id"
        SPOTIPY_CLIENT_SECRET = "your-client-secret"
        SPOTIPY_REDIRECT_URI = "https://example.com"

   - For Streamlit Cloud: use the Secrets Manager in the app settings.

Requirements
------------
- Python 3.8 or higher
- streamlit
- requests
- beautifulsoup4
- spotipy

License
-------
This project is licensed under the MIT License.
