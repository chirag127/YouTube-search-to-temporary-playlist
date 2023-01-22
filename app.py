import streamlit as st
import requests
from bokeh.models.widgets import Div

INVIDIOUS_URL = "https://vid.puffyan.us"


def search_videos(query, page=1):

    """
    The search_videos function searches for videos on YouTube and returns a list of video IDs.

    :param query: Search for videos
    :param page: Specify which page of search results to return
    :return: A list of video ids
    """
    # Call the Invidious API to search for videos
    url = f"{INVIDIOUS_URL}/api/v1/search?q={query}&page={page}&type=video"
    response = requests.get(url)
    data = response.json()
    # Get video URLs from search results
    video_ids = []

    views = []
    for item in data:

        views.append(item["viewCount"])

        video_ids.append(f"{item['videoId']}")

    # sort by views
    video_ids = [x for _, x in sorted(zip(views, video_ids), reverse=True)]
    return video_ids


def create_playlist(video_ids):
    """
    The create_playlist function creates a YouTube playlist using a list of video IDs.

    :param video_ids: Pass in a list of video ids
    :return: A url that can be used to create a new playlist with the given video ids
    """

    # Create a playlist using the video URLs
    playlist_url = (
        f"http://www.youtube.com/watch_videos?video_ids={','.join(video_ids)}"
    )
    return playlist_url


def main():

    st.title("Invidious Playlist Creator")

    # Get search term from user
    search_term = st.text_input("Enter a search term:")

    # Get video URLs and create playlist
    if st.button("Create Playlist"):
        video_ids = []
        for page in range(1, 3):
            video_ids.extend(search_videos(search_term, page))
        if video_ids:
            playlist_url = create_playlist(video_ids)
            st.success("Playlist created!")
            st.text("Playlist URL:")
            st.text(playlist_url)

            # make a button to copy the playlist url
            if st.button("Copy Playlist URL"):
                st.text(playlist_url)

            # make a button to open the playlist in a new tab
            if st.button("Open Playlist"):
                java_script = "window.open('about:blank', 'new_window')"
                html = f'<a href="{playlist_url}" target="_blank" onclick="{java_script}">New Tab</a>'
                div = Div(text=html)
                st.bokeh_chart(div)

            # make a button to open the playlist in the same tab
            if st.button("Open Playlist in Same Tab"):
                java_script = "window.open('about:blank', 'new_window')"
                html = f'<a href="{playlist_url}" target="_self" onclick="{java_script}">New Tab</a>'
                div = Div(text=html)
                st.bokeh_chart(div)

            # make a button to open the playlist in the youtube app
            if st.button("Open Playlist in Youtube App"):
                java_script = "window.open('about:blank', 'new_window')"
                html = f'<a href="vnd.youtube:{playlist_url}" target="_self" onclick="{java_script}">New Tab</a>'
                div = Div(text=html)
                st.bokeh_chart(div)

        else:
            st.error("No videos found.")


if __name__ == "__main__":
    main()
