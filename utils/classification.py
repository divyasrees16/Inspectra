# utils/classification.py

import numpy as np
from datetime import datetime
from config.settings import CLASS_NAMES
from utils.preprocessing import preprocess_for_effnet


# =====================================
# EfficientNet Classification
# =====================================
def classify_defect_with_json(img_pil, effnet_sess):

    input_tensor = preprocess_for_effnet(img_pil)

    input_name = effnet_sess.get_inputs()[0].name
    output = effnet_sess.run(None, {input_name: input_tensor})[0]

    # Softmax
    probs = np.exp(output) / np.sum(np.exp(output), axis=1, keepdims=True)

    # Top 3 predictions
    top_indices = np.argsort(probs[0])[::-1][:3]

    classification_results = {
        "timestamp": datetime.now().isoformat(),
        "model_info": {
            "type": "EfficientNet",
            "classes": len(CLASS_NAMES)
        },
        "top_predictions": [],
        "all_probabilities": {}
    }

    # Add top 3
    for i, idx in enumerate(top_indices):
        classification_results["top_predictions"].append({
            "rank": i + 1,
            "class_name": CLASS_NAMES[idx],
            "confidence": float(probs[0][idx]),
            "class_id": int(idx)
        })

    # Store all class probabilities
    for i, class_name in enumerate(CLASS_NAMES):
        classification_results["all_probabilities"][class_name] = float(probs[0][i])

    return classification_results