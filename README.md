# Recommendation API for International Users

## Overview

This project implements a simple recommendation API designed to suggest **Japanese products to international users**.

The goal is to build a system that is:

* Simple
* Explainable
* Easily extensible

while reflecting real-world considerations such as user preferences and regional differences.

---

## Approach

I implemented a **hybrid recommendation system** combining three key factors:

### 1. Popularity

Items with higher popularity are more likely to be recommended.

### 2. User Preference Matching

Products are matched against user interests (e.g., snacks, tea).

### 3. Regional Assumptions

Basic assumptions about international preferences are included to simulate real-world behavior
(e.g., snack-based products for certain regions).

---

## Scoring Function

Each item is assigned a score using:

score = 0.5 * popularity + 0.3 * preference_match + 0.2 * regional_bonus

This keeps the system:

* Interpretable
* Easy to debug
* Easy to extend

---

## API Design

### Endpoint

GET /recommend?user_id=A&limit=3

### Example Response

{
"user_id": "A",
"recommendations": [
{
"item_id": "2",
"name": "Pocky",
"score": 0.765
}
]
}

---

## How to Run

pip install -r requirements.txt
uvicorn main:app --reload

Then open:
http://127.0.0.1:8000/docs

---

## Design Choices

* Chose a **rule-based hybrid system** to prioritize clarity over complexity
* Avoided heavy ML models to keep the system explainable
* Focused on international users by incorporating simple regional behavior

---

## Scalability

### Current (Small Scale)

* Real-time scoring for each request

### ~10K Users

* Introduce caching (e.g., Redis)
* Precompute recommendations periodically

### ~1M Users

* Separate candidate generation and ranking
* Use batch pipelines for offline processing
* Use distributed systems for scalability

---

## Performance Improvements

* Caching frequently requested recommendations
* Batching computations for efficiency
* Precomputing recommendations instead of real-time scoring

---

## Assumptions

* User preferences vary by region
* New users may lack interaction data (cold start → popularity fallback)
* Cultural familiarity affects product recommendations

---

## Future Improvements

* Replace rule-based scoring with ML models
* Introduce collaborative filtering
* Use real user interaction data
* Improve personalization using behavioral signals

---

## Advanced Idea

For diverse international users, a **Mixture-of-Experts (MoE)** approach could allow different models to specialize for different regions or user segments, improving personalization at scale.

---

## Conclusion

This project demonstrates a practical approach to building a recommendation API that balances simplicity, clarity, and scalability, while aligning with real-world product needs.
