# INSPECTRA

AI-powered industrial surface-defect inspection. INSPECTRA runs a YOLOv8 detector and an EfficientNet classifier (both as ONNX models) behind a Streamlit UI, logs every inspection to **InfluxDB**, and visualises trends on a **Grafana** dashboard. An optional LLM step (Groq) turns the raw detections into a written engineering report.


<img width="1638" height="472" alt="image" src="https://github.com/user-attachments/assets/608954aa-5ab7-4aa2-8025-881ee69f11df" />


## Features

| Mode | What it does | Logged to InfluxDB? |
|---|---|---|
| **Image Upload** | Choose *Detect (YOLO)* for boxes + counts, or *Classify (EfficientNet)* for the top-3 defect types. Optional JSON download and AI report. | YOLO runs only |
| **Real-Time Detection** | Reads an IP-camera stream (phone running "IP Webcam"), runs YOLO on every frame. | Yes, at most once every 2 s, and only when a defect is found |
| **Test Video Detection** | Runs YOLO over an uploaded `.mp4` / `.avi` / `.mov`. | Yes, every frame that contains a defect |

## Project structure

```
Project/
├── app.py                  # Streamlit entry point
├── config/settings.py      # model paths, class names, defect descriptions
├── models/
│   ├── best.onnx           # YOLOv8 detector (9 classes)
│   ├── effnet_gc10.onnx    # EfficientNet classifier (10 classes)
│   └── model_loader.py     # cached ONNX Runtime sessions
├── utils/
│   ├── preprocessing.py    # letterbox + normalisation
│   ├── detection.py        # YOLO inference, box drawing, JSON output
│   ├── classification.py   # EfficientNet inference, top-3 JSON
│   ├── database.py         # InfluxDB writer
│   └── analysis.py         # Groq report (with offline fallback)
├── ui/                     # image_upload.py, realtime.py, test_video.py, theme.py
├── videos/test.mp4         # sample video
├── docker-compose.yml      # InfluxDB + Grafana
└── grafana/                # provisioning + dashboard JSON
```

## Run the app

**Requirements:** Python 3.10+, and optionally a Groq API key (AI reports), a phone with the *IP Webcam* app (live mode), and InfluxDB (logging).

Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

macOS / Linux:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```text
GROQ_API_KEY=your_groq_api_key
```

Start InfluxDB and Grafana first (next section), then:

```bash
streamlit run app.py
```

The app opens at <http://localhost:8501>. The AI report needs a valid `GROQ_API_KEY`; without one it falls back to a short template report.

**Live camera:** install *IP Webcam* on an Android phone, press *Start server*, and put the URL it shows into `PHONE_STREAM_URL` at the top of `ui/realtime.py`, for example `http://192.168.1.20:8080/video`. The phone and PC must be on the same network.

---

## InfluxDB and Grafana setup

> **Use InfluxDB 1.8.x, not 2.x or 3.x.** The app writes with the `influxdb` Python package, which only supports the InfluxDB 1.x API and no authentication. Grafana is the data-source type **InfluxDB with query language InfluxQL**.

| Service | Port | URL | Default login |
|---|---|---|---|
| InfluxDB 1.8 | 8086 | <http://localhost:8086> | none |
| Grafana | 3000 | <http://localhost:3000> | `admin` / `admin` (you are asked to change it) |

### Option A: Docker (recommended)

Needs [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) or Docker Engine + the Compose plugin (Linux).

From the project folder (where `docker-compose.yml` is):

```bash
docker compose up -d
docker compose ps
```

Both containers should show as running. This single command:

- starts InfluxDB 1.8 and **creates the `defects` database** automatically,
- starts Grafana, **registers the InfluxDB data source**, and **loads the "InSpectra - Defect Monitoring" dashboard**.

Open <http://localhost:3000>, sign in with `admin` / `admin`, then go to **Dashboards → Inspectra → InSpectra - Defect Monitoring**.

To set your own Grafana admin password, create (or add to) a `.env` file in the same folder before the first start:

```text
GRAFANA_ADMIN_PASSWORD=choose-a-strong-password
```


### Option B: Native install on Windows

