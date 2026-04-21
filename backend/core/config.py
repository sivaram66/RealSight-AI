import os

# Dynamically locate the RealSight_AI root folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Ensure the assets directory exists
os.makedirs(ASSETS_DIR, exist_ok=True)

class AppState:
    # Set the default video path (Make sure CAM-2.mp4 is inside your assets folder!)
    CURRENT_STREAM_SOURCE = os.path.join(ASSETS_DIR, "CAM-2.mp4")
    CURRENT_SUMMARY = "Initializing behavioral analysis..."

# Create a single state instance to be shared across all files
state = AppState()