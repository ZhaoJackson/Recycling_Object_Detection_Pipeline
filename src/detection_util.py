# src/detection_util.py

from src.commonconst import *

def infer_on_video_with_metrics(video_path, model_id):
    video_name = os.path.basename(video_path).split('.')[0]
    def get_metrics_file_path(model_id, video_name):
        path = os.path.join(metrics_folder, model_id.replace('/', '_'))
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, f"{model_id.replace('/', '_')}_output_{video_name}.csv")
    
    model_output_dir = os.path.join(output_folder, model_id.replace('/', '_'))
    os.makedirs(model_output_dir, exist_ok=True)
    output_video_path = os.path.join(model_output_dir, f"{model_id.replace('/', '_')}_output_{video_name}{output_video_extension}")
    metrics_file_path = get_metrics_file_path(model_id, video_name)

    cap = cv2.VideoCapture(video_path)
    input_frame_rate = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*video_format)
    out = cv2.VideoWriter(output_video_path, fourcc, input_frame_rate, (int(cap.get(3)), int(cap.get(4))))

    metrics = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        temp_image_path = "temp_frame.jpg"
        cv2.imwrite(temp_image_path, frame)
        result = client.infer(temp_image_path, model_id=model_id)

        if result is None:
            continue

        frame_metrics = {
            'inference_id': result.get('inference_id'),
            'time': result.get('time'),
            'image': result.get('image'),
            'predictions': result.get('predictions')
        }
        metrics.append(frame_metrics)

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

    cap.release()
    out.release()

    logging.info(f"Processed video saved as {output_video_path}")
    print(f"Processed video saved as {output_video_path}")

    df_metrics = pd.DataFrame(metrics)
    df_metrics.to_csv(metrics_file_path, index=False)
    logging.info(f"Saving metrics to {metrics_file_path}")