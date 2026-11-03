# utils/analysis.py

import json
import os
from groq import Groq
from config.settings import DEFECT_DESCRIPTIONS


# =====================================
# Groq AI Analysis
# =====================================
def get_groq_analysis(json_data, analysis_type="detection"):

    groq_api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key)

    if analysis_type == "detection":

        prompt = f"""
You are an industrial defect detection and materials analysis expert.

Detection Data:
{json.dumps(json_data, indent=2)}

Defect Descriptions:
{json.dumps(DEFECT_DESCRIPTIONS, indent=2)}

Generate a structured engineering report with:

1. Defects Identified
2. Locations and Sizes
3. Potential Impact on Quality
4. Recommended Actions
5. Conclusion

Professional and technical tone.
"""

    else:

        prompt = f"""
You are an expert in defect classification and industrial quality assurance.

Classification Data:
{json.dumps(json_data, indent=2)}

Defect Descriptions:
{json.dumps(DEFECT_DESCRIPTIONS, indent=2)}

Generate structured analysis including:

1. Top Defects Identified
2. Confidence Analysis
3. Impact on Material Quality
4. Recommended Actions
5. Conclusion
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a senior materials quality expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=1200
        )

        return response.choices[0].message.content

    except Exception as e:
        return generate_fallback_analysis(json_data, analysis_type)


# =====================================
# Fallback Analysis (No API)
# =====================================
def generate_fallback_analysis(json_data, analysis_type):

    if analysis_type == "detection":

        detections = json_data.get("detections", [])

        if not detections:
            return "No defects detected. The material appears free of visible surface defects."

        output = "**Defects Identified:**\n"

        for i, det in enumerate(detections, 1):
            output += f"- {i}. {det['class_name']} ({det['confidence']:.1%})\n"

        output += "\n**Potential Impact on Quality:**\n"
        output += "Detected defects may affect structural integrity and surface finish.\n"

        output += "\n**Recommended Actions:**\n"
        output += "Inspect process parameters and apply corrective measures.\n"

        output += "\n**Conclusion:**\n"
        output += "Implement preventive quality control improvements."

        return output

    else:

        preds = json_data.get("top_predictions", [])

        if not preds:
            return "No classification results available."

        output = "**Top Defects Identified:**\n"

        for i, p in enumerate(preds, 1):
            output += f"- {i}. {p['class_name']} ({p['confidence']:.1%})\n"

        output += "\n**Recommended Actions:**\n"
        output += "Verify production conditions and monitor future batches."

        return output