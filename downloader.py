import yt_dlp
import os
from utils import convert_to_mp4, clean_filename

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_video_info(url):
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        try:
            info = ydl.extract_info(url, download=False)

            formats = []
            for f in info["formats"]:
                if f.get("height") and f.get("vcodec") != "none":
                    formats.append({
                        "format_id": f["format_id"],
                        "resolution": f"{f['height']}p",
                        "ext": f["ext"]
                    })

            return {
                "title": clean_filename(info["title"]),
                "thumbnail": info["thumbnail"],
                "formats": formats
            }
        except:
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
        "progress_hooks": [hook],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)

    original_file = ydl.prepare_filename(info)
    return convert_to_mp4(original_file)
