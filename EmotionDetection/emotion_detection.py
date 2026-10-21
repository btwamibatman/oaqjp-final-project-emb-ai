"""Detect emotions with the IBM Watson NLP service used by Skills Network."""

import logging

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")
LOGGER = logging.getLogger(__name__)


def emotion_detector(text_to_analyse):
    """Return five Watson scores and their maximum, or None values on failure."""
    invalid_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not isinstance(text_to_analyse, str) or not text_to_analyse.strip():
        return invalid_result

    try:
        response = requests.post(
            URL,
            json={"raw_document": {"text": text_to_analyse}},
            headers=HEADERS,
            timeout=(10, 30),
        )
        if response.status_code == 400:
            return invalid_result
        response.raise_for_status()
        scores = response.json()["emotionPredictions"][0]["emotion"]
        result = {emotion: float(scores[emotion]) for emotion in EMOTIONS}
        result["dominant_emotion"] = max(result, key=result.get)
        return result
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as error:
        LOGGER.warning("Watson emotion prediction failed: %s", error)
        return invalid_result
