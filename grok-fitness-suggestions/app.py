import openai
import markdown
import bleach
import requests
from concurrent.futures import ThreadPoolExecutor
from waitress import serve
from flask import Flask, render_template, request
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
import json
import re
import aiosqlite
import speech_recognition as sr
import threading
import nest_asyncio
import asyncio
import pennylane as qml
from pennylane import numpy as np
from textblob import TextBlob
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired
import secrets


# Load configuration from JSON
with open("config.json", "r") as f:
    config = json.load(f)

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

openai.api_key = config["openai_api_key"]
nest_asyncio.apply()

# Initialize Quantum Language Model
qml_model = qml.device('default.qubit', wires=4)

# Flask app initialization
app = Flask(__name__)

# Generate a random secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Initialize the database
async def initialize_db():
    async with aiosqlite.connect("unified_data.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS data (
                type TEXT,
                latitude REAL,
                longitude REAL,
                fitnessinsights TEXT,
                fitness_suggestions TEXT,
                emotion TEXT,
                color_code TEXT,
                quantum_state TEXT,
                amplitude REAL,
                cluster_label TEXT,
                cluster_color_code TEXT,
                fitnessinsights_detection_state TEXT,
                timestamp DATETIME,
                PRIMARY KEY (type, latitude, longitude)
            )
        ''')
        await db.commit()

# Create a FlaskForm for the timer input
class TimerForm(FlaskForm):
    time = IntegerField('Recording Time (seconds)', validators=[DataRequired()])
    submit = SubmitField('Start Recording')

# Sanitize input to prevent SQL injection
def sanitize_input(input_str):
    return bleach.clean(input_str)

# Function for recording emotion with a timer
async def record_emotion(time):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Please wait. Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print("Microphone calibrated.")
        print(f"Recording for {time} seconds...")
        audio_data = recognizer.listen(source, timeout=time)
        print("Recording complete.")

    return recognizer.recognize_google(audio_data)

# Function for generating emotional data
async def generate_emotion_data(emotion, task1_label, task2_label, task3_label):
    try:
        # Task 1: Generate HTML color code
        task1_prompt = f"Please generate an HTML color code that best represents the emotion: {emotion}."
        task1_response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": task1_prompt}
            ]
        )
        color_code = re.search(r'#[0-9a-fA-F]{6}', task1_response['choices'][0]['message']['content'])
        
        amplitude = None  # Initialize amplitude
        
        if color_code:
            # Calculate amplitude if color code is available
            amplitude = sentiment_to_amplitude(emotion)
        
        # Task 3: Generate quantum state
        if color_code:
            quantum_state = quantum_circuit(color_code.group(0), amplitude).numpy()
        else:
            quantum_state = None

        # Store the data
        await store_data("emotion", emotion, color_code.group(0) if color_code else None, quantum_state, amplitude, task1_label, task2_label, None)

        # Task 2: Perform fitnessinsights detection using ChatGPT with quantum data
        task2_prompt = f"Please analyze the user's input as {quantum_state} this is the {amplitude} and the text generating the quantum state: {emotion}, and provide insights into fitnessinsights detection by providing the following 1. Enact advancedd understanding through the quantum clusting of emotions then specificl design eeven taylor insights for user food recipe suggestions customized from inspection of quantum state emotion mmaps, quantum insights.  Following is quantum state data that provides a right to left emotional and brain capacitive delivery of understanding to ai models. Interpreate the data from the text in the example. Highly Fun and Chatty about food "
        task2_response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": " Please analyze the user's input as {quantum_state} this is the {amplitude} and the text generating the quantum state: {emotion}, and provide insights into fitnessinsights detection by providing the following 1. Enact advancedd understanding through the quantum clusting of emotions then specificl design eeven taylor insights for user food recipe suggestions customized from inspection of quantum state emotion mmaps, quantum insights.  Following is quantum state data that provides a right to left emotional and brain capacitive delivery of understanding to ai models. Interpreate the data from the text in the example. Highly Fun and Chatty about food"},
                {"role": "user", "content": task2_prompt}
            ]
        )
        fitnessinsights_detection_state = task2_response['choices'][0]['message']['content']

        # Update the stored data with fitnessinsights detection information
        await update_fitnessinsights_detection_state(emotion, fitnessinsights_detection_state)

    except openai.error.InvalidRequestError as e:
        print(f"OpenAI error: {e}")

# Store data in the database
async def store_data(data_type, emotion, color_code, quantum_state, amplitude, cluster_label, cluster_color_code, fitnessinsights_detection_state):
    async with aiosqlite.connect("unified_data.db") as db:
        await db.execute("""
            INSERT OR REPLACE INTO data (type, emotion, color_code, quantum_state, amplitude, cluster_label, cluster_color_code, fitnessinsights_detection_state, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data_type, emotion, color_code, str(quantum_state.tolist()) if quantum_state.all() else None, amplitude, cluster_label, cluster_color_code, fitnessinsights_detection_state, datetime.now()))
        await db.commit()

# Update fitnessinsights detection state in the database
async def update_fitnessinsights_detection_state(emotion, fitnessinsights_detection_state):
    async with aiosqlite.connect("unified_data.db") as db:
        await db.execute("""
            UPDATE data
            SET fitnessinsights_detection_state = ?
            WHERE type = ? AND emotion = ?
        """, (fitnessinsights_detection_state, "emotion", emotion))
        await db.commit()

# Sentiment analysis to amplitude mapping
def sentiment_to_amplitude(text):
    analysis = TextBlob(text)
    return (analysis.sentiment.polarity + 1) / 2

@qml.qnode(qml_model)
def quantum_circuit(color_code, amplitude):
    r, g, b = [int(color_code[i:i+2], 16) for i in (1, 3, 5)]
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    qml.RY(r * np.pi, wires=0)
    qml.RY(g * np.pi, wires=1)
    qml.RY(b * np.pi, wires=2)
    qml.RY(amplitude * np.pi, wires=3)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    qml.CNOT(wires=[2, 3])
    return qml.state()

# Function for capturing audio and initiating fitnessinsights detection
@app.route('/capture_audio', methods=['GET', 'POST'])
def capture_audio():  # Removed 'async'
    form = TimerForm()
    if form.validate_on_submit():
        time = form.time.data
        # Removed 'await'
        emotion = run_async(record_emotion(time))  
        
        # Create a thread to run the coroutine
        thread = threading.Thread(target=lambda: asyncio.run(generate_emotion_data(emotion, "color_code", "fitnessinsights_detection_state", "quantum_state")))
        thread.start()
        return "Audio recording and fitnessinsights detection initiated."
    return render_template('capture_audio.html', form=form)

async def save_to_sql(data_type, latitude, longitude, fitnessinsights, fitness_suggestions):
    async with aiosqlite.connect("unified_data.db") as db:
        await db.execute(
            '''
            INSERT OR REPLACE INTO data (type, latitude, longitude, fitnessinsights, fitness_suggestions, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                data_type,
                latitude,
                longitude,
                sanitize_input(fitnessinsights),
                sanitize_input(fitness_suggestions),
                datetime.now()
            )
        )
        await db.commit()

