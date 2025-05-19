# src/data/data_handling.py

from src.commonconst import *

# def process_metrics(metrics_folder):
#     def get_metrics_file_path(model_id, video_index):
#         return os.path.join(metrics_folder, model_id, f'{model_id}_output_Trash{video_index}.csv')

#     all_metrics_by_video = {i: [] for i in range(1, 7)}
#     model_ids = [folder for folder in os.listdir(metrics_folder) if os.path.isdir(os.path.join(metrics_folder, folder))]
    
#     for model_id in model_ids:
#         for i in range(1, 7):
#             metrics_file_path = get_metrics_file_path(model_id, i)
#             logging.info(f"Constructed metrics file path: {metrics_file_path}")
            
#             if os.path.exists(metrics_file_path):
#                 logging.info(f"Reading metrics from {metrics_file_path}")
#                 df_metrics = pd.read_csv(metrics_file_path)
#                 df_metrics['model_id'] = model_id
#                 all_metrics_by_video[i].append(df_metrics)
#             else:
#                 logging.warning(f"No metrics found for model {model_id} at path {metrics_file_path}")

#     for video_index, metrics_list in all_metrics_by_video.items():
#         if not metrics_list:
#             logging.warning(f"No metrics to process for video {video_index}.")
#             continue

#         combined_metrics = pd.concat(metrics_list, ignore_index=True)
    
#         def safe_eval(x):
#             try:
#                 return eval(x)
#             except (SyntaxError, NameError):
#                 return None

#         combined_metrics['predictions'] = combined_metrics['predictions'].apply(lambda x: safe_eval(x) if isinstance(x, str) else x)
#         combined_metrics['predictions'] = combined_metrics['predictions'].apply(lambda preds: [(pred['class'], pred['confidence']) for pred in preds] if preds else [('none', 0)])
#         exploded_metrics = combined_metrics.explode('predictions')
#         exploded_metrics[['class', 'confidence']] = pd.DataFrame(exploded_metrics['predictions'].tolist(), index=exploded_metrics.index)
#         exploded_metrics.drop(columns=['predictions'], inplace=True)

#         summary = exploded_metrics.groupby('model_id').agg(
#             total_frames=('model_id', 'size'),
#             num_detections=('class', lambda x: (x != 'none').sum()),
#             avg_confidence=('confidence', 'mean'),
#             avg_time=('time', 'mean')
#         )
#         summary['detection_percentage'] = (summary['num_detections'] / summary['total_frames']) * 100
#         summary['detected_classes'] = exploded_metrics[exploded_metrics['class'] != 'none'].groupby('model_id')['class'].apply(lambda x: ', '.join(x.unique()))
        
#         summary_metrics_file_path = process_metrics_file[video_index-1]
#         logging.info(f"Saving summary metrics for video {video_index} to {summary_metrics_file_path}")
#         summary.to_csv(summary_metrics_file_path)
#         logging.info(f"Metrics summary saved as {summary_metrics_file_path}")

# def visualize_summary_metrics(process_metrics_file):
#     # Create the metrics_viz directory if it doesn't exist
#     if not os.path.exists(metrics_viz_folder):
#         os.makedirs(metrics_viz_folder)

#     for i in range(1, 7):
#         file_path = process_metrics_file[i-1]
#         if os.path.exists(file_path):
#             df = pd.read_csv(file_path)
#             model_ids = df['model_id'].unique()

#             # Plotting total frames per model
#             plt.figure(figsize=(10, 6))
#             df.plot(kind='bar', x='model_id', y='total_frames', legend=False)
#             plt.title(f'Total Frames for Video {i}')
#             plt.xlabel('Model ID')
#             plt.ylabel('Total Frames')
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.savefig(os.path.join(metrics_viz_folder, f'Total_Frames_Video_{i}.png'))
#             plt.close()

