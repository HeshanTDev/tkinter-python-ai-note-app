import os
import requests
import json
from typing import Optional
from dotenv import load_dotenv
from config.settings import OPENROUTER_API_URL
from utils.logger import setup_logger

logger = setup_logger("AIService")

class AIService:
    @staticmethod
    def _make_request(system_prompt: str, user_content: str) -> Optional[str]:
        load_dotenv(override=True)
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        model_name = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku").strip()

        if not api_key:
            logger.error("OpenRouter API key is missing.")
            raise ValueError("API key is not configured in the .env file.")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/",
            "X-Title": "AI Notes App"
        }

        data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        }

        try:
            response = requests.post(OPENROUTER_API_URL, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ValueError(f"Network error or invalid API key: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    @staticmethod
    def summarize_note(content: str) -> str:
        prompt = "You are a helpful assistant that summarizes notes. Provide a concise, bulleted summary of the following note. IMPORTANT: Do not use any markdown formatting whatsoever. Use plain text only. Do not use asterisks (*) or bold text."
        return AIService._make_request(prompt, content)

    @staticmethod
    def generate_title(content: str) -> str:
        prompt = "Generate a short, catchy title (max 6 words) for the following note content. Only output the title, nothing else. Do not use quotes or any markdown formatting."
        return AIService._make_request(prompt, content)

    @staticmethod
    def explain_note(content: str) -> str:
        prompt = "Explain the concepts in the following note in simple terms, as if explaining to a beginner. IMPORTANT: Do not use any markdown formatting whatsoever. Use plain text only. Do not use asterisks (*) or bold text."
        return AIService._make_request(prompt, content)

    @staticmethod
    def generate_study_questions(content: str) -> str:
        prompt = "Generate 3-5 study questions based on the following note to test understanding. IMPORTANT: Do not use any markdown formatting whatsoever. Use plain text only. Do not use asterisks (*) or bold text."
        return AIService._make_request(prompt, content)
