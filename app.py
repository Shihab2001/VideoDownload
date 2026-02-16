import streamlit as st
from downloader import get_video_info, download_video

# --------------------------------------------------
# Page config (mobile friendly)
# --------------------------------------------------
st.set_page_config(
    page_title="Easy Video Downloader",
    layout="centered"
)

# --------------------------------------------------
# Simple mobile-friendly styling
# --------------------------------------------------
st.markdown(
    """
    <style>
        button {
            width: 100%;
            font-size: 16px;
            padding: 0.6em;
        }
        .stDownloadButton button {
            background-color: #4CAF50;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("🎬 Easy Video Downloader")
st.write(
    "Paste a **YouTube / Instagram / Facebook** video link and download it as **MP4**.\n\n"
    "👉 One button per resolution, clean & simple."
)

url = st.text_input(
    "🔗 Paste video link",
    placeholder="https://www.youtube.com/watch?v=..."
)

# --------------------------------------------------
# Main logic
# --------------------------------------------------
if url:
    with st.spinner("Fetching video information..."):
        info = get_video_info(url)

    if info is None:
        st.error("❌ Unable to fetch video info. Make sure the video is public.")
    else:
        # Thumbnail + title
        st.image(info["thumbnail"], use_container_width=True)
        st.subheader(info["title"])

        st.markdown("### 📥 Select Resolution")

        # info["resolutions"] is a dict like:
        # { "360p": "18", "720p": "137", ... }
        for res, format_id in info["resolutions"].items():

            if st.button(
                f"⬇ Download {res}",
                key=f"download_{res}"
            ):
                progress_bar = st.progress(0)

                def update_progress(p):
                    try:
                        progress_bar.progress(min(int(p), 100))
                    except:
                        pass

                with st.spinner("Downloading and converting to MP4..."):
                    file_path = download_video(
                        url=url,
                        resolution=res,
                        format_id=format_id,
                        title=info["title"],
                        progress_callback=update_progress
                    )

                st.success("✅ Video is ready!")

                with open(file_path, "rb") as file:
                    st.download_button(
                        label="📥 Save MP4",
                        data=file,
                        file_name=file_path.split("/")[-1],
                        mime="video/mp4",
                        key=f"save_{res}"
                    )
