from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)

CORS(app)


# GEMINI API KEY

# genai.configure( api_key="AIzaSyCXJYCzx-FLzcRVj89QuwkOXUMo4CYah6c")

# model =genai.GenerativeModel("models/gemini-1.5-flash")
 



# Paste your Gemini API key here
genai.configure(api_key="AIzaSyCXJYCzx-FLzcRVj89QuwkOXUMo4CYah6c")

# Load Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash")

try:
    # Test message
    response = model.generate_content("Hello")

    # Print AI response
    print("\nAI Response:\n")
    print(response.text)

except Exception as e:
    print("\nError:\n")
    print(e)