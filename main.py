# main.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Merged Assignments - Enrollment / Progress / Rating / Access Control")

# ---- Shared in-memory storage (single place) ----
course_lessons = {
    1: [1, 2, 3, 4],
    2: [1, 2]
}

enrollments: Dict[int, set] = {}           # { userId: set(courseId) }
completions: Dict[tuple, set] = {}         # { (userId, courseId): set(lessonId) }
course_ratings: Dict[int, Dict[int, float]] = {}  # { courseId: { userId: rating } }

# ---- Enrollment endpoint ----
@app.post("/courses/{courseId}/enroll")
def enroll_user(courseId: int, userId: int = Query(..., description="user id")):
    if courseId not in course_lessons:
        raise HTTPException(status_code=404, detail="Course not found")
    user_set = enrollments.setdefault(userId, set())
    if courseId in user_set:
        raise HTTPException(status_code=400, detail="User already enrolled")
    user_set.add(courseId)
    return {"message": "enrollment successful", "userId": userId, "courseId": courseId}

# ---- Lesson completion endpoint (idempotent) ----
@app.post("/courses/{courseId}/lessons/{lessonId}/complete")
def complete_lesson(courseId: int, lessonId: int, userId: int = Query(..., description="user id")):
    if courseId not in course_lessons:
        raise HTTPException(status_code=404, detail="Course not found")
    if lessonId not in course_lessons[courseId]:
        raise HTTPException(status_code=404, detail="Lesson not found in course")
    if userId not in enrollments or courseId not in enrollments[userId]:
        raise HTTPException(status_code=400, detail="User not enrolled in course")
    key = (userId, courseId)
    completed_set = completions.setdefault(key, set())
    completed_set.add(lessonId)   # idempotent
    return {"message": "lesson marked completed", "userId": userId, "courseId": courseId, "lessonId": lessonId}

# ---- Progress endpoint ----
@app.get("/users/{userId}/courses/{courseId}/progress")
def get_progress(userId: int, courseId: int):
    if courseId not in course_lessons:
        raise HTTPException(status_code=404, detail="Course not found")
    total = len(course_lessons[courseId])
    completed = len(completions.get((userId, courseId), set()))
    percent = round((completed / total) * 100, 2) if total > 0 else 0.0
    return {
        "userId": userId,
        "courseId": courseId,
        "total_lessons": total,
        "completed_lessons": completed,
        "progress_percentage": percent
    }

# ---- Rating endpoints (only enrolled users can rate) ----
class RatingIn(BaseModel):
    userId: int
    rating: float

@app.post("/courses/{courseId}/rating")
def submit_rating(courseId: int, payload: RatingIn):
    userId = payload.userId
    value = payload.rating
    if courseId not in course_lessons:
        raise HTTPException(status_code=404, detail="Course not found")
    if userId not in enrollments or courseId not in enrollments[userId]:
        raise HTTPException(status_code=403, detail="User not enrolled in course")
    if not (0.5 <= value <= 5.0):
        raise HTTPException(status_code=400, detail="Rating must be between 0.5 and 5.0")
    ratings = course_ratings.setdefault(courseId, {})
    ratings[userId] = value
    return {"message": "rating recorded", "courseId": courseId, "userId": userId, "rating": value}

@app.get("/courses/{courseId}/rating")
def get_course_rating(courseId: int):
    if courseId not in course_lessons:
        raise HTTPException(status_code=404, detail="Course not found")
    ratings = course_ratings.get(courseId, {})
    count = len(ratings)
    avg = round(sum(ratings.values())/count, 2) if count else 0.0
    breakdown = {}
    for r in ratings.values():
        breakdown.setdefault(str(r), 0)
        breakdown[str(r)] += 1
    return {"courseId": courseId, "count": count, "average": avg, "breakdown": breakdown}

# ---- Problem 2: Access Control endpoint ----
@app.get("/courses/{courseId}/lessons")
def get_lessons(courseId: int, userId: int = Query(..., description="user id")):
    if courseId not in course_lessons:
        raise HTTPException(status_code=404, detail="Course not found")
    if userId not in enrollments or courseId not in enrollments[userId]:
        raise HTTPException(status_code=403, detail="Forbidden: user not enrolled")
    return {
        "courseId": courseId,
        "lessons": course_lessons[courseId]
    }
