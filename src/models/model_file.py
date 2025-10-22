# src/models/model_file.py

from src.commonconst import *

def check_model_status(model_id):
    """
    Check if a model is available and functional by running a test inference.
    
    Args:
        model_id: The Roboflow model ID to check
        
    Returns:
        bool: True if model is functional, False otherwise
    """
    try:
        logging.info(f"Checking model status for: {model_id}")
        result = client.infer(default_test_image_url, model_id=model_id)
        
        if result and "predictions" in result:
            logging.info(f"Model {model_id} loaded successfully.")
            return True
        else:
            logging.error(f"Model {model_id} failed to load - no predictions returned.")
            return False
            
    except Exception as e:
        logging.error(f"An error occurred for model {model_id}: {e}")
        return False

def check_all_models(model_list=None):
    """
    Check status of all models in the list.
    
    Args:
        model_list: List of model IDs (default: model_ids from commonconst)
        
    Returns:
        list: List of valid/functional model IDs
    """
    if model_list is None:
        model_list = model_ids
        
    valid_models = []
    logging.info(f"Checking status of {len(model_list)} models...")
    
    for model_id in model_list:
        if check_model_status(model_id):
            valid_models.append(model_id)
        else:
            logging.warning(f"Model {model_id} failed status check")
    
    logging.info(f"Valid models: {len(valid_models)}/{len(model_list)}")
    return valid_models
