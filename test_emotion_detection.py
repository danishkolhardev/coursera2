"""
Unit tests for the EmotionDetection package and Flask server.
"""
import unittest
from unittest.mock import patch, MagicMock
from EmotionDetection.emotion_detection import emotion_detector
from server import app


def create_mock_response(status_code, emotions_data=None):
    """Helper function to create mock Watson API response."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    if emotions_data is not None:
        mock_resp.text = f'''{{
            "emotionPredictions": [
                {{
                    "emotion": {{
                        "anger": {emotions_data.get("anger", 0.0)},
                        "disgust": {emotions_data.get("disgust", 0.0)},
                        "fear": {emotions_data.get("fear", 0.0)},
                        "joy": {emotions_data.get("joy", 0.0)},
                        "sadness": {emotions_data.get("sadness", 0.0)}
                    }},
                    "target": ""
                }}
            ],
            "producerId": {{"name": "Emotion Workflow", "version": "0.0.1"}}
        }}'''
    else:
        mock_resp.text = '{"error": "Bad Request"}'
    return mock_resp


class TestEmotionDetection(unittest.TestCase):
    """Test suite for the emotion_detector function."""

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_joy(self, mock_post):
        """Test statement expressing joy."""
        mock_post.return_value = create_mock_response(200, {
            "anger": 0.002,
            "disgust": 0.001,
            "fear": 0.003,
            "joy": 0.98,
            "sadness": 0.004
        })
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result['dominant_emotion'], 'joy')
        self.assertAlmostEqual(result['joy'], 0.98)

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_anger(self, mock_post):
        """Test statement expressing anger."""
        mock_post.return_value = create_mock_response(200, {
            "anger": 0.95,
            "disgust": 0.02,
            "fear": 0.01,
            "joy": 0.01,
            "sadness": 0.01
        })
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result['dominant_emotion'], 'anger')
        self.assertAlmostEqual(result['anger'], 0.95)

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_disgust(self, mock_post):
        """Test statement expressing disgust."""
        mock_post.return_value = create_mock_response(200, {
            "anger": 0.02,
            "disgust": 0.94,
            "fear": 0.01,
            "joy": 0.01,
            "sadness": 0.02
        })
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result['dominant_emotion'], 'disgust')
        self.assertAlmostEqual(result['disgust'], 0.94)

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_sadness(self, mock_post):
        """Test statement expressing sadness."""
        mock_post.return_value = create_mock_response(200, {
            "anger": 0.01,
            "disgust": 0.01,
            "fear": 0.02,
            "joy": 0.01,
            "sadness": 0.95
        })
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result['dominant_emotion'], 'sadness')
        self.assertAlmostEqual(result['sadness'], 0.95)

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_fear(self, mock_post):
        """Test statement expressing fear."""
        mock_post.return_value = create_mock_response(200, {
            "anger": 0.01,
            "disgust": 0.01,
            "fear": 0.96,
            "joy": 0.01,
            "sadness": 0.01
        })
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result['dominant_emotion'], 'fear')
        self.assertAlmostEqual(result['fear'], 0.96)

    def test_emotion_detector_blank_input(self):
        """Test blank string input returns None for all emotions."""
        result = emotion_detector("")
        self.assertIsNone(result['dominant_emotion'])
        self.assertIsNone(result['anger'])
        self.assertIsNone(result['joy'])

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_api_400_error(self, mock_post):
        """Test API returning 400 error returns None for all emotions."""
        mock_post.return_value = create_mock_response(400)
        result = emotion_detector("some input")
        self.assertIsNone(result['dominant_emotion'])


class TestFlaskServer(unittest.TestCase):
    """Test suite for the Flask server routes and error handling."""

    def setUp(self):
        """Set up Flask test client."""
        self.client = app.test_client()

    def test_index_route(self):
        """Test that the index route returns status 200 and loads HTML."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI Emotion Detector', response.data)

    def test_emotion_detector_blank_text(self):
        """Test emotion detector endpoint with blank text returns 400."""
        response = self.client.get('/emotionDetector?textToAnalyze=')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'Invalid text! Please try again!')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_valid_text(self, mock_post):
        """Test emotion detector endpoint with valid text returns formatted string."""
        mock_post.return_value = create_mock_response(200, {
            "anger": 0.01,
            "disgust": 0.02,
            "fear": 0.03,
            "joy": 0.90,
            "sadness": 0.04
        })
        response = self.client.get('/emotionDetector?textToAnalyze=I%20love%20Python')
        self.assertEqual(response.status_code, 200)
        expected_substring = "The dominant emotion is joy."
        self.assertIn(expected_substring, response.data.decode())


if __name__ == '__main__':
    unittest.main()