#### 1. InfluxDB 1.8.10

1. Download **`influxdb-1.8.10_windows_amd64.zip`** from <https://dl.influxdata.com/influxdb/releases/influxdb-1.8.10_windows_amd64.zip>. If the link ever changes, go to <https://www.influxdata.com/downloads/> and choose the *1.x* (v1) download.
2. Extract it, for example to `C:\influxdb-1.8.10`.
3. Open a PowerShell window in that folder and start the server. **Leave this window open.**

   ```powershell
   cd C:\influxdb-1.8.10
   .\influxd.exe
   ```

   With no config file, InfluxDB stores its data under `%USERPROFILE%\.influxdb`.
4. Open a **second** PowerShell window, start the CLI and create the database:

   ```powershell
   cd C:\influxdb-1.8.10
   .\influx.exe
   ```

   ```sql
   CREATE DATABASE defects
   SHOW DATABASES
   exit
   ```

   `defects` must appear in the list. The app's writer connects to a database named exactly `defects` and does **not** create it, so this step is required.
5. Quick health check:

   ```powershell
   curl.exe -i http://localhost:8086/ping
   ```

   You should see `HTTP/1.1 204 No Content`.

To keep InfluxDB running in the background across reboots, wrap `influxd.exe` as a Windows service, or simply start it before each session.

#### 2. Grafana

1. Download the **Windows installer** from <https://grafana.com/grafana/download?platform=windows> (Grafana OSS edition) and run it with the defaults.
2. Grafana starts on <http://localhost:3000>. If the page does not load, open `services.msc` and start the *Grafana* service.
3. Sign in with `admin` / `admin` and set a new password when asked.
4. Continue with [Connect Grafana to InfluxDB](#connect-grafana-to-influxdb-manual) and [Import the dashboard](#import-the-dashboard).

### Verify data is flowing

Run a detection in the app first (upload an image, or use the sample video in *Test Video Detection*). Then query InfluxDB.

Docker:

```bash
docker exec -it inspectra-influxdb influx -precision rfc3339 -database defects -execute "SELECT * FROM defect_counts ORDER BY time DESC LIMIT 5"
```

Native Windows (`influx.exe`):

```sql
USE defects
SELECT * FROM defect_counts ORDER BY time DESC LIMIT 5
```

Each row is one inspection event with `total_defects` and one count column per defect type. No rows? See [Troubleshooting](#troubleshooting).

### Connect Grafana to InfluxDB (manual)

Skip this if you used Docker. It is already configured.

1. In Grafana: **Connections → Data sources → Add data source → InfluxDB**.
2. Set:

   | Field | Value |
   |---|---|
   | Query language | **InfluxQL** |
   | URL | `http://localhost:8086` |
   | Database | `defects` |
   | HTTP method | `GET` |
   | User / Password | leave empty |

   If Grafana itself runs in Docker while InfluxDB runs natively on Windows, use `http://host.docker.internal:8086` as the URL.
3. Click **Save & test**. Before the app has written anything, a message about no measurements is normal. Run a detection and test again.

### Import the dashboard

Skip this if you used Docker. It is already loaded.

1. **Dashboards → New → Import → Upload dashboard JSON file**, and pick `grafana/dashboards/inspectra.json`.
2. Click **Import**. The dashboard has a **Data source** dropdown at the top. Select your InfluxDB source if it is not selected already.


## Model notes

- `best.onnx` is a YOLOv8 detector exported with NMS included. It was trained on **9** classes: `crease`, `crescent_gap`, `inclusion`, `oil_spot`, `punching_hole`, `silk_spot`, `waist_folding`, `water_spot`, `welding_line`.
- `effnet_gc10.onnx` is an EfficientNet classifier with **10** classes (the nine above plus `rolled_pit`).
- Inference runs through ONNX Runtime on the CPU (`onnxruntime` in `requirements.txt`). For GPU, install `onnxruntime-gpu` and pass a CUDA execution provider when creating the sessions in `models/model_loader.py`.
- The YOLO export is built with Ultralytics, which is licensed AGPL-3.0. Check that licence before distributing or hosting this project.
