import os
import numpy as np

######################## VARIABLES ########################
RANDOM_STATE = int(os.environ.get('RANDOM_STATE'))
DATA_LOCAL_PATH = os.environ.get('DATA_LOCAL_PATH')
MAJOR_RATIO = np.float32(os.environ.get('MAJOR_RATIO'))

PREFECT_FLOW_NAME = os.environ.get("PREFECT_FLOW_NAME")
PREFECT_LOG_LEVEL = os.environ.get("PREFECT_LOG_LEVEL")

GAR_IMAGE = os.environ.get("GAR_IMAGE")
GAR_MEMORY = os.environ.get("GAR_MEMORY")
