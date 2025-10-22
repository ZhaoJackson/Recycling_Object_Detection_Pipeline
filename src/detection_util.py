# src/detection_util.py

from src.commonconst import *

def infer_on_video_with_metrics(video_path, model_id):
    """
    Run inference on a video using the specified model.
    Saves output video with bounding boxes and metrics CSV.
    """
    video_name = os.path.basename(video_path).split('.')[0]
    
    def get_metrics_file_path(model_id, video_name):
        """Generate path for metrics CSV file"""
        path = os.path.join(metrics_folder, model_id.replace('/', '_'))
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, f"{model_id.replace('/', '_')}_output_{video_name}.csv")
    
    # Setup output directories and paths
    model_output_dir = os.path.join(output_folder, model_id.replace('/', '_'))
    os.makedirs(model_output_dir, exist_ok=True)
    output_video_path = os.path.join(model_output_dir, f"{model_id.replace('/', '_')}_output_{video_name}{output_video_extension}")
    metrics_file_path = get_metrics_file_path(model_id, video_name)

    # Open video capture
    cap = cv2.VideoCapture(video_path)
    input_frame_rate = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*video_format)
    out = cv2.VideoWriter(output_video_path, fourcc, input_frame_rate, (int(cap.get(3)), int(cap.get(4))))

    metrics = []
    frame_count = 0
    
    logging.info(f"Processing video: {video_path} with model: {model_id}")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save frame temporarily for inference
        cv2.imwrite(temp_image_path, frame)
        result = client.infer(temp_image_path, model_id=model_id)

        if result is None:
            logging.warning(f"No result for frame {frame_count}")
            continue

        # Collect metrics
        frame_metrics = {
            'inference_id': result.get('inference_id'),
            'time': result.get('time'),
            'image': result.get('image'),
            'predictions': result.get('predictions')
        }
        metrics.append(frame_metrics)

        # Draw bounding boxes and labels
        labels = [item["class"] for item in result["predictions"]]
        boxes = [{"x": item["x"], "y": item["y"], "width": item["width"], "height": item["height"]} for item in result["predictions"]]

        for bbox, label in zip(boxes, labels):
            x_center, y_center, w, h = bbox["x"], bbox["y"], bbox["width"], bbox["height"]
            x = int(x_center - w / 2)
            y = int(y_center - h / 2)
            w = int(w)
            h = int(h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), font_color, line_thickness)
            cv2.putText(frame, label, (x, y - 10), default_font, font_scale, font_color, line_thickness)

        out.write(frame)
        frame_count += 1
        
        if frame_count % 100 == 0:
            logging.info(f"Processed {frame_count} frames")

    cap.release()
    out.release()

    # Clean up temp file
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

    logging.info(f"Processed video saved as {output_video_path}")
    logging.info(f"Total frames processed: {frame_count}")

    # Save metrics to CSV
    df_metrics = pd.DataFrame(metrics)
    df_metrics.to_csv(metrics_file_path, index=False)
    logging.info(f"Metrics saved to {metrics_file_path}")
