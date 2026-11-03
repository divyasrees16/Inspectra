# ui/realtime.py

import streamlit as st
import cv2
import time
from PIL import Image

from models.model_loader import load_yolo_session
from utils.detection import detect_defects_with_json
from utils.database import write_to_influx_v1


PHONE_STREAM_URL = "http://192.168.137.141:8080/video"


def render_realtime():

    if "run_camera" not in st.session_state:
        st.session_state.run_camera = False

    if "last_logged" not in st.session_state:
        st.session_state.last_logged = 0

    st.subheader("📸 Real-Time Defect Detection (Phone Camera)")
    st.info("Using IP Webcam stream from your mobile device.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Start Camera"):
            st.session_state.run_camera = True

    with col2:
        if st.button("⏹ Stop Camera"):
            st.session_state.run_camera = False

    frame_placeholder = st.empty()

    if st.session_state.run_camera:

        cap = cv2.VideoCapture(PHONE_STREAM_URL)
        yolo_sess = load_yolo_session()

        while st.session_state.run_camera:

            ret, frame = cap.read()
            if not ret:
                st.error("❌ Unable to read stream.")
                break

            frame = cv2.resize(frame, (640, 480))

            img_pil = Image.fromarray(
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            )

            json_results, annotated_img = detect_defects_with_json(
                img_pil, yolo_sess
            )

            total_defects = json_results["summary"]["total_defects"]

            now = time.time()

            if total_defects > 0 and (
                now - st.session_state.last_logged > 2
            ):
                write_to_influx_v1(json_results)
                st.session_state.last_logged = now

            frame_placeholder.image(
                annotated_img,
                channels="BGR"
            )

            time.sleep(0.01)

        cap.release()