"""
Astra AI - LLM Integration Client
Supports OpenAI (GPT-4o, GPT-4o-mini), Google Gemini (Gemini 1.5 Flash), and Groq.
Grounded with live database context and regulatory knowledge base citations.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
import httpx

logger = logging.getLogger("astra_ai.llm")

class LLMClient:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE API KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.preferred_provider = os.getenv("LLM_PROVIDER", "auto").lower()

    def is_configured(self) -> bool:
        """Returns True if at least one valid LLM API key is present."""
        return bool(self.openai_api_key or self.gemini_api_key or self.groq_api_key)

    def get_active_provider(self) -> Optional[str]:
        if self.preferred_provider == "openai" and self.openai_api_key:
            return "openai"
        if self.preferred_provider == "gemini" and self.gemini_api_key:
            return "gemini"
        if self.preferred_provider == "groq" and self.groq_api_key:
            return "groq"
        
        # Auto-detect in order of availability
        if self.openai_api_key and not self.openai_api_key.startswith("sk-placeholder"):
            return "openai"
        if self.gemini_api_key and not self.gemini_api_key.startswith("AIzaSy-placeholder"):
            return "gemini"
        if self.groq_api_key:
            return "groq"
        return None

    def generate_response(
        self,
        query: str,
        retrieved_context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Sends the user query and database RAG context to the active LLM provider.
        Returns the generated natural language reasoning, or None if LLM is unavailable.
        """
        provider = self.get_active_provider()
        if not provider:
            logger.info("No active LLM API key configured. Using deterministic compliance engine.")
            return None

        system_prompt = (
            "You are Astra AI, an elite Enterprise Risk, Fraud & Regulatory Intelligence Copilot. "
            "You assist compliance officers, fraud investigators, and risk analysts in auditing financial "
            "transactions, assessing customer risk scores, detecting AML/CFT anomalies, and correlating "
            "actions against RBI, PMLA, FATF, and Basel III regulatory frameworks.\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. Ground all your reasoning strictly in the provided Context Data. Do NOT hallucinate transaction amounts, dates, or IDs.\n"
            "2. Always cite specific rule names, risk points (+X pts), and regulatory documents when referencing flags.\n"
            "3. Use professional, concise, structured markdown with bullet points, bold highlights, and clear actionable takeaways.\n"
            "4. Maintain an objective, authoritative compliance audit tone."
        )

        user_content = f"Query: {query}\n\nContext Data:\n{json.dumps(retrieved_context, indent=2, default=str)}"

        try:
            if provider == "openai":
                return self._call_openai(system_prompt, user_content)
            elif provider == "gemini":
                return self._call_gemini(system_prompt, user_content)
            elif provider == "groq":
                return self._call_groq(system_prompt, user_content)
        except Exception as e:
            logger.error(f"Error calling {provider} LLM API: {e}")
            return None

        return None

    def _call_openai(self, system_prompt: str, user_content: str) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.2,
            "max_tokens": 1000
        }
        with httpx.Client(timeout=20.0) as client:
            resp = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenAI error {resp.status_code}: {resp.text}")
                return None

    def _call_gemini(self, system_prompt: str, user_content: str) -> Optional[str]:
        preferred_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        candidate_models = [preferred_model, "gemini-2.5-flash", "gemini-flash-latest", "gemini-3.5-flash"]

        payload = {
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "parts": [{"text": user_content}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1000
            }
        }

        with httpx.Client(timeout=25.0) as client:
            for model in candidate_models:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_api_key}"
                try:
                    resp = client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates and "content" in candidates[0]:
                            parts = candidates[0]["content"].get("parts", [])
                            if parts:
                                return parts[0].get("text", "")
                    else:
                        logger.warning(f"Gemini {model} returned {resp.status_code}: {resp.text[:100]}")
                except Exception as e:
                    logger.warning(f"Error attempting Gemini model {model}: {e}")
                    continue
        return None

    def _call_groq(self, system_prompt: str, user_content: str) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.2,
            "max_tokens": 1000
        }
        with httpx.Client(timeout=20.0) as client:
            resp = client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"Groq error {resp.status_code}: {resp.text}")
                return None

llm_client = LLMClient()
