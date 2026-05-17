"""
AI Service Layer
Generates actionable insights from GA4 data using Anthropic's Claude API.
"""

import json
import logging
from typing import List, Dict, Any
from anthropic import Anthropic

from app.config.settings import settings
from app.schemas.analytics import AIInsight

logger = logging.getLogger(__name__)

# Prompt for Claude
SYSTEM_PROMPT = """
You are an expert Google Analytics 4 data analyst.
You will be provided with raw JSON data representing website traffic, devices, and top pages over a certain period.
Your job is to analyze this data and generate 4 concise, actionable insights.

Each insight must be categorized as:
- 'positive': for growth or good metrics
- 'warning': for high bounce rates, drops in traffic, etc.
- 'info': for interesting patterns (peak hours, etc.)
- 'action': a recommendation based on the data

You must return EXACTLY 4 insights in the following JSON format, and NOTHING ELSE:
[
  {
    "id": "1",
    "title": "Short title",
    "description": "1-2 sentence explanation",
    "type": "positive|warning|info|action",
    "metric": "Key number (e.g. +23%)",
    "change": "Context (e.g. vs last week)"
  }
]
"""

class AIService:
    def __init__(self):
        self.api_key = getattr(settings, "ANTHROPIC_API_KEY", None)
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None

    def generate_insights(self, overview: Any, traffic: List[Any], devices: List[Any], top_pages: List[Any]) -> List[AIInsight]:
        """
        Sends the GA4 data to Claude to generate insights.
        """
        if not self.client:
            logger.warning("No Anthropic API Key found. Returning default insights.")
            raise ValueError("ANTHROPIC_API_KEY is missing.")

        # Serialize data for the prompt
        data_context = {
            "overview": overview.model_dump() if hasattr(overview, "model_dump") else overview,
            "traffic": [t.model_dump() if hasattr(t, "model_dump") else t for t in traffic],
            "devices": [d.model_dump() if hasattr(d, "model_dump") else d for d in devices],
            "top_pages": [p.model_dump() if hasattr(p, "model_dump") else p for p in top_pages],
        }

        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.2,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": f"Here is the GA4 data:\n```json\n{json.dumps(data_context, indent=2)}\n```\nGenerate the JSON insights array."
                    }
                ]
            )

            # Claude's response is in response.content[0].text
            raw_text = response.content[0].text
            
            # Extract JSON array from text (in case Claude wraps it in backticks)
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()

            insights_data = json.loads(raw_text)
            
            # Convert to Pydantic models
            return [AIInsight(**insight) for insight in insights_data]

        except Exception as e:
            logger.error(f"Failed to generate AI insights: {e}")
            raise e

ai_service = AIService()
