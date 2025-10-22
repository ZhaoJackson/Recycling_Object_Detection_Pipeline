# main.py

from src.commonconst import *
from src.detection_util import infer_on_video_with_metrics
from src.db_layer import save_frames_to_db
from src.data.data_handling import (
    process_videos, 
    read_and_save_frames, 
    add_timestamps_to_frames
)
from src.output.output_processing import (
    annotate_frames_with_predictions, 
    merge_frames_to_video
)
from src.models.model_file import check_model_status, check_all_models

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging_level, 
        format=logging_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def run_model_benchmarking():
    """
    Phase 1: Run all models on all videos to benchmark performance.
    This generates output videos and metrics for each model.
    """
    logging.info("=" * 80)
    logging.info("PHASE 1: MODEL BENCHMARKING")
    logging.info("=" * 80)
    
    # Check which models are functional
    logging.info("Checking model availability...")
    valid_models = check_all_models(model_ids)
    
    if not valid_models:
        logging.error("No valid models available. Exiting...")
        return []
    
    logging.info(f"Found {len(valid_models)} valid models: {valid_models}")
    
    # Run inference on all videos with all valid models
    for model_id in valid_models:
        logging.info(f"\n{'=' * 60}")
        logging.info(f"Processing with model: {model_id}")
        logging.info(f"{'=' * 60}")
        
        for video_path in input_video_path:
            video_name = os.path.basename(video_path)
            logging.info(f"Processing video: {video_name}")
            
            try:
                infer_on_video_with_metrics(video_path, model_id)
                logging.info(f"✓ Successfully processed {video_name} with {model_id}")
            except Exception as e:
                logging.error(f"✗ Error processing {video_name} with {model_id}: {e}")
    
    logging.info("\n" + "=" * 80)
    logging.info("PHASE 1 COMPLETE: All models benchmarked")
    logging.info("=" * 80)
    
    return valid_models

def run_video_processing_with_best_model():
    """
    Phase 2: Process a video with the best model.
    Extract frames → Add timestamps → Annotate → Save to DB → Merge to video
    """
    logging.info("\n" + "=" * 80)
    logging.info("PHASE 2: VIDEO PROCESSING WITH BEST MODEL")
    logging.info("=" * 80)
    
    # Use the first video as example
    sample_video = input_video_path[0]
    logging.info(f"Processing sample video: {os.path.basename(sample_video)}")
    logging.info(f"Using best model: {best_model}")
    
    try:
        # Extract frames
        logging.info("\nStep 1: Extracting frames from video...")
        read_and_save_frames(sample_video, frames_folder)
        
        # Add timestamps
        logging.info("\nStep 2: Adding timestamps to frames...")
        add_timestamps_to_frames(frames_folder, timestamped_frames_folder)
        
        # Annotate frames with predictions
        logging.info("\nStep 3: Running inference and annotating frames...")
        annotate_frames_with_predictions(
            timestamped_frames_folder, 
            annotated_frames_folder, 
            best_model
        )
        
        # Save frames to database
        logging.info("\nStep 4: Saving frames to database...")
        save_frames_to_db(annotated_frames_folder)
        
        # Merge frames back to video
        output_video = os.path.join(merged_video_folder, "output_video.mp4")
        logging.info("\nStep 5: Merging frames to video...")
        merge_frames_to_video(annotated_frames_folder, output_video)
        
        logging.info("\n" + "=" * 80)
        logging.info(f"PHASE 2 COMPLETE: Output video saved at {output_video}")
        logging.info("=" * 80)
        
    except Exception as e:
        logging.error(f"Error in Phase 2: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main application entry point"""
    setup_logging()
    
    logging.info("\n" + "=" * 80)
    logging.info("COMPUTER VISION - TRASH DETECTION PROJECT")
    logging.info("=" * 80)
    logging.info(f"Project root: {PROJECT_ROOT}")
    logging.info(f"Input videos: {len(input_video_path)} files")
    logging.info(f"Models to test: {len(model_ids)}")
    
    # Check if input videos exist
    existing_videos = [v for v in input_video_path if os.path.exists(v)]
    if not existing_videos:
        logging.error("No input videos found in src/data/Trash/")
        logging.error("Please ensure video files (Trash1.mp4 - Trash6.mp4) are present.")
        return
    
    logging.info(f"Found {len(existing_videos)} input videos")
    
    # Ask user what to run
    print("\n" + "=" * 80)
    print("SELECT OPERATION:")
    print("=" * 80)
    print("1. Run Model Benchmarking (Phase 1 - Test all models on all videos)")
    print("2. Run Video Processing (Phase 2 - Process with best model)")
    print("3. Run Both Phases")
    print("4. Quick Test (Run best model on first video only)")
    print("=" * 80)
    
    choice = input("\nEnter your choice (1-4) [default: 4]: ").strip() or "4"
    
    if choice == "1":
        run_model_benchmarking()
        
    elif choice == "2":
        run_video_processing_with_best_model()
        
    elif choice == "3":
        valid_models = run_model_benchmarking()
        if valid_models:
            run_video_processing_with_best_model()
            
    elif choice == "4":
        logging.info("\n" + "=" * 80)
        logging.info("QUICK TEST MODE")
        logging.info("=" * 80)
        logging.info(f"Processing: {os.path.basename(input_video_path[0])}")
        logging.info(f"Using model: {best_model}")
        
        try:
            infer_on_video_with_metrics(input_video_path[0], best_model)
            logging.info("\n✓ Quick test completed successfully!")
            logging.info(f"Output video: {output_folder}/{best_model.replace('/', '_')}/")
            logging.info(f"Metrics CSV: {metrics_folder}/{best_model.replace('/', '_')}/")
        except Exception as e:
            logging.error(f"Error in quick test: {e}")
            import traceback
            traceback.print_exc()
    
    else:
        logging.error(f"Invalid choice: {choice}")
        return
    
    logging.info("\n" + "=" * 80)
    logging.info("APPLICATION COMPLETED")
    logging.info("=" * 80)

if __name__ == "__main__":
    main()
