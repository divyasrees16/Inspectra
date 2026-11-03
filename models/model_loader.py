import streamlit as st
import onnxruntime as ort
from config.settings import YOLO_ONNX_PATH, EFFNET_ONNX_PATH

@st.cache_resource
def load_yolo_session():
    return ort.InferenceSession(YOLO_ONNX_PATH)

@st.cache_resource
def load_effnet_session():
    return ort.InferenceSession(EFFNET_ONNX_PATH)