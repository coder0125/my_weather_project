# app.py
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from weather_service import get_weather_data, get_daily_summary
from alerts import check_alerts, send_email_alert
from db import setup_db, get_daily_summaries 

app = Flask(__name__)

# Task to call the weather API every 5 minutes
def fetch_weather_task():
    get_weather_data()
    alerts = check_alerts()
    if alerts:
        send_email_alert(alerts)

scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_weather_task, trigger="interval", minutes=5)
scheduler.start()

@app.route('/')
def index():
    summaries = get_daily_summaries()
    return render_template('index.html', summaries=summaries)

@app.route('/alerts')
def alerts():
    alerts_list = check_alerts()
    return render_template('alerts.html', alerts=alerts_list)

# Shut down the scheduler when exiting the app
@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    scheduler.shutdown()

if __name__ == '__main__':
    setup_db()  # Setup the database tables if not already created
    app.run(debug=True)
