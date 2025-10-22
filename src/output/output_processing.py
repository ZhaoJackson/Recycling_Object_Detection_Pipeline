# src/output/output_processing.py

from src.commonconst import *

def annotate_frames_with_predictions(input_folder, output_folder, model_id=None):
    """
    Annotate frames with predictions from the specified model.
    
    Args:
        input_folder: Folder containing input frames
        output_folder: Folder to save annotated frames
        model_id: Model ID to use for inference (default: best_model)
    """
    if model_id is None:
        model_id = best_model
        
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Created output folder: {output_folder}")

    logging.info(f"Starting inference on frames with model: {model_id}")

    frame_files = sorted(os.listdir(input_folder))
    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(input_folder, frame_file)
        
        # Run inference
        result = client.infer(frame_path, model_id=model_id)

        if result is None:
            logging.error(f"No result returned for frame {frame_file}")
            continue

        # Read frame
        frame = cv2.imread(frame_path)
        
        # Draw predictions
        if 'predictions' in result:
            for pred in result['predictions']:
                x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
                confidence = pred['confidence']
                x, y, w, h = int(x - w / 2), int(y - h / 2), int(w), int(h)
                cv2.rectangle(frame, (x, y), (x + w, y + h), font_color, line_thickness)
                label = f"{pred['class']} ({confidence:.2f})"
                cv2.putText(frame, label, (x, y - 10), default_font, font_scale, font_color, line_thickness)

        # Save annotated frame
        output_frame_path = os.path.join(output_folder, frame_file)
        cv2.imwrite(output_frame_path, frame)
        
        if (i + 1) % 50 == 0:
            logging.info(f"Annotated {i + 1}/{len(frame_files)} frames")
    
    logging.info(f"All frames annotated and saved to {output_folder}")

def merge_frames_to_video(input_folder, output_video_path, fps=None):
    """
    Merge frames from a folder into a video.
    
    Args:
        input_folder: Folder containing frames
        output_video_path: Path to save output video
        fps: Frames per second (default: frame_rate constant)
    """
    if fps is None:
        fps = frame_rate
        
    frame_files = sorted(os.listdir(input_folder))
    
    if not frame_files:
        logging.error(f"No frames found in {input_folder}")
        return
    
    first_frame = cv2.imread(os.path.join(input_folder, frame_files[0]))
    height, width, _ = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*video_format)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    logging.info(f"Merging {len(frame_files)} frames into video")

    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(input_folder, frame_file)
        frame = cv2.imread(frame_path)
        out.write(frame)
        
        if (i + 1) % 100 == 0:
            logging.info(f"Merged {i + 1}/{len(frame_files)} frames")

    out.release()
    logging.info(f"Output video saved at {output_video_path}")
