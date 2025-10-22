# Computer Vision: Object Detection Benchmark & Video Processing

A step‑by‑step guide to set up, run, and extend the project that benchmarks multiple Roboflow models on trash/recycling videos and processes videos with the best model.

---

## ✨ What this project does (at a glance)

**Phase 1 — Benchmark models**
- Run 8 pre‑configured Roboflow models on sample videos
- Collect per‑model metrics (confidence, detections, runtime)
- Compare and automatically identify the best model

**Phase 2 — Process videos with the best model**
- Extract frames → add timestamps → run inference → annotate → (dummy) DB save → merge back to video
- Produce final labeled videos + CSV metrics + summary visualizations

> All paths are relative to the project root and API keys are read from a `.secrets` file ignored by git.

---

## 🧱 Repo structure

```
computer_vision/
├── .secrets              # API keys
├── .gitignore            # Updated to ignore secrets and cache files
├── main.py               # Main entry point (menu-driven)
├── requirements.txt      # Python dependencies
├── src/
│   ├── commonconst.py    # All constants, path config, secrets loading, Roboflow client init
│   ├── db_layer.py       # Dummy DB storing frames
│   ├── detection_util.py # Video inference utilities
│   ├── data/
│   │   ├── data_handling.py  # Video processing & metrics helpers
│   │   └── Trash/            # Input videos (ignored by git)
│   ├── models/
│   │   └── model_file.py     # Model validation helpers
│   └── output/
│       ├── output_processing.py  # Frame annotation & video merge
│       ├── models_outputs/       # Per-model output videos
│       ├── models_metrics/       # Raw metrics CSVs
│       └── process_metrics/      # Processed metrics & visualizations
```
> Notes
> - Input videos live in `src/data/Trash/` (ignored by git).
> - Output folders are created automatically.
> - Comprehensive logging helps you follow progress.

---

## 🧰 Requirements

- **Python** 3.10 recommended
- **Editor**: VS Code (recommended)
- **Roboflow API Key** in a `.secrets` file (see below)

### `.secrets` (required)
Create a file named `.secrets` at the project root:
```
ROBOFLOW_API_KEY=your_api_key_here
ROBOFLOW_API_URL=https://detect.roboflow.com
```
> Keep it private — it’s git‑ignored by default.

---

## 🚀 Quick Start (2–5 minutes)

1) **Activate your env** (example uses conda):
```
conda activate ollama_env
```

2) **Go to the project folder**:
```
cd /Users/jacksonzhao/Desktop/computer_vision
```

3) **Install deps** (choose one):
- **Fastest (essentials only)**
  ```bash
  pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org inference-sdk moviepy
  ```
- **All packages from `requirements.txt`**
  ```bash
  pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
  ```

4) **Run a quick test** (recommended first run):
```
python main.py
```
Select **Option 4 – Quick Test**. It runs the best model on the smallest sample video and produces a labeled video + metrics in minutes.

---

## 🔧 Full Setup (alternative paths)

### Option A — Use existing conda env
```bash
conda activate ollama_env
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org inference-sdk moviepy
# opencv-python, pandas, matplotlib are often preinstalled in this env
```

### Option B — Fresh virtualenv (recommended for clean installs)
```bash
python -m venv cvproject
# macOS/Linux
source cvproject/bin/activate
# Windows (PowerShell)
# .\cvproject\Scripts\Activate.ps1

pip install -r requirements.txt
```

### Option C — Fresh conda env
```bash
conda create -n cvproject python=3.10
conda activate cvproject
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org inference-sdk opencv-python pandas matplotlib moviepy
```

> **SSL gotchas?** Re‑run with `--trusted-host` flags (shown above) or run your system’s “Install Certificates” script (macOS Python installs often include it).

---

## ✅ Sanity check

Verify imports work:
```bash
python -c "from src.commonconst import *; print('✓ All imports successful')"
```

Make sure input videos exist:
```
ls src/data/Trash/
# Expect: Trash1.mp4 ... Trash6.mp4 (example set)
```

Ensure `.secrets` exists and includes a valid key.

---

## ▶️ How to run

From the project root:

```bash
conda activate ollama_env  # or activate your venv
python main.py
```

You’ll see a menu — pick one:

### Option 1 — **Model Benchmarking (Phase 1)**
- Runs **all 8 models** on **all videos**
- Produces **output videos** with boxes/labels
- Writes **per‑model/per‑video CSV metrics**
- **Time‑consuming** (inference per frame via API)
- Outputs:
  - Videos → `src/output/models_outputs/{model_id}/`
  - Metrics → `src/output/models_metrics/{model_id}/`

### Option 2 — **Video Processing (Phase 2)**
- Full pipeline on the **first video** using the **best model**
- Steps: extract frames → timestamps → inference → annotate → dummy DB → merge video
- Outputs:
  - Frames → `src/output/frames/`
  - Annotated frames → `src/output/annotated_frames/`
  - Merged video → `src/output/merged_video/`

### Option 3 — **Both Phases**
- Benchmarks all models, then runs the full pipeline with the best model
- Most comprehensive; **longest runtime**

### Option 4 — **Quick Test (Recommended)**
- Best model on the smallest sample video
- End‑to‑end validation in **~2–5 minutes**

---

## 🧪 Models configured (example set)

1. `fyp-rytyv/1`
2. `bottles-pcttk/1`
3. `recycling-objects-4aqr3/3`
4. `trash-recognition-660tk/1`
5. `waste-tfpi0/7`
6. `rudo_v3/2`
7. `recycle-items-detection/3`
8. `detection-er/3`  ← **current best**

> The best model can be changed centrally in `src/commonconst.py` (see “Configuration”).

---

## 🔩 Configuration (centralized in `src/commonconst.py`)

- Load secrets from `.secrets`
- Define model IDs to test + designating the “best” model
- Set input/output relative paths
- Configure video processing parameters
- Configure logging

> Adjust once here; the whole pipeline will follow.

---

## 📂 Outputs & artifacts

- **Per‑model output videos**: `src/output/models_outputs/{model_id}/`
- **Per‑model metrics CSVs**: `src/output/models_metrics/{model_id}/`
- **Processed metrics & visualizations**: `src/output/process_metrics/`
- **Frames**: `src/output/frames/`
- **Annotated frames**: `src/output/annotated_frames/`
- **Merged video**: `src/output/merged_video/`

---

## 🛠️ Troubleshooting

1) **Wrong env** → Activate the correct one:
```
conda activate ollama_env  # or your venv
```

2) **Missing key** → Ensure `.secrets` exists with a valid `ROBOFLOW_API_KEY`.

3) **Input videos not found** → Put videos into `src/data/Trash/`.

4) **SSL/installation errors**
- Use `--trusted-host` flags shown above
- Try: `pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org inference-sdk`
- On macOS, run your Python’s “Install Certificates.command”

5) **Import errors after install** → Restart your shell or IDE kernel.

6) **Network/API errors** → Check internet connectivity and API quota.

---

## 🧪 Developer tips

- Keep committing/pushing regularly while refining models
- Track metrics over time (CSV in `src/output/models_metrics/`)
- Centralize constants in `src/commonconst.py` to avoid hardcoding
- Use Option 4 often during development to validate changes quickly

---

## 🗺️ End‑to‑End Workflow (recap)

1. **Validate models** (quick) → `models/model_file.py`
2. **Benchmark models** (Phase 1) → videos + CSV metrics
3. **Select best model** (config) → `commonconst.py`
4. **Full pipeline** (Phase 2) → frames → annotate → DB → merge
5. **Review outputs** in `src/output/…`

---

**Enjoy your trash detection system!** 🗑️📹🤖
