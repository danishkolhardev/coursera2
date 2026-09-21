"""
Setup configuration for the EmotionDetection package.
"""
from setuptools import setup, find_packages

setup(
    name="EmotionDetection",
    version="1.0.0",
    description="AI-powered emotion detection package using IBM Watson NLP",
    author="Danish Kolhar",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
)
