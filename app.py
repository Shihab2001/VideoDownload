import streamlit as st
from downloader import get_video_info, download_video
from yt_dlp.utils import DownloadError

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Easy Video Downloader",
    layout="centered"
)

# --------------------------------------------------
# Mobile-friendly CSS
# --------------------------------------------------
st.markdown(
    """
    <style>
        button {
            width: 100%;
            font-size: 16px;
            padding: 0.6em;
        }
        .error-box {
            background: #ffe6e6;
            padding: 1em;
            border-radius: 8px;
            color: #900;
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
    "Paste a **public YouTube video link**.\n\n"
    "⚠️ Some videos may fail on Streamlit Cloud due to platform blocking."
)

url = st.text_input(
    "🔗 Paste video link",
    placeholder="https://www.youtube.com/watch?v=..."
)

# --------------------------------------------------
# Logic
# --------------------------------------------------
if url:
    with st.spinner("Fetching video information..."):
        info = get_video_info(url)

    if info is None:
        st.error("❌ Could not fetch video info. Video may be private or blocked.")
        st.stop()

    st.image(info["thumbnail"], use_container_width=True)
    st.subheader(info["title"])
    st.markdown("### 📥 Select Resolution")

    for res, format_id in info["resolutions"].items():

        if st.button(f"⬇ Download {res}", key=f"download_{res}"):

            progress_bar = st.progress(0)

            def update_progress(p):
                try:
                    progress_bar.progress(min(int(p), 100))
                except:
                    pass

            try:
                with st.spinner("Downloading and converting to MP4..."):
                    file_path = download_video(
                        url=url,
                        resolution=res,
                        format_id=format_id,
                        title=info["title"],
                        progress_callback=update_progress
                    )

                st.success("✅ Video ready!")

                with open(file_path, "rb") as f:
                    st.download_button(
                        "📥 Save MP4",
                        f,
                        file_name=file_path.split("/")[-1],
                        mime="video/mp4",
                        key=f"save_{res}"
                    )

            except DownloadError:
                st.markdown(
                    """
                    <div class="error-box">
                    ❌ Download blocked (HTTP 403).<br><br>
                    This video cannot be downloaded from Streamlit Cloud.
                    <br><br>
                    ✅ Solution:
                    <ul>
                      <li>Run this app locally</li>
                      <li>Or deploy on a VPS (DigitalOcean / Railway)</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