#             # Plotting detection percentage per model
#             plt.figure(figsize=(10, 6))
#             df.plot(kind='bar', x='model_id', y='detection_percentage', legend=False, color='orange')
#             plt.title(f'Detection Percentage for Video {i}')
#             plt.xlabel('Model ID')
#             plt.ylabel('Detection Percentage')
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.savefig(os.path.join(metrics_viz_folder, f'Detection_Percentage_Video_{i}.png'))
#             plt.close()

#             # Plotting average confidence per model
#             plt.figure(figsize=(10, 6))
#             df.plot(kind='bar', x='model_id', y='avg_confidence', legend=False, color='green')
#             plt.title(f'Average Confidence for Video {i}')
#             plt.xlabel('Model ID')
#             plt.ylabel('Average Confidence')
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.savefig(os.path.join(metrics_viz_folder, f'Avg_Confidence_Video_{i}.png'))
#             plt.close()

#             # Plotting average time per model
#             plt.figure(figsize=(10, 6))
#             df.plot(kind='bar', x='model_id', y='avg_time', legend=False, color='red')
#             plt.title(f'Average Time for Video {i}')
#             plt.xlabel('Model ID')
#             plt.ylabel('Average Time')
#             plt.xticks(rotation=45)
#             plt.tight_layout()
#             plt.savefig(os.path.join(metrics_viz_folder, f'Avg_Time_Video_{i}.png'))
#             plt.close()

#             print(f'Visualizations for Video {i} saved.')
#         else:
#             print(f'File {file_path} does not exist.')

# def analyze_model_performance(process_metrics_file):
#     all_data = []
#     for file_path in process_metrics_file:
#         if os.path.exists(file_path):
#             df = pd.read_csv(file_path)
#             all_data.append(df)
#         else:
#             print(f'File {file_path} does not exist.')

#     if not all_data:
#         print("No data available for analysis.")
#         return

#     combined_df = pd.concat(all_data, ignore_index=True)
#     performance_summary = combined_df.groupby('model_id').agg({
#         'total_frames': ['mean', 'std'],
#         'detection_percentage': ['mean', 'std'],
#         'avg_confidence': ['mean', 'std'],
#         'avg_time': ['mean', 'std']
#     }).reset_index()

#     performance_summary.columns = ['_'.join(col).strip() for col in performance_summary.columns.values]
#     performance_summary.rename(columns={'model_id_': 'model_id'}, inplace=True)
#     best_detection_model = performance_summary.sort_values(by='detection_percentage_mean', ascending=False).iloc[0]
#     best_confidence_model = performance_summary.sort_values(by='avg_confidence_mean', ascending=False).iloc[0]

#     print("Performance Summary:")
#     print(performance_summary)
#     print("\nBest Model based on Detection Percentage:")
#     print(best_detection_model)
#     print("\nBest Model based on Average Confidence:")
#     print(best_confidence_model)
    
#     extreme_cases = combined_df[(combined_df['detection_percentage'] < 10) | (combined_df['detection_percentage'] > 90)]
#     extreme_cases_summary = extreme_cases.groupby('model_id').agg({
#         'total_frames': ['mean', 'std'],
#         'detection_percentage': ['mean', 'std'],
#         'avg_confidence': ['mean', 'std'],
#         'avg_time': ['mean', 'std']
#     }).reset_index()

#     extreme_cases_summary.columns = ['_'.join(col).strip() for col in extreme_cases_summary.columns.values]
#     extreme_cases_summary.rename(columns={'model_id_': 'model_id'}, inplace=True)

#     print("\nExtreme Cases Summary:")
#     print(extreme_cases_summary)

#     if not os.path.exists(best_model_metrics_folder):
#         os.makedirs(best_model_metrics_folder)

#     performance_summary.to_csv(os.path.join(best_model_metrics_folder, 'performance_summary.csv'), index=False)
#     best_detection_model.to_frame().T.to_csv(os.path.join(best_model_metrics_folder, 'best_detection_model.csv'), index=False)
#     best_confidence_model.to_frame().T.to_csv(os.path.join(best_model_metrics_folder, 'best_confidence_model.csv'), index=False)
#     extreme_cases_summary.to_csv(os.path.join(best_model_metrics_folder, 'extreme_cases_summary.csv'), index=False)

