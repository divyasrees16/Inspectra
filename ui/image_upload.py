# ui/image_upload.py

import streamlit as st
import json
from datetime import datetime
from PIL import Image

from models.model_loader import load_yolo_session, load_effnet_session
from utils.detection import detect_defects_with_json
from utils.classification import classify_defect_with_json
from utils.database import write_to_influx_v1
from utils.analysis import get_groq_analysis


def render_image_upload(show_json, show_ai_analysis):

    col1, col2 = st.columns([1, 1])

    with col1:
        option = st.radio(
            "Choose Analysis Type",
            ["Detect Defects (YOLO)", "Classify Defect (EfficientNet)"]
        )

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        img_pil = Image.open(uploaded_file).convert("RGB")

        with col1:
            st.image(img_pil, caption="Uploaded Image", use_container_width=True)

        with col2:

            # =============================
            # YOLO Detection
            # =============================
            if option == "Detect Defects (YOLO)":

                st.subheader("Detection Results")

                with st.spinner("Analyzing image for defects..."):
                    yolo_sess = load_yolo_session()
                    json_results, annotated_img = detect_defects_with_json(
                        img_pil, yolo_sess
                    )
                    write_to_influx_v1(json_results)

                st.image(
                    annotated_img,
                    caption="Detection Results",
                    use_container_width=True
                )

                total_defects = json_results["summary"]["total_defects"]

                if total_defects > 0:
                    st.success(f"Found {total_defects} defects")

                    defect_types = json_results["summary"]["defect_types"]

                    summary_text = ", ".join(
                        [
                            f"{count} {defect.replace('_', ' ')}"
                            for defect, count in defect_types.items()
                        ]
                    )

                    st.info(f"**Defects:** {summary_text}")

                else:
                    st.success("No defects detected")

            # =============================
            # EfficientNet Classification
            # =============================
            elif option == "Classify Defect (EfficientNet)":

                st.subheader("Classification Results")

                with st.spinner("Classifying defect type..."):
                    effnet_sess = load_effnet_session()
                    json_results = classify_defect_with_json(
                        img_pil, effnet_sess
                    )

                top_pred = json_results["top_predictions"][0]

                st.success(
                    f"**Most Likely:** "
                    f"{top_pred['class_name'].replace('_', ' ').title()} "
                    f"({top_pred['confidence']:.1%})"
                )

                st.write("**Top 3 Predictions:**")

                for pred in json_results["top_predictions"]:
                    st.write(
                        f"{pred['rank']}. "
                        f"{pred['class_name'].replace('_', ' ').title()}: "
                        f"{pred['confidence']:.1%}"
                    )

        # =============================
        # JSON Output
        # =============================
        if show_json and "json_results" in locals():

            st.subheader("📊 JSON Output")
            st.json(json_results)

            json_str = json.dumps(json_results, indent=2)

            st.download_button(
                label="📥 Download JSON Results",
                data=json_str,
                file_name=f"defect_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        # =============================
        # AI Analysis
        # =============================
        if show_ai_analysis and "json_results" in locals():

            st.subheader("🤖 Analysis & Insights")

            analysis_type = (
                "detection"
                if option == "Detect Defects (YOLO)"
                else "classification"
            )

            ai_analysis = get_groq_analysis(
                json_results,
                analysis_type
            )

            st.markdown(ai_analysis)