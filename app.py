from flask import Flask, render_template
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_scores():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()
    cur.execute("SELECT student_id, name, score FROM student_scores")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.route("/")
def index():
    data = get_scores()
    return render_template("index.html", scores=data)

if __name__ == "__main__":
    app.run(debug=True)