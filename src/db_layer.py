# src/db_layer.py

from src.commonconst import *

class DummyDB:
    """
    A simple in-memory database for storing frame data.
    In production, this would be replaced with a real database connection.
    """
    def __init__(self):
        self.data = []
        logging.info(f"Initialized {dummy_db_name}")

    def save_frame(self, frame_id, frame_data):
        """
        Save a frame to the database.
        
        Args:
            frame_id: Unique identifier for the frame
            frame_data: Encoded frame data (bytes)
        """
        self.data.append((frame_id, frame_data))
        logging.info(f"Frame {frame_id} saved to {dummy_db_name}")
    
    def get_frame(self, frame_id):
        """
        Retrieve a frame from the database.
        
        Args:
            frame_id: Frame identifier to retrieve
            
        Returns:
            tuple: (frame_id, frame_data) or None if not found
        """
        for fid, fdata in self.data:
            if fid == frame_id:
                logging.info(f"Frame {frame_id} retrieved from {dummy_db_name}")
                return (fid, fdata)
        logging.warning(f"Frame {frame_id} not found in {dummy_db_name}")
        return None
    
    def get_frame_count(self):
        """Get total number of frames in database."""
        return len(self.data)

# Initialize global database instance
db = DummyDB()

def save_frames_to_db(input_folder):
    """
    Save all frames from a folder to the database.
    
    Args:
        input_folder: Folder containing frames to save
    """
    frame_files = sorted(os.listdir(input_folder))
    logging.info(f"Saving {len(frame_files)} frames to {dummy_db_name}")
    
    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(input_folder, frame_file)
        frame = cv2.imread(frame_path)
        
        if frame is None:
            logging.warning(f"Could not read frame: {frame_path}")
            continue
            
        # Encode frame to bytes
        _, frame_encoded = cv2.imencode('.jpg', frame)
        frame_data = frame_encoded.tobytes()
        
        # Save to database
        db.save_frame(i, frame_data)
        
        if (i + 1) % 100 == 0:
            logging.info(f"Saved {i + 1}/{len(frame_files)} frames to database")
    
    logging.info(f"All frames saved. Total in DB: {db.get_frame_count()}")
