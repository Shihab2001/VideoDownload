import streamlit as st
from downloader import get_video_info, download_video

st.set_page_config(
    page_title="Easy Video Downloader",
    layout="centered"
)

st.markdown(
    """
    <style>
    button { width: 100%; font-size: 16px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬 Easy Video Downloader")
st.write("Paste a video link and download in MP4")

url = st.text_input("🔗 Paste Video Link", placeholder="https://youtube.com/...")

if url:
    with st.spinner("Fetching video details..."):
        info = get_video_info(url)

    if info:
        st.image(info["thumbnail"], use_container_width=True)
        st.subheader(info["title"])

        st.write("### Select Resolution")

        for f in info["formats"]:
            if st.button(f"⬇ Download {f['resolution']}"):
                progress = st.progress(0)

                def update_progress(p):
                    progress.progress(min(int(p), 100))

                with st.spinner("Downloading..."):
                    file_path = download_video(
                        url,
                        f["format_id"],
                        info["title"],
                        f["resolution"],
                        update_progress
                    )

                st.success("Download ready!")

                with open(file_path, "rb") as file:
                    st.download_button(
                        label="📥 Save Video",
                        data=file,
                        file_name=file_path.split("/")[-1],
                        mime="video/mp4"
                    )
    else:
        st.error("❌ Could not fetch video info")
