import yt_dlp
import os
from utils import convert_to_mp4, clean_filename

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

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            formats = []
            for f in info["formats"]:
                if f.get("height") and f.get("vcodec") != "none":
                    formats.append({
                        "format_id": f["format_id"],
                        "resolution": f"{f['height']}p"
                    })

            return {
                "title": clean_filename(info["title"]),
                "thumbnail": info["thumbnail"],
                "formats": formats
            }
    except Exception as e:
        return None


def download_video(url, format_id, title, resolution, progress_callback):
    output_template = f"{DOWNLOAD_DIR}/{title} - {resolution}.%(ext)s"

    def hook(d):
        if d["status"] == "downloading":
            percent = d.get("_percent_str", "0%").replace("%", "")
            try:
                progress_callback(float(percent))
            except:
                pass

    ydl_opts = {
        "format": format_id,
        "outtmpl": output_template,
        "merge_output_format": "mp4",
        "progress_hooks": [hook],
        "http_headers": HEADERS,
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)

    original_file = ydl.prepare_filename(info)
    return convert_to_mp4(original_file)
