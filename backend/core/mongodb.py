from pymongo import MongoClient

# Подключение к MongoDB (локально)
client = MongoClient("mongodb://localhost:27017/")
db = client["resume_analyzer"]

resumes_collection = db["resumes"]
