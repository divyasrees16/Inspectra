# ui/test_video.py

import streamlit as st
import cv2
from PIL import Image

from models.model_loader import load_yolo_session
from utils.detection import detect_defects_with_json
from utils.database import write_to_influx_v1


def render_test_video():

    if "run_test_video" not in st.session_state:
        st.session_state.run_test_video = False

    st.subheader("🎥 Test Video Defect Analysis")
    st.info("Offline YOLO-based defect detection on uploaded video.")

    uploaded_video = st.file_uploader(
        "Upload Test Video",
        type=["mp4", "avi", "mov"]
    )

    if uploaded_video:

        temp_video_path = f"temp_{uploaded_video.name}"

        with open(temp_video_path, "wb") as f:
            f.write(uploaded_video.read())

        cap = cv2.VideoCapture(temp_video_path)
        yolo_sess = load_yolo_session()

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        st.write(f"🎬 FPS: {int(fps)}")
        st.write(f"📦 Total Frames: {total_frames}")
        st.write(f"⏱ Duration: {duration:.2f} sec")

        frame_placeholder = st.empty()
        progress_bar = st.progress(0)

        if st.button("▶ Start Video Analysis"):
            st.session_state.run_test_video = True

        frame_count = 0

        if st.session_state.run_test_video:

            while cap.isOpened():

                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1
                frame = cv2.resize(frame, (640, 480))

                img_pil = Image.fromarray(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                )

                json_results, annotated_img = detect_defects_with_json(
                    img_pil, yolo_sess
                )

                if json_results["summary"]["total_defects"] > 0:
                    write_to_influx_v1(json_results)

                frame_placeholder.image(
                    annotated_img,
                    channels="BGR"
                )

                progress_bar.progress(
                    frame_count / total_frames
                )

            cap.release()
            st.success("✅ Video Analysis Completed")