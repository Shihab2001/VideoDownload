import streamlit as st
from downloader import get_video_info, download_video

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Easy Video Downloader",
    layout="centered"
)

# ---------------- Mobile Friendly Styling ----------------
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

# ---------------- UI ----------------
st.title("🎬 Easy Video Downloader")
st.write("Paste a **YouTube / Instagram / Facebook** video link and download as MP4")

url = st.text_input(
    "🔗 Paste video link",
    placeholder="https://www.youtube.com/watch?v=..."
)

# ---------------- Logic ----------------
if url:
    with st.spinner("Fetching video information..."):
        info = get_video_info(url)

    if info is None:
        st.error("❌ Unable to fetch video info. Make sure the video is public.")
    else:
        st.image(info["thumbnail"], use_container_width=True)
        st.subheader(info["title"])

        st.markdown("### 📥 Select Resolution")

        for f in info["formats"]:
            if st.button(
                f"⬇ Download {f['resolution']}",
                key=f"download_{f['format_id']}"
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
                        format_id=f["format_id"],
                        title=info["title"],
                        resolution=f["resolution"],
                        progress_callback=update_progress
                    )

                st.success("✅ Video ready!")

                with open(file_path, "rb") as file:
                    st.download_button(
                        label="📥 Save MP4",
                        data=file,
                        file_name=file_path.split("/")[-1],
                        mime="video/mp4",
                        key=f"save_{f['format_id']}"
                    )
