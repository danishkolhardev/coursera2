"""
Root emotion_detection module for direct execution and backward compatibility.
"""
from EmotionDetection.emotion_detection import emotion_detector

__all__ = ['emotion_detector']

if __name__ == '__main__':
    sample_text = "I love this new application!"
    result = emotion_detector(sample_text)
    print(f"Emotion detection result for '{sample_text}':")
    print(result)
