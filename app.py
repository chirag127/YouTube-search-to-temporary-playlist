import streamlit as st
import requests

INVIDIOUS_URL = "https://vid.puffyan.us"

def search_videos(query, page=1):
    # Call the Invidious API to search for videos
    url = f"{INVIDIOUS_URL}/api/v1/search?q={query}&page={page}&type=video"
    response = requests.get(url)
    data = response.json()
    print(data)
    # Get video URLs from search results
    video_ids = []
    for item in data:

        video_ids.append(f"{item['videoId']}")
    return video_ids

def create_playlist(video_ids):
    # Create a playlist using the video URLs
    playlist_url = f"http://www.youtube.com/watch_videos?video_ids={','.join(video_ids)}"
    return playlist_url

def main():
    st.title("Invidious Playlist Creator")

    # Get search term from user
    search_term = st.text_input("Enter a search term:")

    # Get video URLs and create playlist
    if st.button("Create Playlist"):
        video_ids = []
        for page in range(1, 5):
            video_ids.extend(search_videos(search_term, page))
        if video_ids:
            playlist_url = create_playlist(video_ids)
            st.success("Playlist created!")
            st.text("Playlist URL:")
            st.text(playlist_url)
        else:
            st.error("No videos found.")

if __name__ == "__main__":
    main()