async def retrieve_from_sql(latitude, longitude, data_type):
  async with aiosqlite.connect("unified_data.db") as db:
      cursor = await db.execute(
        'SELECT fitnessinsights, fitness_suggestions, timestamp FROM data WHERE type = ? AND latitude = ? AND longitude = ?',
        (data_type, latitude, longitude))  # Removed sanitize_input calls
      result = await cursor.fetchone()
      return result if result else (None, None, None)

def get_fitnessinsights(latitude, longitude):

  def fetch_weather_data():
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,soil_moisture_0_1cm&temperature_unit=fahrenheit&forecast_days=16'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

  with ThreadPoolExecutor() as executor:
    future = executor.submit(fetch_weather_data)
    weather_data = future.result()

  # Check if weather_data is None and handle the error
  if weather_data is None:
    return "Error fetching weather data"

  rules = f"""Analyze the weather data for the given location with the following details: Provide Indepth Details to the weather
                Temperature: {weather_data['hourly']['temperature_2m']},
                Timestamps: {datetime.now().strftime("%Y-%m-%d %H:%M")} to {datetime.now() + timedelta(hours=len(weather_data['hourly']['temperature_2m']) - 1)}. Provide insights and predictions."""

  response = openai.ChatCompletion.create(
    model='gpt-4-vision-preview',
    messages=[{
      "role": "system",
      "content": rules
      
    }, {
      "role":
      "user",
      "content":
      
      "Please analyze the weather data and provide insights."
      
    }],
  max_tokens=950)
  return response['choices'][0]['message']['content']


def get_fitness_suggestions(fitnessinsights, latitude, longitude):
  prompt = f"The weather insights for the recipe (Latitude: {latitude}, Longitude: {longitude}) are as follows: {fitnessinsights}. Suggest the unique fitness routines based upon the localized population and universal weather insights provided. "
  response = openai.ChatCompletion.create(model='gpt-4-vision-preview',
                                          messages=[{
                                            "role":
                                            "system",
                                            "content":
                                            "You are a helpful assistant."
                                          }, {
                                            "role": "user",
                                            "content": prompt
                                          }],
                                          max_tokens=950)
  return response['choices'][0]['message']['content']
def update_easley_sc():
  latitude = '34.8298'
  longitude = '-82.6015'
  fitnessinsights = get_fitnessinsights(latitude, longitude)
  fitness_suggestions = get_fitness_suggestions(fitnessinsights, latitude,
                                                  longitude)
  save_to_sql("weather", latitude, longitude, fitnessinsights, fitness_suggestions)

async def weather():
    latitude_str = request.form.get('latitude', '34.8298')
    longitude_str = request.form.get('longitude', '-82.6015')

    # Sanitize the latitude and longitude values
    latitude_str = sanitize_input(latitude_str)
    longitude_str = sanitize_input(longitude_str)

    # Validate that latitude and longitude are valid floating-point numbers
    try:
        latitude = float(latitude_str)
        longitude = float(longitude_str)
    except ValueError:
        return "Invalid latitude or longitude"

    # Ensure latitude and longitude are within valid ranges
    if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
        return "Invalid latitude or longitude"

    fitnessinsights, fitness_suggestions, timestamp = await retrieve_from_sql(
        latitude, longitude, "weather")

    if timestamp is None or (datetime.now() -
                            datetime.fromisoformat(timestamp)) > timedelta(
                                hours=24):
        fitnessinsights = get_fitnessinsights(latitude, longitude)
        fitness_suggestions = get_fitness_suggestions(fitnessinsights, latitude,
                                                        longitude)
        await save_to_sql("weather", latitude, longitude, fitnessinsights, fitness_suggestions)

    fitnessinsights_html = markdown.markdown(fitnessinsights)
    fitness_suggestions_html = markdown.markdown(fitness_suggestions)

    return render_template('weather.html',
                            fitnessinsights=fitnessinsights_html,
                            fitness_suggestions=fitness_suggestions_html)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config["your_secret_key_field"]  # Make sure this field exists in your config.json
    app.add_url_rule('/', 'weather', weather, methods=['GET', 'POST'])
    app.add_url_rule('/capture_audio', 'capture_audio', capture_audio, methods=['GET', 'POST'])
    return app

if __name__ == '__main__':
    run_async(initialize_db())  # Initialize the database
    app = create_app()
    serve(app, host='localhost', port=8080)
