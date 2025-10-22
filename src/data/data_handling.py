# src/data/data_handling.py

from src.commonconst import *

def overlay_text_on_frame(frame, text, position=(50, 50), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, color=(0, 0, 255), thickness=1):
    """Overlay text on a single frame with a shadow for better readability."""
    shadow_color = (0, 0, 0)
    shadow_offset = 2
    lines = text.split('\n')
    line_height = int(font_scale * 30)
    x, y = position

    for i, line in enumerate(lines):
        y_line = y + i * line_height
        # Draw shadow
        cv2.putText(frame, line, (x + shadow_offset, y_line + shadow_offset), font, font_scale, shadow_color, thickness, cv2.LINE_AA)
        # Draw text
        cv2.putText(frame, line, (x, y_line), font, font_scale, color, thickness, cv2.LINE_AA)
   
    return frame

def process_video(video_path, metrics_text, output_path):
    """Process a video by overlaying text on each frame and save the result."""
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*video_format), fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = overlay_text_on_frame(frame, metrics_text, position=(10, 30))
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    logging.info(f"Processed video saved to {output_path}")

def get_metrics_for_video(metrics_dir, video_name, model_id):
    """Extract metrics for a specific video and model."""
    video_index = video_name.split('_')[-1].split('.')[0][-1]  # Extracts {i} from video name
    summary_file = os.path.join(metrics_dir, f'Trash{video_index}_summary.csv')
    if os.path.exists(summary_file):
        df = pd.read_csv(summary_file)
        metrics_row = df[df['model_id'] == model_id]
        if not metrics_row.empty:
            metrics_text = (
                f"model_id: {metrics_row['model_id'].values[0]}\n"
                f"total_frames: {metrics_row['total_frames'].values[0]}\n"
                f"num_detections: {metrics_row['num_detections'].values[0]}\n"
                f"avg_confidence: {metrics_row['avg_confidence'].values[0]:.4f}\n"
                f"avg_time: {metrics_row['avg_time'].values[0]:.4f}\n"
                f"detection_percentage: {metrics_row['detection_percentage'].values[0]:.2f}\n"
                f"detected_classes: {metrics_row['detected_classes'].values[0]}"
            )
            return metrics_text
    return None

def process_videos(model_output_dir, metrics_dir, output_dir):
    """Process all videos by overlaying metrics and save the results."""
    logging.info(f"Processing videos from {model_output_dir}")
    
    for model_id in os.listdir(model_output_dir):
        model_dir = os.path.join(model_output_dir, model_id)
        if os.path.isdir(model_dir):
            logging.info(f"Processing model: {model_id}")
            for video_name in os.listdir(model_dir):
                video_path = os.path.join(model_dir, video_name)
                if video_path.endswith('.mp4'):
                    metrics_text = get_metrics_for_video(metrics_dir, video_name, model_id)
                    if metrics_text:
                        output_path = os.path.join(output_dir, model_id, video_name)
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        process_video(video_path, metrics_text, output_path)
                        logging.info(f"Processed {video_name} for {model_id}")
                    else:
                        logging.warning(f"No metrics found for {video_name} and {model_id}")

def read_and_save_frames(video_path, output_folder=None):
    """Extract frames from a video and save them to a folder."""
    if output_folder is None:
        output_folder = frames_folder
        
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Created output folder: {output_folder}")

    logging.info(f"Reading video file: {video_path}")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
        logging.info(f"Saved frame {frame_count} to {frame_path}")

    cap.release()
    logging.info(f"Total frames saved: {frame_count}")

def add_timestamps_to_frames(input_folder, output_folder=None):
    """Add timestamps to frames from input folder and save to output folder."""
    if output_folder is None:
        output_folder = timestamped_frames_folder
        
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Created output folder: {output_folder}")

    logging.info("Adding timestamps to frames")

    frame_files = sorted(os.listdir(input_folder))
    for frame_file in frame_files:
        frame_path = os.path.join(input_folder, frame_file)
        frame = cv2.imread(frame_path)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(frame, timestamp, (10, 30), default_font, font_scale, font_color, line_thickness)
        output_frame_path = os.path.join(output_folder, frame_file)
        cv2.imwrite(output_frame_path, frame)
        logging.info(f"Timestamp added to {frame_file}")