#     performance_summary['composite_score'] = (performance_summary['detection_percentage_mean'] + performance_summary['avg_confidence_mean']) / 2
#     best_composite_model = performance_summary.sort_values(by='composite_score', ascending=False).iloc[0]

#     print("\nBest Model based on Composite Score:")
#     print(best_composite_model)

#     best_composite_model.to_frame().T.to_csv(os.path.join(best_model_metrics_folder, 'best_composite_model.csv'), index=False)

#     return performance_summary, best_detection_model, best_confidence_model, extreme_cases_summary


# def overlay_text_on_frame(frame, text, position=(50, 50), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, color=(0, 0, 255), thickness=1):
#     """Overlay text on a single frame with a shadow for better readability."""
#     shadow_color = (0, 0, 0)
#     shadow_offset = 2
#     lines = text.split('\n')
#     line_height = int(font_scale * 30)
#     x, y = position

#     for i, line in enumerate(lines):
#         y_line = y + i * line_height
#         # Draw shadow
#         cv2.putText(frame, line, (x + shadow_offset, y_line + shadow_offset), font, font_scale, shadow_color, thickness, cv2.LINE_AA)
#         # Draw text
#         cv2.putText(frame, line, (x, y_line), font, font_scale, color, thickness, cv2.LINE_AA)
    
#     return frame

# def process_video(video_path, metrics_text, output_path):
#     """Process a video by overlaying text on each frame and save the result."""
#     cap = cv2.VideoCapture(video_path)
#     frame_width = int(cap.get(3))
#     frame_height = int(cap.get(4))
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*video_format), fps, (frame_width, frame_height))

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if ret:
#             frame = overlay_text_on_frame(frame, metrics_text, position=(10, 30))
#             out.write(frame)
#         else:
#             break

#     cap.release()
#     out.release()

# def get_metrics_for_video(metrics_dir, video_name, model_id):
#     """Extract metrics for a specific video and model."""
#     video_index = video_name.split('_')[-1].split('.')[0][-1]  # Extracts {i} from video name
#     summary_file = os.path.join(metrics_dir, f'Trash{video_index}_summary.csv')
#     if os.path.exists(summary_file):
#         df = pd.read_csv(summary_file)
#         metrics_row = df[df['model_id'] == model_id]
#         if not metrics_row.empty:
#             metrics_text = (
#                 f"model_id: {metrics_row['model_id'].values[0]}\n"
#                 f"total_frames: {metrics_row['total_frames'].values[0]}\n"
#                 f"num_detections: {metrics_row['num_detections'].values[0]}\n"
#                 f"avg_confidence: {metrics_row['avg_confidence'].values[0]}\n"
#                 f"avg_time: {metrics_row['avg_time'].values[0]}\n"
#                 f"detection_percentage: {metrics_row['detection_percentage'].values[0]}\n"
#                 f"detected_classes: {metrics_row['detected_classes'].values[0]}"
#             )
#             return metrics_text
#     return None

# def process_videos(model_output_dir, metrics_dir, output_dir):
#     """Process all videos by overlaying metrics and save the results."""
#     for model_id in os.listdir(model_output_dir):
#         model_dir = os.path.join(model_output_dir, model_id)
#         if os.path.isdir(model_dir):
#             for video_name in os.listdir(model_dir):
#                 video_path = os.path.join(model_dir, video_name)
#                 if video_path.endswith('.mp4'):
#                     metrics_text = get_metrics_for_video(metrics_dir, video_name, model_id)
#                     if metrics_text:
#                         output_path = os.path.join(output_dir, model_id, video_name)
#                         os.makedirs(os.path.dirname(output_path), exist_ok=True)
#                         process_video(video_path, metrics_text, output_path)



def read_and_save_frames(video_path, output_folder=frame_dir):
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

def add_timestamps_to_frames(input_folder, output_folder=timestamped_frames_dir):
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
        
