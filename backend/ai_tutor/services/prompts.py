import json


def build_ai_tutor_prompt(problem, code, error_log=""):
    payload = {
        "problem": problem,
        "code": code,
        "error_log": error_log or "",
    }
    return (
        "You are an AI tutor for an Online Judge coding platform. "
        "Return only valid JSON with these exact keys: bug_analysis, test_cases, steps. "
        "bug_analysis must explain likely bugs, exact code locations when visible, and why they fail. "
        "test_cases must be an array of concise hidden edge-case inputs or descriptions covering minimum, maximum, boundary, and tricky patterns. "
        "steps must be an array of 5 concise tutoring steps: understand problem, choose data structure, choose algorithm, pseudocode design, implementation guidance. "
        "Do not provide full solution code unless the user's code already reveals that implementation direction. "
        "Use Korean for all user-facing text. "
        "Input JSON follows:\n"
        f"{json.dumps(payload, ensure_ascii=False)}"
    )

