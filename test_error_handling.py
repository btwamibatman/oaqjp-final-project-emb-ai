"""Local contract tests; mocked results are not live Watson evidence."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection import emotion_detector
from EmotionDetection.emotion_detection import HEADERS, URL
from server import app

EMPTY_RESULT = dict.fromkeys(("anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"))
SCORES = {"anger": 0.01, "disgust": 0.02, "fear": 0.03, "joy": 0.9, "sadness": 0.04}


class TestLocalContracts(unittest.TestCase):
    """Verify parsing, transport failures, and the original Flask contract."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_format_and_request_contract(self, post):
        response = Mock(status_code=200)
        response.json.return_value = {"emotionPredictions": [{"emotion": SCORES}]}
        post.return_value = response
        self.assertEqual(emotion_detector("example"), {**SCORES, "dominant_emotion": "joy"})
        post.assert_called_once_with(
            URL, json={"raw_document": {"text": "example"}}, headers=HEADERS, timeout=(10, 30)
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400(self, post):
        post.return_value.status_code = 400
        self.assertEqual(emotion_detector("example"), EMPTY_RESULT)
        post.return_value.json.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_invalid_inputs(self, post):
        for value in ("", " \t\n", None, 123):
            with self.subTest(value=value):
                self.assertEqual(emotion_detector(value), EMPTY_RESULT)
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_timeout(self, post):
        post.side_effect = requests.Timeout("Mocked timeout")
        self.assertEqual(emotion_detector("example"), EMPTY_RESULT)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_500(self, post):
        post.return_value.status_code = 500
        post.return_value.raise_for_status.side_effect = requests.HTTPError("Mocked HTTP 500")
        self.assertEqual(emotion_detector("example"), EMPTY_RESULT)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_malformed_responses(self, post):
        post.return_value.status_code = 200
        for payload in ({}, {"emotionPredictions": []}, {"emotionPredictions": [{"emotion": {}}]}):
            with self.subTest(payload=payload):
                post.return_value.json.return_value = payload
                self.assertEqual(emotion_detector("example"), EMPTY_RESULT)

    def test_frontend(self):
        with app.test_client() as client:
            self.assertIn(b"textToAnalyze", client.get("/").data)
            with client.get("/static/mywebscript.js") as response:
                self.assertEqual(response.status_code, 200)

    @patch("server.emotion_detector")
    def test_blank_web_input(self, detector):
        with app.test_client() as client:
            for query in ({}, {"textToAnalyze": ""}, {"textToAnalyze": "   "}):
                response = client.get("/emotionDetector", query_string=query)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.text, "Invalid text! Please try again!")
        detector.assert_not_called()

    @patch("server.emotion_detector", return_value={**SCORES, "dominant_emotion": "joy"})
    def test_valid_web_contract(self, detector):
        with app.test_client() as client:
            response = client.get("/emotionDetector", query_string={"textToAnalyze": "example"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.text,
                "For the given statement, the system response is 'anger': 0.01, "
                "'disgust': 0.02, 'fear': 0.03, 'joy': 0.9, 'sadness': 0.04. "
                "The dominant emotion is joy.",
            )
        detector.assert_called_once_with("example")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_web(self, post):
        post.return_value.status_code = 400
        with app.test_client() as client:
            response = client.get("/emotionDetector", query_string={"textToAnalyze": "example"})
            self.assertEqual(response.text, "Invalid text! Please try again!")


if __name__ == "__main__":
    unittest.main()
