# src/output/output_processing.py

from src.commonconst import *

def annotate_frames_with_predictions(input_folder, output_folder, model_id=best_model):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Created output folder: {output_folder}")

    logging.info("Starting inference on frames")

    frame_files = sorted(os.listdir(input_folder))
    for frame_file in frame_files:
        frame_path = os.path.join(input_folder, frame_file)
        result = client.infer(frame_path, model_id=model_id)

        if result is None:
            logging.error(f"No result returned for frame {frame_file}")
            continue

        frame = cv2.imread(frame_path)
        if 'predictions' in result:
            for pred in result['predictions']:
                x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
                confidence = pred['confidence']
                x, y, w, h = int(x - w / 2), int(y - h / 2), int(w), int(h)
                cv2.rectangle(frame, (x, y), (x + w, y + h), font_color, line_thickness)
                label = f"{pred['class']} ({confidence:.2f})"
                cv2.putText(frame, label, (x, y - 10), default_font, font_scale, font_color, line_thickness)

        output_frame_path = os.path.join(output_folder, frame_file)
        cv2.imwrite(output_frame_path, frame)
        logging.info(f"Annotated {frame_file} with predictions")

def merge_frames_to_video(input_folder, output_video_path):
    frame_files = sorted(os.listdir(input_folder))
    first_frame = cv2.imread(os.path.join(input_folder, frame_files[0]))
    height, width, _ = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*video_format)
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    logging.info("Merging frames into video")

    for frame_file in frame_files:
        frame_path = os.path.join(input_folder, frame_file)
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()
    logging.info(f"Output video saved at {output_video_path}")