# Recommendation API for International Users

## Overview

This project implements a recommendation API designed to suggest **Japanese products to international users**.

The objective is to build a system that is:

* Simple
* Explainable
* Scalable
* Easily extensible

while reflecting real-world considerations such as user preferences, regional differences, and system performance constraints.

---

## Approach

I implemented a **hybrid recommendation system** combining three core signals:

### 1. Popularity

A global baseline signal ensuring that widely liked products are always considered.

### 2. User Preference Matching

Products are matched against user interests (e.g., snacks, tea), allowing basic personalization.

### 3. Regional Assumptions

Simple heuristics are used to simulate differences in international markets (e.g., snack-heavy preferences in certain regions).

---

## Why a Rule-Based System (Instead of ML)

I intentionally chose a rule-based approach for this implementation.

### Reasons:

* The system uses **synthetic data**, so training a machine learning model would not produce meaningful results
* A rule-based system is **fully interpretable**, making it easier to understand and debug
* It provides a strong **baseline system**, which is how real-world recommendation systems are often developed initially

In a production setting, this system would naturally evolve into an ML-based pipeline once sufficient user interaction data is available.

---

## Scoring Function

Each item is scored using:

score = 0.5 * popularity + 0.3 * preference_match + 0.2 * regional_bonus

This weighted combination ensures:

* Stability (via popularity)
* Personalization (via preferences)
* Context awareness (via regional signals)

The design prioritizes **clarity and extensibility**, allowing easy replacement or augmentation with ML models later.

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

* pip install -r requirements.txt
* uvicorn main:app --reload in cmd

Then open:
http://127.0.0.1:8000/docs

---

## Design Choices

* Prioritized **simplicity and clarity** over premature optimization
* Used a **hybrid scoring approach** to simulate real-world recommendation logic
* Designed the system to be easily extensible toward ML-based approaches
* Focused on **international users**, incorporating regional behavior assumptions

---

## Scalability

### Current (Small Scale)

* Recommendations are computed in real-time per request
* Suitable for low traffic and prototyping

---

### ~10K Users

At this stage, repeated computation becomes inefficient.

Improvements:

* Introduce **caching (e.g., Redis)** to store recommendations for frequently active users
* Use **precomputation** to generate recommendations periodically (e.g., every few hours)
* Reduce latency by serving cached results instead of recomputing

---

### ~1M Users

At larger scale, system architecture needs to change:

* Separate into:

  * **Candidate Generation** (retrieve a subset of relevant items)
  * **Ranking** (score and sort candidates)

* Use **offline batch pipelines** to compute recommendations for large user sets

* Store results in databases or caches for fast retrieval

* Introduce distributed systems for handling large-scale traffic

---

## Performance Improvements

### Caching

* Store recommendations per user to avoid recomputation
* Reduces latency and improves throughput

### Batching

* Instead of scoring items individually per request, process multiple items or users together
* Especially useful when integrating ML models (vectorized computation)
* Improves efficiency and resource utilization

### Precomputation

* Generate recommendations offline at regular intervals
* Allows real-time API to remain lightweight

---

## Assumptions

* User preferences vary significantly across regions
* New users may not have interaction history (cold start → popularity fallback)
* Cultural familiarity affects product engagement
* Product demand patterns differ across international markets

---

## Future Improvements (ML Integration)

Once real interaction data is available, the system can evolve into:

* **Collaborative filtering** (user-user or item-item similarity)
* **Learning-to-rank models** for optimized scoring
* **Behavioral feature engineering** (clicks, purchases, dwell time)

The current scoring function can serve as a **baseline model** for these approaches.

---

## Advanced Idea: Mixture-of-Experts (MoE)

For large-scale international systems, user behavior becomes highly heterogeneous.

A **Mixture-of-Experts (MoE)** architecture can address this by:

* Training multiple specialized models (experts), each focused on:

  * Different regions
  * Different user segments
  * Different product categories

* Using a **gating mechanism** to dynamically select the most relevant expert for each request

This enables:

* Better personalization
* Improved scalability
* More efficient use of model capacity

---

## Conclusion

This project demonstrates a practical and production-aware approach to building a recommendation API.

It emphasizes:

* Clear system design
* Realistic scalability considerations
* Thoughtful progression from rule-based systems to ML-driven architectures

while maintaining alignment with real-world product requirements.
