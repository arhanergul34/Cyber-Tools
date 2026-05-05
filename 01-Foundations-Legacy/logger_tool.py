import logging
from datetime import datetime

# STEP 1: Log Configuration (Preparing the Registry)
# This setting determines how the logs will appear.
logging.basicConfig(
    filename='cyber_tool.log',  # File name to save 
    level=logging.INFO,         # Registration level (INFO: Information)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Time - Level - Message
    )

def log_event(message, level="info"):
    """The system prints system events to the screen and also saves them to a file."""

    if level == "info":
        logging.info(message)
        print(f"[*] INFO: {message}")
    elif level == "warning":
        logging.warning(message)
        print(f"[!] WARNING: {message}")
    elif level == "error":
        logging.error(message)
        print(f"[X] ERROR: {message}")
        
# Example usage (Simulation)
if __name__ == "__main__":
    log_event("System scan started")
    log_event("A vulnerability has been detected on Port 80!", "warning")
    log_event("Report file could not be created!", "error")
    log_event("Transaction completed successfully.")
    