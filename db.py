import sqlite3

def setup_db():
    """Set up the SQLite database and create the weather_data table if it doesn't exist."""
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            temp REAL NOT NULL,
            feels_like REAL,
            condition TEXT,
            timestamp INTEGER)
    ''')         
    conn.commit()
    conn.close()

def store_weather_data(city, temp, feels_like, condition, timestamp):
    """Stores weather data for a given city into the SQLite database."""
    try:
        conn = sqlite3.connect('weather.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO weather_data (city, temp, feels_like, condition, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (city, temp, feels_like, condition, timestamp))
        conn.commit()
        print(f"Weather data for {city} stored successfully.")
    
    except sqlite3.Error as e:
        print(f"An error occurred while storing weather data: {e}")
    
    finally:
        conn.close()  # Ensure the connection is closed even if an error occurs

def get_daily_summaries():
    """Retrieve daily summaries from the weather_data table."""
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''
        SELECT city, AVG(temp) AS avg_temp, MAX(temp) AS max_temp, condition 
        FROM weather_data
        GROUP BY city, DATE(timestamp, 'unixepoch')
    ''')
    summaries = c.fetchall()
    conn.close()
    return summaries

def get_latest_weather_data():
    """Retrieve the latest weather data entries from the weather_data table."""
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''
        SELECT city, temp 
        FROM weather_data 
        ORDER BY timestamp DESC LIMIT 10
    ''')
    data = c.fetchall()
    conn.close()
    return data
