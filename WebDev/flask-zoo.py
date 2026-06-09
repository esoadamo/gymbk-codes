from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from typing import TypedDict, List
import os

try:
    import requests
    from dotenv import load_dotenv
except ImportError as e:
    print("Chybi vam balicky", e)
    print("Doinstalujte je pomoci pip install requests python-dotenv")
    print("Nebo uv add requests python-dotenv")
    exit(1)

load_dotenv()


app = Flask("zoo")


class Comment(TypedDict):
    comment: str
    name: str | None


class ChatMessage(TypedDict):
    role: str
    content: str


class Database(TypedDict):
    total_amount: int
    comments: List[Comment]


DATABASE: Database = {
    "total_amount": 0,
    "comments": []
}


@app.route('/')
def index():
    return render_template(
        "zoo.html",
        total_amount=DATABASE["total_amount"],
        comments=DATABASE["comments"],
        url=request.url
    )


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)


@app.route('/donate', methods=['POST'])
def donate():
    try:
        amount = int(request.form.get('amount', 0))
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError:
        return "Invalid amount", 400
    name = request.form.get('name', None)
    comment_text = request.form.get('comments', '')
    
    DATABASE["total_amount"] += amount
    
    if comment_text:
        DATABASE["comments"].append({
            "comment": comment_text,
            "name": name
        })
    
    return redirect(url_for('index'))


@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.form.get('message', '')
    chat_history = request.form.get('history', '[]')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Render the current page to string for context
    page_context = render_template("zoo.html", total_amount=DATABASE["total_amount"], comments=DATABASE["comments"])
    
    # Prepare the full context for Mistral API
    context = f"Page context:\n{page_context}\n\nChat history:\n{chat_history}\n\nUser's new question: {user_message}"
    
    # Call Mistral API
    mistral_api_key = os.getenv('MISTRAL_API_KEY')
    if not mistral_api_key:
        return jsonify({"error": "Mistral API key not configured"}), 500
    
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {mistral_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-tiny",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant for a Zoo donation website. Answer questions based on the provided context about the page."},
                    {"role": "user", "content": context}
                ]
            }
        )

        response.raise_for_status()
        bot_reply = response.json()['choices'][0]['message']['content']
        
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
