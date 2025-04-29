# data_generator.py

from faker import Faker
import random
from db_connect import get_database

fake = Faker()
db = get_database()

# Collections
users_col = db["users"]
courses_col = db["courses"]
enrollments_col = db["enrollments"]
outcomes_col = db["outcomes"]

# Clear existing data first (optional, for clean runs)
users_col.delete_many({})
courses_col.delete_many({})
enrollments_col.delete_many({})
outcomes_col.delete_many({})

# 1. Generate Users
roles = ["doctor", "nurse", "pharmacist", "therapist"]
specialties = ["cardiology", "oncology", "endocrinology", "neurology", "orthopedics"]

users = []
for _ in range(200):
    users.append({
        "name": fake.name(),
        "email": fake.email(),
        "role": random.choice(roles),
        "specialty": random.choice(specialties)
    })

users_col.insert_many(users)
print(f"Inserted {len(users)} users.")

# 2. Generate Courses
categories = ["cardiology", "oncology", "diabetes", "mental health", "orthopedics"]
courses = []
for _ in range(20):
    courses.append({
        "title": fake.sentence(nb_words=4),
        "category": random.choice(categories)
    })

courses_col.insert_many(courses)
print(f"Inserted {len(courses)} courses.")

# 3. Generate Enrollments
user_ids = [user["_id"] for user in users_col.find()]
course_ids = [course["_id"] for course in courses_col.find()]

enrollments = []
statuses = ["completed", "in-progress", "dropped"]

for _ in range(600):
    enrollments.append({
        "user_id": random.choice(user_ids),
        "course_id": random.choice(course_ids),
        "status": random.choices(statuses, weights=[0.6, 0.3, 0.1])[0],  # More completions
        "completion_date": str(fake.date_this_year())

    })

enrollments_col.insert_many(enrollments)
print(f"Inserted {len(enrollments)} enrollments.")

# 4. Generate Outcomes
outcomes = []

for enrollment in enrollments:
    if enrollment["status"] == "completed":
        outcomes.append({
            "user_id": enrollment["user_id"],
            "course_id": enrollment["course_id"],
            "outcome_score": random.randint(60, 100),
            "outcome_type": random.choice(["knowledge", "behavior_change", "patient_outcome"])
        })

outcomes_col.insert_many(outcomes)
print(f"Inserted {len(outcomes)} outcomes.")
