import hashlib
import json

from django.conf import settings

from utils.cache import cache

from .prompts import build_ai_tutor_prompt
from .providers import get_default_provider


class AITutorService(object):
    def __init__(self, provider=None):
        self.provider = provider or get_default_provider()

    def generate(self, user, problem, code, error_log=""):
        self._check_rate_limit(user)
        cache_key = self._cache_key(problem, code, error_log)
        cached = cache.get(cache_key)
        if cached:
            return cached

        prompt = build_ai_tutor_prompt(problem, code, error_log)
        result = self.provider.generate_json(prompt)
        result = self._normalize_result(result)
        cache.set(cache_key, result, settings.AI_TUTOR_CACHE_SECONDS)
        return result

    def _normalize_result(self, result):
        if not isinstance(result, dict):
            result = {}

        bug_analysis = result.get("bug_analysis") or "분석 결과를 생성하지 못했습니다."
        test_cases = result.get("test_cases") or []
        steps = result.get("steps") or []

        if not isinstance(test_cases, list):
            test_cases = [str(test_cases)]
        if not isinstance(steps, list):
            steps = [str(steps)]

        return {
            "bug_analysis": str(bug_analysis),
            "test_cases": [str(item) for item in test_cases[:10]],
            "steps": [str(item) for item in steps[:8]],
        }

    def _cache_key(self, problem, code, error_log):
        raw = json.dumps(
            {
                "problem": problem,
                "code": code,
                "error_log": error_log or "",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return "ai_tutor:response:%s" % digest

    def _check_rate_limit(self, user):
        user_id = getattr(user, "id", None) or "anonymous"
        key = "ai_tutor:rate:%s" % user_id
        current = cache.get(key) or 0
        if int(current) >= settings.AI_TUTOR_RATE_LIMIT:
            raise ValueError("AI 튜터 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
        cache.set(key, int(current) + 1, settings.AI_TUTOR_RATE_WINDOW_SECONDS)

