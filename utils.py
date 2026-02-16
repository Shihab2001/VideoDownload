import subprocess
import os
import re

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def convert_to_mp4(input_file):
    if input_file.endswith(".mp4"):
        return input_file

    output_file = input_file.rsplit(".", 1)[0] + ".mp4"

    command = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-movflags", "faststart",
        "-pix_fmt", "yuv420p",
        output_file
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(input_file):
        os.remove(input_file)

    return output_file
