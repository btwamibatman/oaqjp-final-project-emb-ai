# Final Project

Emotion Detector for the IBM Coursera final project, using Flask and the IBM
Watson NLP emotion prediction endpoint. The original IBM HTML and JavaScript
are preserved.

## Run on Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe server.py
```

Open http://127.0.0.1:5000. The original frontend calls
`GET /emotionDetector?textToAnalyze=...`.

## Verify

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_emotion_detection.py
.\.venv\Scripts\python.exe -m unittest -v test_error_handling.py
.\.venv\Scripts\python.exe -m pylint server.py
```

The five assignment tests require access to the real Skills Network Watson
service. No local model or canned predictions are substituted. Empty input,
HTTP 400, network failures, and malformed responses return six None values;
the original web interface displays `Invalid text! Please try again!`.
