import streamlit as st
import yt_dlp
import os

def download_playlist(playlist_url, download_folder):
    # Check if the download folder exists; if not, create it
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Set options for yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save to specified folder
        'format': 'bestvideo+bestaudio',  # Download best video and audio quality
        'noplaylist': False,  # Download the entire playlist
        'ignoreerrors': True,  # Skip errors for unavailable videos
        'geo-bypass': True,  # Bypass geographical restrictions
        'age-limit': 18,  # Skip age-restricted content if needed
        'no-post-overwrites': True,  # Skip unavailable videos
        'progress_hooks': [my_hook],  # Progress hook for feedback
    }

    # Use yt-dlp to download playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

# Hook function to display progress
def my_hook(d):
    if d['status'] == 'downloading':
        st.write(f"Downloading: {d['filename']} ({d['_percent_str']} - {d['_eta_str']})")
    elif d['status'] == 'finished':
        st.write(f"Finished downloading: {d['filename']}")

# Streamlit UI
st.title("YouTube Playlist Downloader")

st.markdown("Enter the URL of a YouTube playlist to download the videos:")

# Input: YouTube Playlist URL
playlist_url = st.text_input("Enter Playlist URL:")

# Button to trigger download
if st.button("Download Playlist"):
    if playlist_url:
        # Define download folder (Downloads directory)
        download_folder = os.path.join(os.path.expanduser("~"), 'Downloads', 'YouTubePlaylist')
        
        # Show downloading message
        st.write("Starting download... Please wait.")
        
        try:
            download_playlist(playlist_url, download_folder)
            st.success("Download completed successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid playlist URL.")
