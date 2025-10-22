# src/commonconst.py

import sys
import os
import logging
import cv2
import pandas as pd
from datetime import datetime
from inference_sdk import InferenceHTTPClient
import matplotlib.pyplot as plt

# Get the project root directory (parent of src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load secrets from .secrets file
def load_secrets():
    """Load API keys and secrets from .secrets file"""
    secrets = {}
    secrets_path = os.path.join(PROJECT_ROOT, '.secrets')
    
    if not os.path.exists(secrets_path):
        logging.error(f"Secrets file not found at {secrets_path}")
        raise FileNotFoundError(f"Please create a .secrets file at {secrets_path}")
    
    with open(secrets_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    secrets[key.strip()] = value.strip()
    
    return secrets

# Load secrets
try:
    SECRETS = load_secrets()
    api_url = SECRETS.get('ROBOFLOW_API_URL', 'https://detect.roboflow.com')
    api_key = SECRETS.get('ROBOFLOW_API_KEY')
    
    if not api_key:
        raise ValueError("ROBOFLOW_API_KEY not found in .secrets file")
        
except Exception as e:
    logging.error(f"Failed to load secrets: {e}")
    raise

# API and Client Configurations
default_test_image_url = "https://source.roboflow.com/xSCf9nSGXWUOYKdRUIAMDNldt7F2/049IL5fBIfegkh83IzH8/original.jpg"

# Initialize the client
client = InferenceHTTPClient(api_url=api_url, api_key=api_key)

# Model Configurations
model_ids = [
    "fyp-rytyv/1",
    "bottles-pcttk/1",
    "recycling-objects-4aqr3/3",
    "trash-recognition-660tk/1",
    "waste-tfpi0/7",
    "rudo_v3/2",
    "recycle-items-detection/3",
    "detection-er/3"
]

best_model = "detection-er/3"

# Inference and Video Processing Settings
video_format = 'mp4v'
frame_rate = 20.0
temp_image_path = "temp_frame.jpg"
output_video_extension = ".mp4"
metrics_file_name = "metrics.csv"
summary_metrics_file_name = "summary_metrics.csv"

# Input paths for videos (relative to project root)
input_video_folder = os.path.join(PROJECT_ROOT, "src/data/Trash")
input_video_path = [os.path.join(input_video_folder, f'Trash{i}.mp4') for i in range(1, 7)]

# Output Paths for videos and metrics (relative to project root)
output_dir = os.path.join(PROJECT_ROOT, "src/output")
output_folder = os.path.join(output_dir, "models_outputs")
metrics_folder = os.path.join(output_dir, "models_metrics")
process_folder = os.path.join(output_dir, "process_metrics")
video_metrics_output_folder = os.path.join(process_folder, "video_metrics")
frames_folder = os.path.join(output_dir, "frames")
timestamped_frames_folder = os.path.join(output_dir, "timestamped_frames")
annotated_frames_folder = os.path.join(output_dir, "annotated_frames")
merged_video_folder = os.path.join(output_dir, "merged_video")
metrics_viz_folder = os.path.join(process_folder, "metrics_viz")
best_model_metrics_folder = os.path.join(process_folder, "best_model_metrics")

# File paths for metrics
process_metrics_file = [os.path.join(process_folder, f'Trash{i}_summary.csv') for i in range(1, 7)]

# Logging Configurations
logging_format = '%(asctime)s:%(levelname)s:%(message)s'
logging_level = logging.INFO

# Video and Image Processing Constants
default_font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.9
font_color = (255, 0, 0)
line_thickness = 2

# Dummy DB Configurations
dummy_db_name = "dummy_db"
dummy_db_path = "dummy_db_path"
