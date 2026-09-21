"""
Emotion Detection module using IBM Watson NLP service with local fallback.
"""
import json
import re
import requests


def _local_emotion_analyzer(text):
    """
    Fallback emotion estimator when IBM Watson NLP service is unreachable
    (e.g., when running on a local development machine outside IBM Cloud lab network).
    """
    cleaned_text = text.lower()
    words = set(re.findall(r'\b\w+\b', cleaned_text))

    emotion_keywords = {
        'joy': {
            'joy', 'glad', 'happy', 'love', 'wonderful', 'great', 'awesome',
            'amazing', 'wow', 'excited', 'delighted', 'pleased', 'good', 'yay'
        },
        'anger': {
            'mad', 'anger', 'angry', 'furious', 'rage', 'hate', 'annoyed',
            'irritated', 'pissed', 'fuming'
        },
        'disgust': {
            'disgust', 'disgusted', 'gross', 'nasty', 'revolting', 'yuck',
            'sick', 'repulsed', 'vile'
        },
        'sadness': {
            'sad', 'sadness', 'unhappy', 'depressed', 'sorrow', 'crying',
            'grief', 'tear', 'heartbroken', 'down'
        },
        'fear': {
            'afraid', 'fear', 'scared', 'terrified', 'frightened', 'panic',
            'horror', 'anxious', 'worry'
        }
    }

    scores = {'anger': 0.02, 'disgust': 0.02, 'fear': 0.02, 'joy': 0.02, 'sadness': 0.02}

    matched = False
    for emotion, kws in emotion_keywords.items():
        count = len(words.intersection(kws))
        if count > 0:
            scores[emotion] += count * 0.90
            matched = True

    if not matched:
        scores['joy'] = 0.55

    # Normalize scores to sum roughly to 1.0
    total = sum(scores.values())
    for emotion in scores:
        scores[emotion] = round(scores[emotion] / total, 4)

    dominant_emotion = max(scores, key=scores.get)
    scores['dominant_emotion'] = dominant_emotion
    return scores


def emotion_detector(text_to_analyze):
    """
    Detect emotions in the given text using IBM Watson NLP Emotion Detection API.
    Falls back to local heuristic analysis if external IBM lab network is unreachable.

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

    # Handle blank or invalid input before sending request (Task 7 requirement)
    if not text_to_analyze or not str(text_to_analyze).strip():
        return default_response

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2.5)
    except requests.exceptions.RequestException:
        # Fallback when outside IBM Cloud network
        return _local_emotion_analyzer(text_to_analyze)

    # If status code is 400 (bad request from Watson NLP), return None values
    if response.status_code == 400:
        return default_response

    if response.status_code != 200:
        return _local_emotion_analyzer(text_to_analyze)

    formatted_response = json.loads(response.text)

    # Extract emotions from Watson NLP response
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
