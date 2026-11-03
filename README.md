# INSPECTRA

INSPECTRA is a Streamlit application for AI-powered industrial surface-defect detection. It supports image upload, real-time camera detection, and analysis of uploaded video using ONNX models.

The ONNX model files (`best.onnx` and `effnet_gc10.onnx`) are stored in `models/`.

## Requirements

- Python 3.10 or newer
- A Groq API key for AI-generated analysis
- A webcam for real-time detection
- InfluxDB at `localhost:8086` if you want to store detection results


## Run locally 

From the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key
```

Then start the app:

```powershell
streamlit run app.py
```

The application opens in your browser. The AI analysis feature requires a valid `GROQ_API_KEY`. Detection-result storage requires a local InfluxDB instance; the app connects to the `defects` database on `localhost:8086`.
