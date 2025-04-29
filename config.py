import os

# MongoDB connection URI from environment variable
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "mlgcme_demo")

# Optional: if you use OpenAI later
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
