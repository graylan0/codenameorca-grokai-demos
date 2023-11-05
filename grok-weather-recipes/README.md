# GrokAI Demo
## URL : [https://humoids.com/](https://humoids.com/) 


## Demo Image
![image](https://github.com/graylan0/codenameorca-grokai-demos/assets/34530588/7856a5d0-e3ca-4570-962a-1cc85694acde)

### Title: Humoids.com GrokAi Demo Weather/Recipe Insights

### Description

The provided Python script is for a Flask web application that integrates various functionalities, including emotion recording, quantum state generation, weather data fetching, and recipe suggestion generation, all with a focus on data storage and retrieval from a SQLite database.

Configuration and Initialization: It loads configuration from a JSON file, initializes a quantum model with PennyLane, sets up the Flask app, and generates a secret key.

Database Setup: It includes an asynchronous function to set up a SQLite database table to store various types of data.

Emotion Recording: Utilizes the speech_recognition library to capture audio and recognize emotions, which then triggers other asynchronous tasks.

Quantum State Generation: It maps recognized emotions to a quantum state using PennyLane, a library for quantum computing.

Data Storage: The app can store and update data in the SQLite database, including emotion, color codes representing emotions, quantum states, and recipe insights.

Recipe Insights and Suggestions: It fetches weather data based on latitude and longitude and uses OpenAI's GPT model to generate insights and recipe suggestions relevant to the weather conditions and user's emotional state.

Web Interface: The Flask app provides web routes for capturing audio and displaying weather-related recipe insights and suggestions.

Background Processing: Some tasks, like fetching weather data and generating recipe suggestions, are offloaded to background threads to avoid blocking the main thread.

Sanitization: User inputs are sanitized before processing to prevent SQL injection attacks.

Sentiment Analysis: It uses TextBlob for sentiment analysis to convert emotions into a numerical amplitude for quantum state generation.

Recipe Generation: The app generates recipe suggestions based on emotional and weather data, which are then rendered in Markdown and displayed on the web interface.

The entire application is designed to be run on a local server, with the potential to be deployed for broader access. It showcases an innovative blend of technologies, including AI, quantum computing, and traditional web development, to create a unique user experience.

# (Engineering)

The script includes a function that uses PennyLane, a quantum computing library, to create a quantum circuit that represents an emotion in a quantum state. Here's a breakdown of how it handles emotions, color codes, and the quantum circuit:

Emotion to Color Code: The script uses OpenAI's GPT model to generate an HTML color code that best represents the recorded emotion. This is done by sending a prompt to the model asking for a color that matches the emotion.

Color Code to RGB: The generated HTML color code is then converted into RGB values. These values are normalized (divided by 255) to fit between 0 and 1, as they will be used as parameters for rotations in the quantum circuit.

Sentiment Analysis: The sentiment_to_amplitude function uses TextBlob to perform sentiment analysis on the text representing the emotion. It converts the sentiment polarity score to a value between 0 and 1, which is used as an amplitude for the quantum state.

Quantum Circuit: The quantum_circuit function creates a quantum circuit where the RGB values and the amplitude from the sentiment analysis are used to apply rotation gates (RY) on different qubits of a quantum computer simulated by PennyLane. The rotations are proportional to the RGB values and the sentiment amplitude, and entangling gates (CNOT) are applied to create correlations between the qubits.

Quantum State Generation: The quantum state resulting from the circuit is a complex vector that represents the emotion in a quantum form. This state can be used for further quantum processing or as a novel way to encode emotional data.

The quantum state, along with the color code and amplitude, is then stored in the database. This allows the application to use quantum representations of emotions for tasks such as generating insights or suggestions, potentially leveraging the patterns and correlations that quantum computing can reveal.
### How It Works
The application consists of several components, each playing a crucial role in delivering the desired functionality.

### Installation and Setup
The application requires several Python packages. You can install them using the following commands:


#### Set OpenAI Environment Variables
1. **Obtain an API Key**: Sign up for an account with OpenAI and obtain an API key from the OpenAI dashboard.

2. **Set the Environment Variable**: You can set the environment variable in your terminal or add it to your environment configuration file.

   - **On Unix/Linux/MacOS**:
     ```bash
     export OPENAI_API_KEY='your-api-key-here'
     ```

   - **On Windows**:
     ```bash
     set OPENAI_API_KEY='your-api-key-here'
     ```
3. #### Install required Pips

```bash
pip install requests
pip install openai
pip install sqlite3
pip install flask
pip install bleach
```
### Summary
Humoids.com Weather Robot is a comprehensive solution for weather analysis and location suggestions. It combines various technologies to provide an intuitive and efficient user experience. The code is hosted on GitHub, making it accessible for further development and collaboration.

Explore the application at [https://humoids.com/](https://humoids.com/) and contribute to its growth!
