# main.py

from src.commonconst import *
# from src.detection_util import infer_on_video_with_metrics
# from src.db_layer import save_frames_to_db
from src.data.data_handling import process_videos
# from src.output.output_processing import annotate_frames_with_predictions, merge_frames_to_video
from src.models.model_file import check_model_status

sys.path.append(folder_path)

def setup_logging():
    logging.basicConfig(level=logging_level, format=logging_format)

def main():
    setup_logging()
    logging.info("Starting the application")
    
    # Define directories
    model_output_dir = 'src/output/models_outputs'
    metrics_dir = 'src/output/process_metrics'
    output_dir = 'src/output/process_metrics/video_metrics'
    
    process_videos(model_output_dir, metrics_dir, output_dir)
    
    
    # video_paths = input_video_path
    
    # valid_models = []
    # for model_id in model_ids:
    #     if check_model_status(model_id):
    #         valid_models.append(model_id)
    #     else:
    #         logging.error(f"Model {model_id} failed to load or is not functional.")
    # if not valid_models:
    #     logging.error("No valid models available. Exiting...")
    #     return

    # try:
    #     # for model_id in valid_models:
    #     #     for video_path in video_paths:
    #     #         logging.info(f"Processing video {video_path} with model {model_id}")
    #     #         infer_on_video_with_metrics(video_path, model_id)
    #     #         logging.info(f"Video processed and metrics saved for model {model_id}")
    #     # process_metrics(metrics_folder)
    #     # logging.info("Metrics processing completed successfully.")
    #     # visualize_summary_metrics(process_metrics_file)
    #     # logging.info("Visualization completed successfully.")
    #     # analyze_model_performance(process_metrics_file)
    #     # logging.info("Analysis completed successfully.")
        
    # except Exception as e:
    #     logging.error(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()



# from src.commonconst import *
# from src.detection_util import infer_on_video_with_metrics
# from src.db_layer import save_frames_to_db
# from src.data.data_handling import process_metrics, read_and_save_frames, add_timestamps_to_frames
# from src.output.output_processing import annotate_frames_with_predictions, merge_frames_to_video
# from src.models.model_file import check_model_status

# sys.path.append(folder_path)

# def setup_logging():
#     logging.basicConfig(level=logging_level, format=logging_format)

# def main():
#     setup_logging()
#     logging.info("Starting the application")
    
#     video_path = input_video_path
#     frames_folder = frame_dir
#     timestamped_frames_folder = timestamped_frames_dir
#     annotated_frames_folder = annotated_frames_dir
#     out_video_path = output_video_path
#     metrics_file = metrics_file_name
#     out_dir = output_dir
#     summary_metrics_name = summary_metrics_file_name

#     valid_models = []
#     for model_id in model_ids:
#         if check_model_status(model_id):
#             valid_models.append(model_id)
#         else:
#             logging.error(f"Model {model_id} failed to load or is not functional.")
#     if not valid_models:
#         logging.error("No valid models available. Exiting...")
#         return

#     try:
#         for model_id in valid_models:
#             logging.info(f"Processing video with model {model_id}")
#             infer_on_video_with_metrics(video_path, model_id)
#             logging.info(f"Video processed and metrics saved for model {model_id}")
#         process_metrics(valid_models, out_dir, metrics_file, summary_metrics_name)
#         logging.info(f"Metrics summary saved at {summary_metrics_name}")
#         read_and_save_frames(video_path, frames_folder)
#         add_timestamps_to_frames(frames_folder, timestamped_frames_folder)
#         annotate_frames_with_predictions(timestamped_frames_folder, annotated_frames_folder, best_model)
#         save_frames_to_db(annotated_frames_folder)
#         merge_frames_to_video(annotated_frames_folder, out_video_path)
#         logging.info(f"Output video saved at {out_video_path}")
#     except Exception as e:
#         logging.error(f"An error occurred during processing: {e}")

# if __name__ == "__main__":
#     main()