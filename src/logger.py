# logger.py
# --------------------------------------------------------
# Logging means recording messages about what your program
# is doing while it runs — to monitor, debug, and understand
# how your code behaves.

import logging
import os
from datetime import datetime

# ✅ Always point to the project root (two levels up from src)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ Create "logs" folder inside the project root
LOG_DIR = os.path.join(ROOT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# ✅ Create a timestamp-based log file name
LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# ✅ Configure logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] [%(levelname)s] %(name)s - Line %(lineno)d: %(message)s",
    level=logging.INFO,
)

# ✅ Create a logger instance
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("✅ Logging has started successfully.")
