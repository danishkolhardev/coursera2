"""
Emotion Detection module using IBM Watson NLP service.
"""
import json
import requests


def emotion_detector(text_to_analyze):
    """
    Detect emotions in the given text using IBM Watson NLP Emotion Detection API.

    Args:
        text_to_analyze (str): Text string to analyze for emotions.

    Returns:
        dict: Dictionary containing emotion scores ('anger', 'disgust', 'fear',
              'joy', 'sadness') and the 'dominant_emotion'.
              Returns all values as None if input is blank or on error (status code 400).
    """
    url = (
        'https://sn-watson-emotion.labs.skills.network/'
        'v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    # Default return structure for invalid/blank input
    default_response = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

    # Handle blank or invalid input before sending request
    if not text_to_analyze or not str(text_to_analyze).strip():
        return default_response

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        return default_response

    # If status code is 400 or other client/server error, return None values
    if response.status_code == 400:
        return default_response

    if response.status_code != 200:
        return default_response

    formatted_response = json.loads(response.text)

    # Check if emotionPredictions exists and is non-empty
    if (
        'emotionPredictions' in formatted_response
        and len(formatted_response['emotionPredictions']) > 0
    ):
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        anger_score = emotions.get('anger', 0.0)
        disgust_score = emotions.get('disgust', 0.0)
        fear_score = emotions.get('fear', 0.0)
        joy_score = emotions.get('joy', 0.0)
        sadness_score = emotions.get('sadness', 0.0)

        emotion_dict = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }

        dominant_emotion = max(emotion_dict, key=emotion_dict.get)

        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }

    return default_response
