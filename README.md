# Object Detection Model Evaluation

This project integrates two key phases of object detection using computer vision models. The goal is to benchmark custom-trained models from Roboflow Universe and use the best model to process a video, generating labeled outputs.

## Project Phases

### Phase 1: Benchmarking Custom-Trained Models
1. **Model Selection**: Search for and select 8 trained models from Roboflow.
2. **Model Evaluation**: Run these models on a video sample to obtain detection results.
3. **Metrics Collection**: Extract metrics from each model, including confidence intervals, detection time, and the number of detected objects.
4. **Comparison and Analysis**: Compare the collected metrics to determine the best model based on performance.
5. **Selection**: Identify and select the best-performing custom-trained model.

### Phase 2: Video Processing with the Best Model
1. **Video Preprocessing**: Use OpenCV to frame the video and save the frames in a database.
2. **Model Loading and Inference**: Load the best model to predict objects in each frame, including labeling and bounding box accuracy.
3. **Video Merging**: Integrate the processed frames with predictions back into a video format as the final output.

## Requirements

- **Development Environment**: VS Code
- **Python Version**: Python 3.10
- **Required Libraries**:
  - `cv2` (OpenCV)
  - `os`
  - `pandas`
  - `inference_sdk`
  - `roboflow supervision opencv-python-headless`
  - `logging`
  - `datetime`
- **Installation**: Follow `requirements.txt` to install dependencies.

## Instructions

### Setup
1. **Clone Repository**: Clone the remote repo from the branch "feature/Jackson_Object_Detection" to your local machine.
2. **Virtual Environment**:
   - Create a virtual environment (`cvproject`) before running the code.
   - In VS Code terminal, use Git to connect the virtual environment, local repo, and remote repo.
   - Set the Python environment to version 3.10 under `cvproject`.
   - Install dependencies using `requirements.txt`.

### Code Execution Order
1. **CommonConst.py**: Store all constants to avoid hard coding and simplify future revisions.
2. **Model_file.py**: Initialize the 8 trained models and the best model.
3. **Detection_util.py**: Run models to compare metrics on a video.
4. **Data_handling.py**: Manually inspect and sort models, perform video inspection, and manipulation.
5. **Db_layer.py**: Save raw frames to the database.
6. **Output_processing.py**: Label results on frames and merge them into a video.
7. **Main.py**: Integrates and runs the complete process with example usages.

### Remote Repository Management
- Regularly commit, pull, and push changes.
- Daily commits for model refinement.
- Commit the database export.

## Output
1. **Processed Videos**: Videos for each model with bounding boxes and labels.
2. **Metrics CSV File**: CSV files containing metrics for each model.
3. **Sample Output**: Video outputs from each model.
4. **Database Export**: SQL schema or files for storing and retrieving video frames.
5. **Final Video Output**: Video processed with the best model, including labeling and timestamps.

## Repo Structure
```
BitBucket/nextgen_recycleanalytics_code/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── src/
│   ├── __init__.py
│   ├── commonconst.py
│   ├── db_Layer.py
│   ├── detection_util.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_handling.py
│   │   └── Trash/
│   │       ├── Trash1.mp4
│   │       ├── Trash2.mp4
│   │       ├── Trash3.mp4
│   │       ├── Trash4.mp4
│   │       ├── Trash5.mp4
│   │       ├── Trash6.mp4
│   ├── models/
│   │   ├── __init__.py
│   │   └── model_file.py
│   ├── output/
│   │   ├── __init__.py
│   │   ├── output_processing.py
│   │   ├── models_outputs/
│   │   │   ├── {model_id}/
│   │   │   │   ├── {model_id}_output_Trash1.mp4
│   │   │   │   ├── {model_id}_output_Trash2.mp4
│   │   │   │   ├── {model_id}_output_Trash3.mp4
│   │   │   │   ├── {model_id}_output_Trash4.mp4
│   │   │   │   ├── {model_id}_output_Trash5.mp4
│   │   │   │   ├── {model_id}_output_Trash6.mp4
│   │   │   ├── ... (continue for other models)
│   │   ├── models_metrics/
│   │   │   ├── {model_id}/
│   │   │   │   ├── {model_id}_output_Trash1.csv
│   │   │   │   ├── {model_id}_output_Trash2.csv
│   │   │   │   ├── {model_id}_output_Trash3.csv
│   │   │   │   ├── {model_id}_output_Trash4.csv
│   │   │   │   ├── {model_id}_output_Trash5.csv
│   │   │   │   ├── {model_id}_output_Trash6.csv
│   │   │   ├── ... (continue for other models)
│   │   ├── process_metrics/
│   │   │   ├── Trash1_summary.csv
│   │   │   ├── Trash2_summary.csv
│   │   │   ├── Trash3_summary.csv
│   │   │   ├── Trash4_summary.csv
│   │   │   ├── Trash5_summary.csv
│   │   │   ├── Trash6_summary.csv
│   │   │   ├── metrics_viz/
│   │   │   │   ├── Total_Frames_Video_1.png
│   │   │   │   ├── Total_Frames_Video_2.png
│   │   │   │   ├── ...
│   │   │   ├── best_model_metrics/
│   │   │   │   ├── best_composite_model.csv
│   │   │   │   ├── best_confidence_model.csv
│   │   │   │   ├── best_detection_model.csv
│   │   │   │   ├── extreme_cases_summary.csv
│   │   │   │   ├── performance_summary.csv
```