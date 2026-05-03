"""
services/ai_service.py
AI integration via the OpenRouter API.
Loads environment variables once at module level (not per-request).
"""

import os
import requests
import json
from typing import Optional
from dotenv import load_dotenv
from config.settings import OPENROUTER_API_URL
from utils.logger import setup_logger

# Load once at import time
load_dotenv(override=True)

logger = setup_logger("AIService")


class AIService:
    """Handles all AI-powered note operations through OpenRouter."""

    @staticmethod
    def _get_credentials() -> tuple:
        """Read API key and model from environment. Re-reads .env for live updates."""
        load_dotenv(override=True)
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku").strip()
        return api_key, model

    @staticmethod
    def _make_request(system_prompt: str, user_content: str) -> Optional[str]:
        """Send a chat completion request to OpenRouter."""
        api_key, model_name = AIService._get_credentials()

        if not api_key:
            logger.error("OpenRouter API key is missing.")
            raise ValueError("API key is not configured. Go to Settings to add it.")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/",
            "X-Title": "AI Notes App",
        }

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        }

        try:
            response = requests.post(
                OPENROUTER_API_URL,
                headers=headers,
                data=json.dumps(payload),
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            raise ValueError("The AI request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ValueError(f"Network error: {e}")
        except (KeyError, IndexError) as e:
            logger.error(f"Unexpected API response format: {e}")
            raise ValueError("Received an unexpected response from the AI.")

    # ── Public AI Actions ────────────────────────────────────────────────────

    @staticmethod
    def summarize_note(content: str) -> str:
        """Generate a concise summary of the note."""
        prompt = (
            "You are a helpful assistant that summarizes notes. "
            "Provide a concise, bulleted summary of the following note. "
            "IMPORTANT: Do not use any markdown formatting. Use plain text only. "
            "Do not use asterisks (*) or bold text."
        )
        return AIService._make_request(prompt, content)

    @staticmethod
    def generate_title(content: str) -> str:
        """Generate a short catchy title for the note."""
        prompt = (
            "Generate a short, catchy title (max 6 words) for the following note content. "
            "Only output the title, nothing else. Do not use quotes or markdown."
        )
        return AIService._make_request(prompt, content)

    @staticmethod
    def explain_note(content: str) -> str:
        """Explain note concepts in beginner-friendly language."""
        prompt = (
            "Explain the concepts in the following note in simple terms, "
            "as if explaining to a beginner. "
            "IMPORTANT: Do not use any markdown formatting. Use plain text only."
        )
        return AIService._make_request(prompt, content)

    @staticmethod
    def generate_study_questions(content: str) -> str:
        """Generate study questions from the note content."""
        prompt = (
            "Generate 3-5 study questions based on the following note to test understanding. "
            "IMPORTANT: Do not use any markdown formatting. Use plain text only."
        )
        return AIService._make_request(prompt, content)

    @staticmethod
    def simplify_note(content: str) -> str:
        """Rewrite the note in simpler, clearer language."""
        prompt = (
            "Rewrite the following note in simpler, clearer language. "
            "Keep the same meaning but make it easier to understand. "
            "IMPORTANT: Do not use any markdown formatting. Use plain text only."
        )
        return AIService._make_request(prompt, content)
