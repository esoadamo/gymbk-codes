from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from typing import TypedDict, List

app = Flask("zoo")


class Comment(TypedDict):
    comment: str
    name: str | None


class Database(TypedDict):
    total_amount: int
    comments: List[Comment]


DATABASE: Database = {
    "total_amount": 0,
    "comments": []
}


@app.route('/')
def index():
    return render_template("zoo.html", total_amount=DATABASE["total_amount"], comments=DATABASE["comments"])


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


if __name__ == "__main__":
    app.run(debug=True)
