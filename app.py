import streamlit as st
import yt_dlp
import ffmpeg
import os

def download_youtube_playlist_with_arabic_subtitles(playlist_url, output_path="downloads"):
    """
    Download all videos and Arabic subtitles from a YouTube playlist.
    
    Args:
        playlist_url (str): YouTube playlist URL
        output_path (str): Directory to save videos and subtitles
    
    Returns:
        list: List of results containing status, paths, and messages for each video
    """
    results = []
    try:
        # Ensure output directory exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # yt-dlp options
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(playlist_index)s_%(title)s.%(ext)s'),
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitlesformat': 'srt',
            'subtitleslangs': ['ar'],
            'merge_output_format': 'mp4',
            'quiet': False,
            'no_warnings': True,
            'ignoreerrors': True,  # Continue on errors for individual videos
        }

        # Download playlist videos and subtitles
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=True)
            if 'entries' not in info:
                return [{
                    "status": "error",
                    "video_path": None,
                    "subtitle_path": None,
                    "video_title": None,
                    "message": "No videos found in the playlist or invalid URL."
                }]

            for entry in info['entries']:
                if entry is None:
                    results.append({
                        "status": "error",
                        "video_path": None,
                        "subtitle_path": None,
                        "video_title": None,
                        "message": "Failed to process a video in the playlist."
                    })
                    continue

                video_title = entry.get('title', 'Unknown Video')
                video_file = os.path.join(output_path, f"{entry.get('playlist_index', '0')}_{video_title}.mp4")
                subtitle_file = os.path.join(output_path, f"{entry.get('playlist_index', '0')}_{video_title}.ar.srt")

                results.append({
                    "status": "success",
                    "video_path": video_file,
                    "subtitle_path": subtitle_file if os.path.exists(subtitle_file) else None,
                    "video_title": video_title,
                    "message": f"Successfully downloaded video: {video_title}"
                })

        return results

    except Exception as e:
        return [{
            "status": "error",
            "video_path": None,
            "subtitle_path": None,
            "video_title": None,
            "message": f"An error occurred while downloading playlist: {str(e)}"
        }]

def embed_subtitles(video_path, subtitle_path, output_path, video_title):
    """
    Embed Arabic subtitles into a video using ffmpeg.
    
    Args:
        video_path (str): Path to the input video
        subtitle_path (str): Path to the subtitle file
        output_path (str): Directory to save the output video
        video_title (str): Title of the video
    
    Returns:
        dict: Result containing status and output video path
    """
    try:
        output_video = os.path.join(output_path, f"{video_title}_subtitled.mp4")
        
        # Escape backslashes for Windows paths in FFmpeg
        subtitle_path = subtitle_path.replace('\\', '\\\\')

        # Use ffmpeg to embed subtitles with re-encoding
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(
            stream,
            output_video,
            vf=f"subtitles='{subtitle_path}':force_style='FontName=Arial,FontSize=24'",
            vcodec='libx264',  # Re-encode video
            acodec='aac',      # Re-encode audio
            preset='fast',     # Balance speed and quality
            y=None             # Overwrite output if exists
        )
        ffmpeg.run(stream, overwrite_output=True)

        return {
            "status": "success",
            "output_video_path": output_video,
            "message": f"Successfully embedded subtitles into: {output_video}"
        }

    except Exception as e:
        return {
            "status": "error",
            "output_video_path": None,
            "message": f"An error occurred while embedding subtitles: {str(e)}"
        }

# Streamlit interface
st.title("YouTube Playlist Downloader with Embedded Arabic Subtitles")
st.write("Enter a YouTube playlist URL to download all videos and embed Arabic subtitles.")

# Input field for YouTube playlist URL
playlist_url = st.text_input("YouTube Playlist URL", placeholder="https://www.youtube.com/playlist?list=...")

# Download button
if st.button("Download and Embed Subtitles"):
    if playlist_url:
        with st.spinner("Downloading playlist videos and subtitles..."):
            # Step 1: Download playlist and subtitles
            download_results = download_youtube_playlist_with_arabic_subtitles(playlist_url)
        
        for result in download_results:
            if result["status"] == "success":
                st.success(result["message"])
                
                # Step 2: Embed subtitles if available
                if result["subtitle_path"]:
                    with st.spinner(f"Embedding subtitles into video: {result['video_title']}"):
                        embed_result = embed_subtitles(
                            result["video_path"],
                            result["subtitle_path"],
                            "downloads",
                            f"{result['video_title']}"
                        )
                    
                    if embed_result["status"] == "success":
                        st.success(embed_result["message"])
                        
                        # Provide download link for the subtitled video
                        if os.path.exists(embed_result["output_video_path"]):
                            with open(embed_result["output_video_path"], "rb") as file:
                                st.download_button(
                                    label=f"Download {result['video_title']} with Embedded Arabic Subtitles",
                                    data=file,
                                    file_name=os.path.basename(embed_result["output_video_path"]),
                                    mime="video/mp4"
                                )
                    else:
                        st.error(embed_result["message"])
                else:
                    st.warning(f"No Arabic subtitles available for video: {result['video_title']}.")
                    # Provide download link for the video without subtitles
                    if os.path.exists(result["video_path"]):
                        with open(result["video_path"], "rb") as file:
                            st.download_button(
                                label=f"Download {result['video_title']} (No Subtitles)",
                                data=file,
                                file_name=os.path.basename(result["video_path"]),
                                mime="video/mp4"
                            )
            else:
                st.error(result["message"])
    else:
        st.warning("Please enter a valid YouTube playlist URL.")