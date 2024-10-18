# alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db import get_latest_weather_data
# Define the email configuration
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USERNAME = 'your-email@example.com'
EMAIL_PASSWORD = 'your-email-password'
EMAIL_FROM = 'your-email@example.com'
EMAIL_TO = 'recipient-email@example.com'

def check_alerts():
    alerts = []
    weather_data = get_latest_weather_data()
    threshold_temp = 35  # Example threshold for alerts

    for entry in weather_data:
        if entry['temp'] > threshold_temp:
            alerts.append(f"Alert: Temperature in {entry['city']} exceeded {threshold_temp}°C")

    return alerts

def send_email_alert(alerts):
    subject = "Weather Alert: Threshold Breached"
    body = "\n".join(alerts)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject

    # Attach the body
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        print(f"Alert email sent to {EMAIL_TO}")
    except Exception as e:
        print(f"Failed to send email: {e}")
