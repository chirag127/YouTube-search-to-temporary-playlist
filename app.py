import streamlit as st
import requests

INVIDIOUS_URL = "https://vid.puffyan.us"

def search_videos(query, page=1):
    # Call the Invidious API to search for videos
    url = f"{INVIDIOUS_URL}/api/v1/search?q={query}&page={page}"
    response = requests.get(url)
    data = response.json()

    # Get video URLs from search results
    video_urls = []
    for item in data["results"]:
        video_urls.append(f"{INVIDIOUS_URL}/watch?v={item['videoId']}")
    return video_urls

def create_playlist(video_urls):
    # Create a playlist using the video URLs
    playlist_url = f"http://www.youtube.com/watch_videos?video_ids={','.join(video_urls)
    return playlist_url

def main():
    st.title("Invidious Playlist Creator")

    # Get search term from user
    search_term = st.text_input("Enter a search term:")

    # Get video URLs and create playlist
    if st.button("Create Playlist"):
        video_urls = []
        for page in range(1, 5):
            video_urls.extend(search_videos(search_term, page))
        if video_urls:
            playlist_url = create_playlist(video_urls)
            st.success("Playlist created!")
            st.text("Playlist URL:")
            st.text(playlist_url)
        else:
            st.error("No videos found.")

if __name__ == "__main__":
    main()
