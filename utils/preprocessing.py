import numpy as np
import cv2
from PIL import Image

# ==== Letterbox Resize ====
def letterbox(image, new_shape=(640, 640), color=(114, 114, 114)):
    shape = image.shape[:2]  # current shape [height, width]
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw /= 2
    dh /= 2
    resized = cv2.resize(image, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return padded, r, dw, dh

# ==== Preprocessing ====
def preprocess_for_yolo(img_pil):
    img_np = np.array(img_pil)
    img_letterboxed, r, dw, dh = letterbox(img_np, new_shape=(640, 640))
    img_letterboxed = img_letterboxed.astype(np.float32) / 255.0
    img_letterboxed = img_letterboxed.transpose(2, 0, 1)  # HWC → CHW
    return np.expand_dims(img_letterboxed, axis=0), r, dw, dh

def preprocess_for_effnet(img_pil):
    img = img_pil.resize((224, 224))
    img_np = np.array(img).astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img_np = (img_np - mean) / std
    img_np = img_np.transpose(2, 0, 1)
    return np.expand_dims(img_np, axis=0).astype(np.float32)