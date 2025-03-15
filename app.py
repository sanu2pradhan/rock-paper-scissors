from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Register user
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data["name"]
    
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute("INSERT INTO users (name, score) VALUES (?, 0)", (name,))
        conn.commit()
    
    conn.close()
    return jsonify({"message": "User registered!"})

# Update score
@app.route("/update_score", methods=["POST"])
def update_score():
    data = request.json
    name = data["name"]
    points = data["score"]

    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET score = score + ? WHERE name = ?", (points, name))
    conn.commit()
    conn.close()

    return jsonify({"message": "Score updated!"})

# Get leaderboard
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, score FROM users ORDER BY score DESC LIMIT 10")
    leaderboard_data = cursor.fetchall()
    
    conn.close()
    return jsonify(leaderboard_data)

if __name__ == "__main__":
    app.run(debug=True)
