# src/db_layer.py

from src.commonconst import *
class DummyDB:
    def __init__(self):
        self.data = []

    def save_frame(self, frame_id, frame_data):
        self.data.append((frame_id, frame_data))
        logging.info(f"Frame {frame_id} saved to {dummy_db_name} at {dummy_db_path}")

db = DummyDB()

def save_frames_to_db(input_folder):
    frame_files = sorted(os.listdir(input_folder))
    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(input_folder, frame_file)
        frame = cv2.imread(frame_path)
        _, frame_encoded = cv2.imencode('.jpg', frame)
        frame_data = frame_encoded.tobytes()
        db.save_frame(i, frame_data)
        logging.info(f"Saved frame {i} to {dummy_db_name} from {frame_path}")