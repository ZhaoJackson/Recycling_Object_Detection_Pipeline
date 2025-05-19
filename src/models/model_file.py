# src/models/model_file.py

from src.commonconst import *

def check_model_status(model_id):
    try:
        result = client.infer(default_test_image_url, model_id=model_id)
        if result and "predictions" in result:
            logging.info(f"Model {model_id} loaded successfully.")
            return True
        else:
            logging.error(f"Model {model_id} failed to load.")
            return False
    except Exception as e:
        logging.error(f"An error occurred for model {model_id}: {e}")
        return False