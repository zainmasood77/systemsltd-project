from flask import Flask, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import requests
import uuid
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

scheduler = BackgroundScheduler()
scheduler.start()

# ✅ Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('api_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_logs (
            id TEXT PRIMARY KEY,
            endpoint TEXT,
            status_code INTEGER,
            response TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/schedule', methods=['POST'])
def schedule_job():
    data = request.get_json()

    # Validate required fields
    try:
        duration = int(data['duration'])       # in minutes
        frequency = int(data['frequency'])     # calls per hour
        endpoint = data['endpoint'].strip()    # API endpoint
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'Invalid input format'}), 400

    if not endpoint:
        return jsonify({'error': 'Endpoint cannot be empty'}), 400

    # Calculate timing
    interval_seconds = int(3600 / frequency)
    total_runs = int((duration * 60) / interval_seconds)
    job_id = str(uuid.uuid4())

    # Define the scheduled job
    def job_logic(run_count=[0]):
        if run_count[0] >= total_runs:
            scheduler.remove_job(job_id)
            return

        try:
            response = requests.get(endpoint)
            status_code = response.status_code
            content_type = response.headers.get("Content-Type", "")
            if 'application/json' in content_type:
                resp_data = str(response.json())
            else:
                resp_data = response.text[:500]  # Store first 500 chars max

            timestamp = datetime.datetime.now().isoformat()

            # ✅ Store in SQLite
            conn = sqlite3.connect('api_logs.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO api_logs (id, endpoint, status_code, response, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (str(uuid.uuid4()), endpoint, status_code, resp_data, timestamp))
            conn.commit()
            conn.close()

        except Exception as e:
            print(f"[{job_id}] ❌ Error: {e}")

        run_count[0] += 1

    # Schedule the job
    scheduler.add_job(
        job_logic,
        trigger=IntervalTrigger(seconds=interval_seconds),
        id=job_id,
        name=f"Call {endpoint}",
        replace_existing=False
    )

    print(f"[{job_id}] 🚀 Scheduled every {interval_seconds}s for {total_runs} runs.")
    return jsonify({'message': 'Job scheduled', 'job_id': job_id})

@app.route('/')
def health():
    return jsonify({'status': 'Backend running'})

if __name__ == '__main__':  # ✅ Corrected
    app.run(debug=True, host='0.0.0.0', port=5000)