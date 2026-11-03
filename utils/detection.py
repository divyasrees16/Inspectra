
# utils/detection.py

import numpy as np
import cv2
from datetime import datetime
from config.settings import CLASS_NAMES_YOLO
from utils.preprocessing import preprocess_for_yolo


# =====================================
# Position Description Helper
# =====================================
def get_position_description(x_center, y_center, img_width, img_height):

    x_rel = x_center / img_width
    y_rel = y_center / img_height

    # Horizontal
    if x_rel < 0.33:
        h_pos = "left"
    elif x_rel < 0.67:
        h_pos = "center"
    else:
        h_pos = "right"

    # Vertical
    if y_rel < 0.33:
        v_pos = "top"
    elif y_rel < 0.67:
        v_pos = "middle"
    else:
        v_pos = "bottom"

    if h_pos == "center" and v_pos == "middle":
        return "center"
    elif h_pos == "center":
        return v_pos
    elif v_pos == "middle":
        return h_pos
    else:
        return f"{v_pos} {h_pos}"


# =====================================
# Size Category Helper
# =====================================
def calculate_defect_size(x1, y1, x2, y2, img_width, img_height):

    area = abs((x2 - x1) * (y2 - y1))
    img_area = img_width * img_height
    relative_area = area / img_area

    if relative_area < 0.01:
        return "small"
    elif relative_area < 0.05:
        return "medium"
    else:
        return "large"


# =====================================
# YOLO Detection with JSON Output
# =====================================
def detect_defects_with_json(img_pil, yolo_sess):

    input_tensor, r, dw, dh = preprocess_for_yolo(img_pil)

    input_name = yolo_sess.get_inputs()[0].name
    detections = yolo_sess.run(None, {input_name: input_tensor})[0]

    if detections.ndim == 3:
        detections = detections[0]

    img_width, img_height = img_pil.size

    detection_results = {
        "timestamp": datetime.now().isoformat(),
        "image_dimensions": {
            "width": img_width,
            "height": img_height
        },
        "model_info": {
            "type": "YOLO",
            "confidence_threshold": 0.3
        },
        "detections": [],
        "summary": {
            "total_defects": 0,
            "defect_types": {}
        }
    }

    img_np = np.array(img_pil)
    defect_counts = {}

    for det in detections:

        det = det.flatten()

        if len(det) < 6 or det[4] < 0.3:
            continue

        # Scale back bounding box
        x1 = int((det[0] - dw) / r)
        y1 = int((det[1] - dh) / r)
        x2 = int((det[2] - dw) / r)
        y2 = int((det[3] - dh) / r)

        conf = float(det[4])
        cls_id = int(det[5])

        if 0 <= cls_id < len(CLASS_NAMES_YOLO):

            class_name = CLASS_NAMES_YOLO[cls_id]

            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2

            position_desc = get_position_description(
                x_center,
                y_center,
                img_width,
                img_height
            )

            size_category = calculate_defect_size(
                x1,
                y1,
                x2,
                y2,
                img_width,
                img_height
            )

            detection_info = {
                "detection_id": len(detection_results["detections"]) + 1,
                "class_name": class_name,
                "confidence": conf,
                "bounding_box": {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "center_x": x_center,
                    "center_y": y_center
                },
                "position_description": position_desc,
                "size_category": size_category,
                "area_pixels": abs((x2 - x1) * (y2 - y1))
            }

            detection_results["detections"].append(detection_info)

            defect_counts[class_name] = defect_counts.get(class_name, 0) + 1

            # Draw bounding box
            label = f"{class_name} ({conf:.2f})"

            cv2.rectangle(
                img_np,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                img_np,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    detection_results["summary"]["total_defects"] = len(detection_results["detections"])
    detection_results["summary"]["defect_types"] = defect_counts

    return detection_results, img_np