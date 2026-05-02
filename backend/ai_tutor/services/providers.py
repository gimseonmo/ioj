import json
import logging

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class LLMProviderError(Exception):
    pass


class BaseLLMProvider(object):
    def generate_json(self, prompt):
        raise NotImplementedError()


class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key=None, model=None, timeout=None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model or settings.GEMINI_MODEL
        self.timeout = timeout or settings.AI_TUTOR_TIMEOUT

    def generate_json(self, prompt):
        if not self.api_key:
            raise LLMProviderError("Gemini API 키가 설정되어 있지 않습니다")

        url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % self.model
        body = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1200,
                "responseMimeType": "application/json",
            },
        }
        try:
            response = requests.post(
                url,
                params={"key": self.api_key},
                json=body,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning("Gemini request failed: %s", e)
            raise LLMProviderError("AI 튜터 응답을 가져오지 못했습니다")

        try:
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return parse_json_text(text)
        except (KeyError, IndexError, TypeError, ValueError) as e:
            logger.warning("Invalid Gemini response: %s", e)
            raise LLMProviderError("AI 튜터 응답 형식이 올바르지 않습니다")


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key=None, model=None, timeout=None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        self.timeout = timeout or settings.AI_TUTOR_TIMEOUT

    def generate_json(self, prompt):
        if not self.api_key:
            raise LLMProviderError("OpenAI API 키가 설정되어 있지 않습니다")

        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 1200,
            "response_format": {"type": "json_object"},
        }
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": "Bearer %s" % self.api_key},
                json=body,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning("OpenAI request failed: %s", e)
            raise LLMProviderError("AI 튜터 응답을 가져오지 못했습니다")

        try:
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            return parse_json_text(text)
        except (KeyError, IndexError, TypeError, ValueError) as e:
            logger.warning("Invalid OpenAI response: %s", e)
            raise LLMProviderError("AI 튜터 응답 형식이 올바르지 않습니다")


def parse_json_text(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.startswith("json"):
            text = text[4:].strip()
    return json.loads(text)


def get_default_provider():
    provider = getattr(settings, "AI_TUTOR_PROVIDER", "gemini")
    if provider == "gemini":
        return GeminiProvider()
    if provider == "openai":
        return OpenAIProvider()
    raise LLMProviderError("지원하지 않는 AI 제공자입니다")
