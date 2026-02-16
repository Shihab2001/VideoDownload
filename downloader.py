import yt_dlp
import os
from utils import clean_filename, convert_to_mp4

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.youtube.com/"
}

def get_video_info(url):
    ydl_opts = {
        "quiet": True,
        "http_headers": HEADERS
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    title = clean_filename(info["title"])

    # -------- Deduplicate resolutions --------
    resolutions = {}
    for f in info["formats"]:
        if f.get("height") and f.get("vcodec") != "none":
            res = f"{f['height']}p"

            # Keep first best format per resolution
            if res not in resolutions:
                resolutions[res] = f["format_id"]

    return {
        "title": title,
        "thumbnail": info["thumbnail"],
        "resolutions": resolutions  # { "720p": "137", ... }
    }


def download_video(url, resolution, format_id, title, progress_callback):
    output_template = f"{DOWNLOAD_DIR}/{title} - {resolution}.%(ext)s"

    def hook(d):
        if d["status"] == "downloading":
            percent = d.get("_percent_str", "0%").replace("%", "")
            try:
                progress_callback(float(percent))
            except:
                pass

    ydl_opts = {
        # Best video at resolution + best audio
        "format": f"bestvideo[format_id={format_id}]+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": output_template,
        "progress_hooks": [hook],
        "http_headers": HEADERS,
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)

    original_file = ydl.prepare_filename(info)
    return convert_to_mp4(original_file)
