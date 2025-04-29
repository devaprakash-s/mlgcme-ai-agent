# api.py

from fastapi import FastAPI
from db_connect import get_database
import pandas as pd

app = FastAPI()

# Connect to the database
db = get_database()

# Collections
users_col = db["users"]
courses_col = db["courses"]
enrollments_col = db["enrollments"]
outcomes_col = db["outcomes"]

# ---- Root API ----
@app.get("/")
def root():
    return {"message": "MLGCME AI Agent API is running"}

# ---- Layer 1: Analytics API ----
@app.get("/analytics/overview")
def get_analytics_overview():
    total_users = users_col.count_documents({})
    total_courses = courses_col.count_documents({})
    total_enrollments = enrollments_col.count_documents({})
    total_completed = enrollments_col.count_documents({"status": "completed"})
    
    completion_rate = (total_completed / total_enrollments) * 100 if total_enrollments > 0 else 0

    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "completion_rate_percentage": round(completion_rate, 2)
    }

# ---- Layer 2: Deep Insights API ----
@app.get("/insights/patterns")
def get_deep_insights():
    # Completion rate by role
    pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_info"
            }
        },
        {"$unwind": "$user_info"},
        {"$group": {
            "_id": "$user_info.role",
            "total_enrollments": {"$sum": 1},
            "completed": {"$sum": {"$cond": [{"$eq": ["$status", "completed"]}, 1, 0]}}
        }},
        {"$project": {
            "role": "$_id",
            "completion_rate": {"$multiply": [{"$divide": ["$completed", "$total_enrollments"]}, 100]},
            "_id": 0
        }}
    ]
    role_insights = list(enrollments_col.aggregate(pipeline))

    return {
        "completion_rate_by_role": role_insights
    }

# ---- Layer 3: Action Strategies API ----
@app.get("/actions/recommendations")
def get_action_recommendations():
    recs = []

    # Check for courses with low completion rates
    pipeline = [
        {
            "$lookup": {
                "from": "enrollments",
                "localField": "_id",
                "foreignField": "course_id",
                "as": "course_enrollments"
            }
        },
        {"$project": {
            "title": 1,
            "completion_rate": {
                "$cond": [
                    {"$gt": [{"$size": "$course_enrollments"}, 0]},
                    {
                        "$multiply": [
                            {
                                "$divide": [
                                    {
                                        "$size": {
                                            "$filter": {
                                                "input": "$course_enrollments",
                                                "as": "enr",
                                                "cond": {"$eq": ["$$enr.status", "completed"]}
                                            }
                                        }
                                    },
                                    {"$size": "$course_enrollments"}
                                ]
                            },
                            100
                        ]
                    },
                    0
                ]
            }
        }}
    ]

    course_analysis = list(courses_col.aggregate(pipeline))

    for course in course_analysis:
        if course["completion_rate"] < 50:
            recs.append({
                "recommendation": f"Consider redesigning course '{course['title']}' - low completion rate ({round(course['completion_rate'],2)}%)."
            })

    # Suggest general engagement tips
    engagement_tips = [
        "Send reminder nudges to learners with incomplete courses.",
        "Personalize course suggestions based on user role and specialty.",
        "Encourage completion by offering micro-certificates for each module."
    ]

    for tip in engagement_tips:
        recs.append({"recommendation": tip})

    return {"recommendations": recs}
