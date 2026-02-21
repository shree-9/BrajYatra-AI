import os

# ─── LLM Configuration ───
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

# ─── API Keys ───
OPENWEATHER_API_KEY = os.environ.get(
    "OPENWEATHER_API_KEY",
    "1095caf889f15b69c0b292d011227db1"
)

GOOGLE_API_KEY = os.environ.get(
    "GOOGLE_API_KEY",
    "AIzaSyBeI4HjFCYGjfMl-Qm7Pa7Ihe7ErHtprgQ"
)

# Set to False to use free Haversine-based distance instead of Google Maps API
USE_GOOGLE_MAPS = False

# ─── Data Paths ───
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
LOCATIONS_PATH = os.path.join(DATA_DIR, "locations_v2.json")
SESSIONS_PATH = os.path.join(DATA_DIR, "sessions.json")
WEIGHTS_PATH = os.path.join(DATA_DIR, "weights.json")

# ─── Default Braj Cities ───
BRAJ_CITIES = ["Mathura", "Vrindavan", "Agra", "Gokul", "Barsana", "Govardhan"]

# ─── Scheduler Settings ───
DAY_START_HOUR = 8   # 08:00 AM
DAY_END_HOUR = 18    # 06:00 PM
MAX_PLACES_PER_DAY = 6