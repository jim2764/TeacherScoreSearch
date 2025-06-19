from flask import Flask, request, render_template
import psycopg2
import os
from dotenv import load_dotenv

# 載入 .env（本地開發用）
load_dotenv()

app = Flask(__name__)

# PostgreSQL 資料庫連線資訊（Render 上使用環境變數）
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    exam_id = request.form.get('exam_id')
    id_number = request.form.get('id_number')

    result = None
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, written_score, oral_score
            FROM teacher_scores
            WHERE exam_id = %s AND id_number = %s
        """, (exam_id, id_number))

        row = cursor.fetchone()

        print(row)

        if row:
            result = {
                'name': row[0],
                'written_score': row[1],
                'oral_score': row[2]
            }

        cursor.close()
        conn.close()
    except Exception as e:
        result = None

    return render_template('result.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)