# src/commonconst.py

import sys
import os
import logging
import cv2
import pandas as pd
from datetime import datetime
from inference_sdk import InferenceHTTPClient
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


# API and Client Configurations
api_url = "https://detect.roboflow.com"
api_key = "fZnjNEsLGs10iAELWBdD"
default_test_image_url = "https://source.roboflow.com/xSCf9nSGXWUOYKdRUIAMDNldt7F2/049IL5fBIfegkh83IzH8/original.jpg"

# Initialize the client
client = InferenceHTTPClient(api_url=api_url, api_key=api_key)

# Model Configurations
# model_ids = [
#     "fyp-rytyv/1",
#     "bottles-pcttk/1",
#     "recycling-objects-4aqr3/3",
#     "trash-recognition-660tk/1",
#     "waste-tfpi0/7",
#     "rudo_v3/2",
#     "recycle-items-detection/3",
#     "detection-er/3"
# ]

best_model = "detection-er/3"

# Inference and Video Processing Settings
video_format = 'mp4v'
frame_rate = 20.0
# temp_image_path = "BitBucket/nextgen_recycleanalytics_code/src/output/temp_frame.jpg"
# output_video_extension = ".mp4"
# metrics_file_name = "metrics.csv"
# summary_metrics_file_name = "summary_metrics.csv"

# Input paths for videos
folder_path = "/Users/jacksonzhao/Desktop/BitBucket/nextgen_recycleanalytics_code/src"
input_video_folder = os.path.join(folder_path, "data/Trash")
input_video_path = [os.path.join(input_video_folder, f'Trash{i}.mp4') for i in range(1, 7)]

# Output Paths for videos and metrics
output_dir = os.path.join(folder_path, "output")
output_folder = os.path.join(output_dir, "models_outputs")
# metrics_folder = os.path.join(output_dir, "models_metrics")
# process_folder = os.path.join(output_dir, "process_metrics")
# video_metrics_output_folder = os.path.join(process_folder, "video_metrics")
frames_folder = os.path.join(output_dir, "frames")
timestamped_frames_folder = os.path.join(output_dir, "timestamp")
annotated_frames_folder = os.path.join(output_dir, "annotated_frames")
merged_video_folder = os.path.join(output_dir, "merged_video")

# metrics_file = [os.path.join(metrics_folder, model_id.split('/')[0], f'{model_id.split("/")[1]}_metrics.csv') for model_id in model_ids]
# process_metrics_file = [os.path.join(process_folder, f'Trash{i}_summary.csv') for i in range(1, 7)]

# frame_dir = "src/output/frames"
# timestamped_frames_dir = "src/output/timestamped_frames"
# annotated_frames_dir = "src/output/annotated_frames"

# Output Files
# video_file = [os.path.join(output_folder, model_id.split('/')[0], f'{model_id.split("/")[1]}_output_video.mp4') for model_id in model_ids]
# metrics_file = [os.path.join(metrics_folder, model_id.split('/')[0], f'{model_id.split("/")[1]}_metrics.csv') for model_id in model_ids]
# process_metrics_file = [os.path.join(process_folder, f'Trash{i}_summary.csv') for i in range (1, 7)]
# metrics_viz_folder = os.path.join(process_folder, "metrics_viz")
# best_model_metrics_folder = os.path.join(process_folder, "best_model_metrics")

# Logging Configurations
logging_format = '%(asctime)s:%(levelname)s:%(message)s'
logging_level = 'INFO'

# Video and Image Processing Constants
default_font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.9
font_color = (255, 0, 0)
line_thickness = 2

# Dummy DB Configurations
dummy_db_name = "dummy_db"
dummy_db_path = "dummy_db_path"



# # src/commonconst.py
# import sys
# import os
# import logging
# import cv2
# import pandas as pd
# from datetime import datetime
# from inference_sdk import InferenceHTTPClient

# # API and Client Configurations
# api_url = "https://detect.roboflow.com"
# api_key = "fZnjNEsLGs10iAELWBdD"
# default_test_image_url = "https://source.roboflow.com/xSCf9nSGXWUOYKdRUIAMDNldt7F2/049IL5fBIfegkh83IzH8/original.jpg"

# # Initialize the client
# client = InferenceHTTPClient(api_url=api_url, api_key=api_key)

# # Model Configurations
# model_ids = [
#     "fyp-rytyv/1",
#     "bottles-pcttk/1",
#     "recycling-objects-4aqr3/3",
#     "trash-recognition-660tk/1",
#     "waste-tfpi0/7",
#     "rudo_v3/2",
#     "recycle-items-detection/3",
#     "detection-er/3"
# ]

# best_model = "bottles-pcttk/1"

# # Inference and Video Processing Settings
# video_format = 'mp4v'
# frame_rate = 20.0
# temp_image_path = "src/output/temp_frame.jpg"
# output_video_extension = ".mp4"
# metrics_file_name = "metrics.csv"

# # Input paths
# folder_path = "BitBucket/nextgen_recycleanalytics_code/src"
# input_video_path = "src/data/Trash.mp4"

# # Output Paths
# output_dir = "src/output"
# frame_dir = "src/output/frames"
# timestamped_frames_dir = "src/output/timestamped_frames"
# annotated_frames_dir = "src/output/annotated_frames"
# output_video_path = "src/output/output_video.mp4"
# summary_metrics_file_name = "src/output/metrics_summary.csv"

# # Logging Configurations
# logging_format = '%(asctime)s:%(levelname)s:%(message)s'
# logging_level = 'INFO'

# # Video and Image Processing Constants
# default_font = cv2.FONT_HERSHEY_SIMPLEX
# font_scale = 0.9
# font_color = (255, 0, 0)
# line_thickness = 2

# # Dummy DB Configurations
# dummy_db_name = "dummy_db"
# dummy_db_path = "dummy_db_path"