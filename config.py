# config.py

# MongoDB connection URI
MONGO_URI = "mongodb+srv://devaprakashs:Omega1514@cluster0.rbkoovo.mongodb.net/?retryWrites=true&w=majority"

# MongoDB database name
DATABASE_NAME = "mlgcme_demo"

# OpenAI API Key (will be loaded from environment on Render)
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
