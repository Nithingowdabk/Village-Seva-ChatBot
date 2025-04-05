from flask import Flask, render_template, request, jsonify, session
import requests
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "bdbd5f33a2d21edae7721305bac8ac4f9a77852b1875b9e021ed5b4f90140679"  # Needed for Flask session storage

# NVIDIA API Setup
NVIDIA_API_KEY = "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"
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

# Google Search API Setup (SerpAPI)
SERP_API_KEY = "your_serpapi_key"

# Topics that require fresh search results
SEARCH_KEYWORDS = ["scheme", "loan", "latest", "news", "subsidy", "update", "government", "apply", "registration"]

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

def summarize_results(query, results):
    """Use NVIDIA AI to generate a structured summary from search results."""
    prompt = f"""Summarize the following search results for the query: "{query}". 
    Provide a structured summary in simple language for Indian users.

    Search Results:
    {results}

    Structure the response as follows:
    - **Overview**: Brief explanation
    - **Key Points**: (Bullet points with key info)
    - **Next Steps**: What should the user do?
    """

    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=512
    )
    
    return completion.choices[0].message.content.strip()

@app.route("/")
def home():
    session.clear()  # Clear session when the user starts a new chat
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "⚠️ Please enter a valid message."})

    # Retrieve past bot responses from session
    conversation_history = session.get("conversation_history", [])

    # Check if query needs fresh search results
    if any(keyword in user_message.lower() for keyword in SEARCH_KEYWORDS):
        search_results = google_search(user_message)
        structured_summary = summarize_results(user_message, "\n".join(search_results))

        # Store response in session for later reference
        conversation_history.append({"user": user_message, "bot": structured_summary})
        session["conversation_history"] = conversation_history

        return jsonify({"response": structured_summary})

    # Prepare AI prompt with past context
    past_responses = "\n".join([f"User: {item['user']}\nBot: {item['bot']}" for item in conversation_history])
    enhanced_prompt = f"""
    Previous conversation:
    {past_responses}

    Now, user asks: "{user_message}"
    Answer the question based on the previous conversation.
    """

    try:
        # Ask NVIDIA AI for a response
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": enhanced_prompt}],
            temperature=0.5,
            top_p=1,
            max_tokens=512
        )
        
        ai_response = completion.choices[0].message.content.strip()

        # Store response in session
        conversation_history.append({"user": user_message, "bot": ai_response})
        session["conversation_history"] = conversation_history

        return jsonify({"response": ai_response})
    
    except Exception as e:
        return jsonify({"response": f"❌ Error processing request: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
