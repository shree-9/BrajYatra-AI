"""
BrajYatra AI — FastAPI Backend

Multi-agent AI travel planner for the Braj region.
Endpoints for itinerary generation, customization, weather, budget, and feedback.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import json

from core.orchestrator import Orchestrator
from agents.explanation_agent import generate_explanation
from agents.budget_agent import estimate_budget
from agents.conversation_agent import generate_response
from agents.weather_agent import fetch_weather
from agents.rl_agent import update_weights, load_weights, reset_weights
from core.memory_store import (
    create_session, get_session, update_session,
    add_feedback, list_sessions
)
from config import LOCATIONS_PATH

# ─── Initialize App ───
app = FastAPI(
    title="BrajYatra AI",
    description="Multi-agent AI travel planner for the Braj region (Mathura, Vrindavan, Agra, Gokul, Barsana, Govardhan).",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ─── Load Orchestrator at startup ───
planner = None


@app.on_event("startup")
def startup():
    global planner
    print("[BrajYatra] Initializing orchestrator...")
    planner = Orchestrator()
    print("[BrajYatra] Ready!")


# ─── Request/Response Models ───

class PlanRequest(BaseModel):
    query: str = Field(..., description="Natural language travel query", min_length=3)
    weather_city: str = Field(default="Mathura", description="City to fetch weather for")


class CustomizeRequest(BaseModel):
    session_id: str = Field(..., description="Session ID from /plan response")
    action: str = Field(..., description="One of: remove, add, swap, reorder")
    day: str = Field(..., description="Day key, e.g., 'Day 1'")
    place: Optional[str] = Field(None, description="Place name (for remove/reorder)")
    place_id: Optional[int] = Field(None, description="Place ID (for add/swap)")
    old_place: Optional[str] = Field(None, description="Place to replace (for swap)")
    new_place_id: Optional[int] = Field(None, description="New place ID (for swap)")
    position: Optional[int] = Field(None, description="Target position (for reorder)")


class FeedbackRequest(BaseModel):
    session_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")


class ChatRequest(BaseModel):
    message: str
    history: list = Field(default_factory=list)


# ─── API Endpoints ───

@app.get("/")
def root():
    return {
        "name": "BrajYatra AI",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "POST /plan",
            "PUT /customize",
            "GET /weather/{city}",
            "POST /budget",
            "POST /feedback",
            "GET /locations",
            "GET /locations/{place_id}",
            "POST /chat"
        ]
    }


@app.post("/plan")
def plan_trip(request: PlanRequest):
    """
    Generate an AI-powered trip itinerary from a natural language query.
    Returns a session_id for further customization.
    """

    if planner is None:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")

    try:
        result = planner.plan_trip(request.query, request.weather_city)

        # Generate explanation
        explanation = generate_explanation(
            request.query,
            result["itinerary"],
            result["intent"]
        )
        result["explanation"] = explanation

        # Estimate budget
        flat_locations = []
        for loc_info in result["locations_used"]:
            loc = planner.get_location_by_id(loc_info["id"])
            if loc:
                flat_locations.append(loc)

        budget = estimate_budget(flat_locations, result["intent"].get("budget", "moderate"))
        result["budget"] = budget

        # Save session
        session_id = create_session(result)
        result["session_id"] = session_id

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planning failed: {str(e)}")


@app.put("/customize")
def customize_itinerary(request: CustomizeRequest):
    """
    Customize an existing itinerary by adding, removing, swapping, or reordering places.
    """

    if planner is None:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")

    session = get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    itinerary = session["data"]["itinerary"]

    # Build params dict for the orchestrator
    params = {
        "day": request.day,
        "place": request.place,
        "place_id": request.place_id,
        "old_place": request.old_place,
        "new_place_id": request.new_place_id,
        "position": request.position
    }

    updated = planner.customize_itinerary(itinerary, request.action, params)

    # Update session
    session["data"]["itinerary"] = updated
    update_session(request.session_id, session["data"])

    # Recalculate budget
    flat_locations = []
    for day_activities in updated.values():
        for act in day_activities:
            loc = planner.get_location_by_id(act.get("place_id"))
            if loc:
                flat_locations.append(loc)

    budget = estimate_budget(flat_locations, session["data"].get("intent", {}).get("budget", "moderate"))

    return {
        "session_id": request.session_id,
        "itinerary": updated,
        "budget": budget,
        "message": f"Successfully applied '{request.action}' to {request.day}"
    }


@app.get("/weather/{city}")
def get_weather(city: str):
    """Fetch current weather for a city in the Braj region."""

    weather = fetch_weather(city)

    if weather is None:
        raise HTTPException(status_code=502, detail=f"Unable to fetch weather for '{city}'")

    return weather


@app.post("/budget")
def get_budget(session_id: str = None, budget_type: str = "moderate"):
    """Get budget estimate for a session's itinerary."""

    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")

    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    flat_locations = []
    itinerary = session["data"].get("itinerary", {})

    for day_activities in itinerary.values():
        for act in day_activities:
            loc = planner.get_location_by_id(act.get("place_id"))
            if loc:
                flat_locations.append(loc)

    return estimate_budget(flat_locations, budget_type)


@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    """Submit feedback rating (1-5) for a session."""

    session = get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Record feedback
    add_feedback(request.session_id, request.rating)

    # Update RL weights
    updated_weights = update_weights(request.rating)

    return {
        "message": "Feedback recorded successfully",
        "rating": request.rating,
        "weights_updated": True
    }


@app.get("/locations")
def get_locations(city: str = None, category: str = None):
    """List all available locations, optionally filtered by city or category."""

    if planner is None:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")

    locations = planner.get_all_locations(city=city, category=category)

    return {
        "count": len(locations),
        "locations": [
            {
                "id": loc["id"],
                "name": loc["name"],
                "category": loc.get("category", ""),
                "city": loc.get("location", {}).get("city", ""),
                "rating": loc.get("ratings", {}).get("overall_rating", 0),
                "is_indoor": loc.get("weather_sensitivity", {}).get("is_indoor", False)
            }
            for loc in locations
        ]
    }


@app.get("/locations/{place_id}")
def get_location_detail(place_id: int):
    """Get full details of a specific location."""

    if planner is None:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")

    loc = planner.get_location_by_id(place_id)
    if not loc:
        raise HTTPException(status_code=404, detail=f"Location ID {place_id} not found")

    return loc


@app.post("/chat")
def chat(request: ChatRequest):
    """Chat with BrajYatra AI assistant."""

    response = generate_response(request.history, request.message)

    return {
        "response": response,
        "history": request.history + [
            {"role": "user", "content": request.message},
            {"role": "assistant", "content": response}
        ]
    }


@app.get("/sessions")
def get_sessions():
    """List all saved sessions."""
    return {"sessions": list_sessions()}


@app.get("/sessions/{session_id}")
def get_session_detail(session_id: str):
    """Get full details of a session."""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


# ─── Run with: python main.py ───
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
