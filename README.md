# Emotion Detection Web Application with Watson NLP & Flask

An AI-powered web application and Python package that analyzes user text statements to detect five distinct emotions (**Anger, Disgust, Fear, Joy, and Sadness**) and identifies the **dominant emotion** using IBM Watson NLP.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Project Architecture & Structure](#project-architecture--structure)
- [Technologies Used](#technologies-used)
- [Prerequisites & Installation](#prerequisites--installation)
- [Running the Application](#running-the-application)
- [Running Unit Tests](#running-unit-tests)
- [Static Code Analysis (Pylint)](#static-code-analysis-pylint)
- [API Reference](#api-reference)
- [Course Submission Guide](#course-submission-guide)

---

## Project Overview

This project is the final capstone for the Coursera course **"Developing AI Applications with Python and Flask"** (IBM Skills Network).

The application provides:
1. A reusable Python package `EmotionDetection` with the `emotion_detector` function.
2. Integration with the IBM Watson NLP Emotion Detection microservice.
3. Robust error handling for blank/invalid inputs (returning HTTP status 400).
4. A Flask web server (`server.py`) with an interactive HTML/JavaScript frontend.
5. Unit tests with Python's `unittest` framework.
6. 100% compliance with PEP 8 standards evaluated by `pylint` (10.00/10 score).

---

## Key Features

- **Multi-Emotion Detection**: Analyzes text to extract individual scores for `anger`, `disgust`, `fear`, `joy`, and `sadness`.
- **Dominant Emotion Identification**: Automatically computes and highlights the dominant emotion.
- **Robust Error Handling**: Safely handles empty strings, blank spaces, or invalid inputs without crashing, returning clear error messages with HTTP status 400.
- **Modern UI**: Clean and responsive web interface for instant interactive emotion analysis.
- **Package Modularity**: Can be imported and used in other Python applications (`from EmotionDetection import emotion_detector`).

---

## Project Architecture & Structure

```text
flaskpython/
│
├── EmotionDetection/
│   ├── __init__.py               # Exposes emotion_detector function
│   └── emotion_detection.py      # Core Watson NLP emotion detection logic
│
├── static/
│   └── mywebscript.js            # Frontend JavaScript for AJAX requests
│
├── templates/
│   └── index.html                # Main application UI
│
├── emotion_detection.py          # Root module entry point for compatibility
├── server.py                     # Flask web server and routing
├── test_emotion_detection.py     # Unit and integration test suite
├── setup.py                      # Package installation configuration
├── requirements.txt              # Project dependencies
├── .gitignore                    # Git ignore file for Python artifacts
└── README.md                     # Complete project documentation
```

---

## Technologies Used

* **Language**: Python 3
* **Web Framework**: Flask
* **NLP Service**: IBM Watson NLP Emotion Detection API
* **HTTP Client**: Requests
* **Testing**: Python `unittest` framework and `unittest.mock`
* **Static Analysis**: Pylint (Score: 10.00/10)
* **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6)

---

## Prerequisites & Installation

### 1. Clone or Open the Project
```bash
cd flaskpython
```

### 2. Create and Activate a Virtual Environment (Optional but recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install the EmotionDetection Package Locally
```bash
pip install -e .
```

---

## Running the Application

Start the Flask server:
```bash
python server.py
```

Output:
```text
 * Serving Flask app 'Emotion Detector'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

Open your browser and navigate to:
`http://localhost:5000`

---

## Running Unit Tests

Execute the test suite using `unittest`:

```bash
python -m unittest -v test_emotion_detection.py
```

Expected Output:
```text
test_emotion_detector_anger (test_emotion_detection.TestEmotionDetection.test_emotion_detector_anger) ... ok
test_emotion_detector_api_400_error (test_emotion_detection.TestEmotionDetection.test_emotion_detector_api_400_error) ... ok
test_emotion_detector_blank_input (test_emotion_detection.TestEmotionDetection.test_emotion_detector_blank_input) ... ok
test_emotion_detector_disgust (test_emotion_detection.TestEmotionDetection.test_emotion_detector_disgust) ... ok
test_emotion_detector_fear (test_emotion_detection.TestEmotionDetection.test_emotion_detector_fear) ... ok
test_emotion_detector_joy (test_emotion_detection.TestEmotionDetection.test_emotion_detector_joy) ... ok
test_emotion_detector_sadness (test_emotion_detection.TestEmotionDetection.test_emotion_detector_sadness) ... ok
test_emotion_detector_blank_text (test_emotion_detection.TestFlaskServer.test_emotion_detector_blank_text) ... ok
test_emotion_detector_valid_text (test_emotion_detection.TestFlaskServer.test_emotion_detector_valid_text) ... ok
test_index_route (test_emotion_detection.TestFlaskServer.test_index_route) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.018s

OK
```

---

## Static Code Analysis (Pylint)

Run `pylint` on all project source files:

```bash
pylint server.py EmotionDetection/emotion_detection.py EmotionDetection/__init__.py emotion_detection.py setup.py test_emotion_detection.py
```

Result:
```text
------------------------------------
Your code has been rated at 10.00/10
```

---

## API Reference

### `GET /emotionDetector?textToAnalyze=<text>`

#### Successful Request Example:
```bash
curl "http://localhost:5000/emotionDetector?textToAnalyze=I%20am%20glad%20this%20happened"
```
**Response (HTTP 200)**:
```text
For the given statement, the system response is 'anger': 0.002, 'disgust': 0.001, 'fear': 0.003, 'joy': 0.98 and 'sadness': 0.004. The dominant emotion is joy.
```

#### Blank / Invalid Input Example:
```bash
curl "http://localhost:5000/emotionDetector?textToAnalyze="
```
**Response (HTTP 400)**:
```text
Invalid text! Please try again!
```

---

## Course Submission Guide

When submitting your Coursera final project assignment:
1. **Task 1**: Screenshot of directory structure / package setup.
2. **Task 2 & 3**: Screenshot of `emotion_detection.py` and formatted output dictionary.
3. **Task 4**: Screenshot of `EmotionDetection/__init__.py` and successful package import in terminal.
4. **Task 5**: Screenshot of `python -m unittest test_emotion_detection.py` showing `OK` (all tests passing).
5. **Task 6**: Screenshot of `server.py` running and web page output for a sample statement.
6. **Task 7**: Screenshot of `server.py` returning HTTP 400 `"Invalid text! Please try again!"` on blank input.
7. **Task 8**: Screenshot of terminal showing `pylint server.py` output with `10.00/10` rating.
