from fastapi import FastAPI
from typing import List
import logging

# ------------------------
# App Setup
# ------------------------

app = FastAPI()

logging.basicConfig(level=logging.INFO)

"""
Recommendation API for Japanese products (international users)

Approach:
- Hybrid system combining:
  1. Popularity
  2. User preferences (category match)
  3. Regional assumptions

Goal:
Keep system simple, explainable, and scalable.
"""

# ------------------------
# Mock Data
# ------------------------

users = {
    "A": {"country": "India", "likes": ["snacks", "spicy"]},
    "B": {"country": "USA", "likes": ["tea", "healthy"]},
    "C": {"country": "France", "likes": ["dessert", "premium"]},
}

items = [
    {"id": "1", "name": "Matcha Tea", "category": "tea", "popularity": 0.9},
    {"id": "2", "name": "Pocky", "category": "snacks", "popularity": 0.85},
    {"id": "3", "name": "Instant Ramen", "category": "noodles", "popularity": 0.88},
    {"id": "4", "name": "Sushi Kit", "category": "meal", "popularity": 0.75},
    {"id": "5", "name": "Japanese Candy Box", "category": "snacks", "popularity": 0.8},
]

# ------------------------
# Scoring Logic
# ------------------------

def compute_score(user, item):
    # Preference match
    preference_score = 1 if item["category"] in user["likes"] else 0

    # Regional assumptions
    regional_bonus = 0
    if user["country"] == "India" and item["category"] == "snacks":
        regional_bonus = 0.2
    elif user["country"] == "USA" and item["category"] == "tea":
        regional_bonus = 0.2
    elif user["country"] == "France" and item["category"] == "dessert":
        regional_bonus = 0.2

    # Hybrid score
    score = (
        0.5 * item["popularity"] +
        0.3 * preference_score +
        0.2 * regional_bonus
    )

    return round(score, 3)

# ------------------------
# Recommendation Engine
# ------------------------

def generate_recommendations(user_id: str, limit: int):
    if user_id not in users:
        return None

    user = users[user_id]

    scored_items = []
    for item in items:
        score = compute_score(user, item)
        scored_items.append({
            "item_id": item["id"],
            "name": item["name"],
            "score": score
        })

    ranked = sorted(scored_items, key=lambda x: x["score"], reverse=True)

    return ranked[:limit]

# ------------------------
# API Endpoint
# ------------------------

@app.get("/recommend")
def recommend(user_id: str, limit: int = 3):
    logging.info(f"Generating recommendations for user {user_id}")

    if user_id not in users:
        return {"error": "User not found"}

    if limit <= 0:
        return {"error": "Limit must be positive"}

    limit = min(limit, len(items))

    recommendations = generate_recommendations(user_id, limit)

    return {
        "user_id": user_id,
        "recommendations": recommendations
    }
