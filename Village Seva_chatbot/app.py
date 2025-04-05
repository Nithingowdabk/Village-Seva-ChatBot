from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
from gtts import gTTS
import os
import re
import time
import requests
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)   # Needed for session storage

# NVIDIA API Configuration
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# Google Search API Setup (SerpAPI)
SERP_API_KEY = "bdbd5f33a2d21edae7721305bac8ac4f9a77852b1875b9e021ed5b4f90140679"

# Topics that require fresh search results
SEARCH_KEYWORDS = ["scheme", "loan", "latest", "news", "subsidy", "update", "government", "apply", "registration"]

# Store user language preference
user_language = {"lang": "English"}

# Function to remove emojis from speech
def remove_emojis(text):
    return re.sub(r'[\U00010000-\U0010FFFF]', '', text)  # Remove all emoji characters

# Function to clean response text
def clean_text(text):
    text = re.sub(r'\*|\+#', '', text)  # Remove asterisks and plus signs
    text = re.sub(r'https?://\S+', '', text)  # Remove URLs
    text = re.sub(r'[_+={}\[\]:;"\<>,?/|`~#]', '', text)  # Remove unwanted punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def google_search(query, num_results=3):
    """Fetch latest search results using Google Search API."""
    url = "https://serpapi.com/search"
    params = {
        "q": f"{query} India site:.in",
        "api_key": SERP_API_KEY,
        "num": num_results
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get("organic_results", [])
        
        search_results = []
        for res in results:
            title = res.get("title", "")
            snippet = res.get("snippet", "")
            link = res.get("link", "")
            search_results.append(f"{title}: {snippet} (Source: {link})")
        
        return search_results if search_results else ["No recent updates found."]
    else:
        return ["Error fetching search results."]

def summarize_results(query, results, lang):
    """Use NVIDIA AI to generate a structured summary from search results."""
    prompt = f"""Summarize the following search results for the query: "{query}". 
    Provide a structured summary in simple language for Indian users.

    Search Results:
    {results}

    Structure the response as follows:
    Overview: Brief explanation
    Key Points: (Bullet points with key info)
    Next Steps: What should the user do?
    """

    if lang == "Kannada":
        prompt = f"Translate the following summary into Kannada: {prompt}"

    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=2000
    )
    
    return completion.choices[0].message.content.strip()

def chatbot_response(user_input, lang):
    """Processes user input, retrieves AI response, and generates speech output."""
    try:
        # Retrieve past conversation history
        conversation_history = session.get("conversation_history", [])

        # If the query requires real-time info, fetch from Google Search API
        if any(keyword in user_input.lower() for keyword in SEARCH_KEYWORDS):
            search_results = google_search(user_input)
            structured_summary = summarize_results(user_input, "\n".join(search_results), lang)

            # Store in session for later reference
            conversation_history.append({"user": user_input, "bot": structured_summary})
            session["conversation_history"] = conversation_history

            return structured_summary, generate_speech(structured_summary, lang)

        # Use past responses to give better answers
        past_responses = "\n".join([f"User: {item['user']}\nBot: {item['bot']}" for item in conversation_history])
        enhanced_prompt = f"""
        Previous conversation:
        {past_responses}

        Now, user asks: "{user_input}"
        Answer the question based on the previous conversation.
        """

        # Request AI response
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": enhanced_prompt}],
            temperature=0.5,
            top_p=1,
            max_tokens=2000
        )

        response_text = completion.choices[0].message.content.strip()
        cleaned_text = clean_text(response_text)

        # Store response in session
        conversation_history.append({"user": user_input, "bot": cleaned_text})
        session["conversation_history"] = conversation_history

        return cleaned_text, generate_speech(cleaned_text, lang)

    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't process your request.", None

def generate_speech(text, lang):
    """Converts text to speech and saves it as an audio file."""
    try:
        timestamp = int(time.time())  # Unique filename
        audio_filename = f"static/response_{timestamp}.mp3"
        speech_text = remove_emojis(clean_text(text))  # Remove emojis and unwanted characters

        if speech_text.strip():
            tts = gTTS(text=speech_text, lang="kn" if lang == "Kannada" else "en", slow=False)
            tts.save(audio_filename)
            return audio_filename
        else:
            return None
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

@app.route("/")
def home():
    session.clear()  # Clear history when user starts new chat
    return render_template("index.html")

@app.route("/set_language", methods=["POST"])
def set_language():
    """Set user preferred language (English/Kannada)."""
    data = request.get_json()
    selected_language = data.get("language", "English")
    user_language["lang"] = selected_language
    return jsonify({"message": f"Language set to {selected_language}"})

@app.route("/get_response", methods=["POST"])
def get_response():
    """Handles user messages and returns AI response with optional speech."""
    data = request.get_json()
    user_message = data.get("message", "").strip()
    lang = user_language["lang"]

    if not user_message:
        return jsonify({"response": " Please enter a valid message."})

    bot_reply, audio_path = chatbot_response(user_message, lang)

    return jsonify({"response": bot_reply, "audio": f"{audio_path}?t={int(time.time())}" if audio_path else None})

if __name__ == "__main__":
    app.run(debug=True)
