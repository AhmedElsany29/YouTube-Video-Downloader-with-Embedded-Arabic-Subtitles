# YouTube-Video-Downloader-with-Embedded-Arabic-Subtitles

A Streamlit-based web application to download all videos from a YouTube playlist, download Arabic subtitles (if available), and embed them as soft subtitles into each video.

## Features
- Download all videos from a YouTube playlist in MP4 format.
- Download Arabic subtitles (manual or auto-generated) in SRT format.
- Embed Arabic subtitles into each video as soft subtitles (toggleable in players like VLC).
- Provide download buttons for subtitled videos via a web interface.
- Handle cases where subtitles are unavailable for some videos.

## Prerequisites
- **Python**: Version 3.7 or higher (recommended: 3.8+).
- **FFmpeg**: Required for embedding subtitles.
  - **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (e.g., `ffmpeg-release-essentials.zip`), extract, and add `bin` to your system PATH (e.g., `C:\ffmpeg\bin`). Alternatively, install via Chocolatey:
    ```bash
    choco installshe install ffmpeg
    ```
  - **macOS**: Install via Homebrew:
    ```bash
    brew install ffmpeg
    ```
  - **Linux**: Install via package manager, e.g., on Ubuntu:
    ```bash
    sudo apt install ffmpeg
    ```
  - Verify installation:
    ```bash
    ffmpeg -version
    ```
- **System**: Windows, macOS, or Linux.

## Installation
1. Clone or download this repository to your local machine (e.g., `F:\Projects\ownload_youtube_video_with_arabic_subtitles`).
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   This installs `streamlit`, `yt-dlp`, and `ffmpeg-python`.

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your browser at `http://localhost:8501`.
3. Enter a YouTube playlist URL (e.g., `https://www.youtube.com/playlist?list=...`).
4. Click "Download and Embed Subtitles".
5. The app will:
   - Download each video and Arabic subtitles (if available) to the `downloads` folder.
   - Embed subtitles into videos, creating files like `1_Video Title_subtitled.mp4`.
   - Display download buttons for each subtitled video (or original video if no subtitles).
6. Access the `downloads` folder for files if browser downloads are slow.

## Project Structure
- `app.py`: Main Streamlit application script.
- `requirements.txt`: Lists Python dependencies.
- `downloads/`: Folder where videos and subtitles are saved.

## Troubleshooting
- **FFmpeg Not Found**:
  - Ensure FFmpeg is installed and in your system PATH.
  - Alternatively, edit `app.py` to hardcode the FFmpeg path:
    ```python
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"  # Update with your path
    if os.path.exists(ffmpeg_path):
        ffmpeg._ffmpeg_path = ffmpeg_path
    ```
- **No Arabic Subtitles**:
  - Some videos may lack Arabic subtitles. The app will download the video and provide it without subtitles.
- **Playlist Issues**:
  - Ensure the playlist is public. Private or region-locked videos may fail.
- **Large Files**:
  - Re-encoding for subtitles increases processing time. Adjust `-preset` in `app.py` (e.g., `ultrafast` for speed, `slow` for quality) if needed.
- **Anaconda Warnings**:
  - If you see warnings about `~orch` or `huggingface_hub`, clean your environment:
    ```bash
    pip uninstall torch huggingface_hub
    pip install torch huggingface_hub
    ```

## Example
Try a playlist with Arabic subtitles, such as one from an Arabic educational or news channel (e.g., Al Jazeera). The app will process each video and provide download links.

## Notes
- Files are saved in the `downloads` folder with names prefixed by playlist index (e.g., `1_Video Title_subtitled.mp4`).
- Soft subtitles can be toggled in players like VLC or MPC-HC.
- For large playlists, processing may take time due to re-encoding.

## License
MIT License
