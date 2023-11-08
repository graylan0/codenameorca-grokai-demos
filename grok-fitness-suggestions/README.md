# humoids.com
## URL : [https://humoids.com/](https://humoids.com/) 



### Title: Humoids.com Fitness Robot

# Quantum Emotional-Mapped Fitness Suggestions

This script is a comprehensive Python application that utilizes several libraries and frameworks to perform tasks such as emotion recording, sentiment analysis, quantum state generation, and fitness insights detection. It is designed to run as a web service using Flask and can be deployed on local servers.

## Features

| Feature | Description |
|---------|-------------|
| **Emotion Recording** | Captures audio input and uses Google's speech recognition to interpret emotions. |
| **Quantum State Generation** | Utilizes PennyLane to create quantum states based on emotional analysis. |
| **Fitness Insights Detection** | Generates fitness suggestions and insights using OpenAI's GPT models. |
| **Weather Data Analysis** | Fetches and analyzes weather data to provide fitness suggestions. |
| **Data Storage** | Uses SQLite database to store and retrieve data asynchronously. |
| **Input Sanitization** | Implements input sanitization to prevent SQL injection attacks. |
| **Quantum Circuit** | Defines a quantum circuit that encodes color codes and amplitudes into quantum states. |
| **Web Forms** | Uses Flask-WTF to create web forms for user interaction. |
| **Threaded Asynchronous Execution** | Employs threading and asyncio for concurrent operations. |

## Installation Guide

### Prerequisites

- Python 3.8 or higher
- Pip (Python package installer)

### Windows Installation

1. **Install Python and Pip**
   - Download Python from the official website.
   - During installation, ensure that you check the option to 'Add Python to PATH'.

2. **Clone the Repository**
   - Use Git to clone the repository or download the ZIP file and extract it.

3. **Install Dependencies**
   - Open Command Prompt and navigate to the project directory.
   - Run `pip install -r requirements.txt` to install all required packages.

4. **Configuration**
   - Create a `config.json` file in the project directory with your OpenAI API key and other configurations.

5. **Run the Application**
   - Execute `python app.py` to start the Flask server.

### Linux/Mac Installation

1. **Install Python and Pip**
   - Use your distribution's package manager to install Python and Pip.

2. **Clone the Repository**
   - Use `git clone` or download and extract the ZIP file.

3. **Install Dependencies**
   - Open a terminal, navigate to the project directory, and run `pip3 install -r requirements.txt`.

4. **Configuration**
   - Same as Windows, create a `config.json` with necessary openai apikey configurations.

5. **Run the Application**
   - Use `python3 app.py` to start the Flask server.

### Usage

- Access the web service by navigating to `localhost:8080` in your web browser.
- Use the provided web forms to interact with the service for emotion recording and fitness insights.


3. #### Install required Pips

```bash
pip install requests
pip install openai
pip install sqlite3
pip install flask
pip install bleach
pip install pennylane
pip install SpeechRecognition
```
