from flask import render_template, jsonify, request
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient
from . import dyslexia_bp
import random

load_dotenv()
client = MongoClient("mongodb+srv://diya:diya@cluster0.mgkw8.mongodb.net/")
db = client["Dyslexia"]

# MongoDB collections
def get_or_create_collection(db, collection_name):
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    return db[collection_name]

questions_collection = get_or_create_collection(db, "Assessment")
patterns_collection = get_or_create_collection(db, "Pattern")
users_collection = get_or_create_collection(db, "User")

GEMINI_API_KEY = "AIzaSyC-AublNqOvjvJ5zMNj9gDKoEgagDwU85g"
genai.configure(api_key=GEMINI_API_KEY)

def get_suggestions(score):
    prompt = f"""
    A user has taken a dyslexia assessment and scored {score}. 
    Based on their score, provide three personalized suggestions to help them improve learning and reading.
    Example:
    - If the score is low, suggest simple reading exercises.
    - If the score is high, suggest professional intervention.
    Return the response in three lines without bullet points, using \n as a separator.
    """
    model = genai.GenerativeModel()
    response = model.generate_content(prompt)
    suggestions = response.text.strip().split("\n")[:3] 
    return suggestions

@dyslexia_bp.route('/dyslexia')
def dyslexia_home():
    return render_template('landing.html')


@dyslexia_bp.route('/get_questions')
def get_questions():
    questions = list(questions_collection.find({}, {"_id": 0}))  
    return jsonify(questions)

@dyslexia_bp.route('/get_patterns')
def get_patterns():
    all_patterns = list(patterns_collection.find({}, {"_id": 0}))
    shuffled_patterns = random.sample(all_patterns, min(5, len(all_patterns)))  
    return jsonify(shuffled_patterns)

@dyslexia_bp.route('/get_suggestions', methods=['GET'])
def fetch_suggestions():
    score = int(request.args.get('score', 0))  
    suggestions = get_suggestions(score)
    return jsonify({"suggestions": suggestions})

@dyslexia_bp.route("/registerapi", methods=["POST"])
def registerapi():
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    placeofbirth = data.get("placeofbirth")

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "Email already registered"}), 400

    user_data = {
        "username": username,
        "email": email,
        "password": password,
        "name": name,
        "age": age,
        "gender": gender,
        "placeofbirth": placeofbirth
    }
    
    users_collection.insert_one(user_data)
    return jsonify({"message": "Registration successful"}), 201

@dyslexia_bp.route("/loginapi", methods=["POST"])
def loginapi():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    if not user or user["password"] != password:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "username": user["username"]}), 200


@dyslexia_bp.route('/activity')
def activity():
    return render_template('activity.html')

@dyslexia_bp.route('/assessment')
def assessment():
    return render_template('assessment.html')

@dyslexia_bp.route('/pattern')
def pattern():
    return render_template("pattern.html")

@dyslexia_bp.route('/reading')
def reading():
    return render_template('reading.html')


@dyslexia_bp.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@dyslexia_bp.route('/login')
def login():
    return render_template('login.html')