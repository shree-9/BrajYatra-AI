"""
Session storage using local JSON files (no MongoDB dependency).
Sessions are stored in data/sessions.json.
"""

import json
import os
import uuid
from datetime import datetime
from config import SESSIONS_PATH


def _load_sessions():
    """Load all sessions from disk."""
    if not os.path.exists(SESSIONS_PATH):
        return {}
    try:
        with open(SESSIONS_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_sessions(sessions):
    """Save all sessions to disk."""
    os.makedirs(os.path.dirname(SESSIONS_PATH), exist_ok=True)
    with open(SESSIONS_PATH, "w") as f:
        json.dump(sessions, f, indent=2, default=str)


def create_session(data):
    """Create a new session and return its ID."""
    sessions = _load_sessions()

    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "data": data,
        "feedback": []
    }

    _save_sessions(sessions)
    return session_id


def get_session(session_id):
    """Retrieve a session by ID."""
    sessions = _load_sessions()
    return sessions.get(session_id)


def update_session(session_id, data):
    """Update session data (e.g., after customization)."""
    sessions = _load_sessions()

    if session_id in sessions:
        sessions[session_id]["data"] = data
        sessions[session_id]["updated_at"] = datetime.now().isoformat()
        _save_sessions(sessions)
        return True

    return False


def add_feedback(session_id, rating):
    """Add a feedback rating (1-5) to a session."""
    sessions = _load_sessions()

    if session_id in sessions:
        sessions[session_id]["feedback"].append({
            "rating": rating,
            "timestamp": datetime.now().isoformat()
        })
        _save_sessions(sessions)
        return True

    return False


def list_sessions():
    """List all session IDs with their creation time."""
    sessions = _load_sessions()
    return [
        {
            "session_id": sid,
            "created_at": s.get("created_at", "unknown")
        }
        for sid, s in sessions.items()
    ]
