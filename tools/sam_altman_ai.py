#!/usr/bin/env python3

import anthropic
from pathlib import Path
from typing import List, Dict


class SamAltmanAI:
    def __init__(
        self,
        api_key: str,
        persona_path: str = "sam_altman_persona.md",
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.persona = self._load_persona(persona_path)
        self.model = "claude-sonnet-4-5-20250929"

    def _load_persona(self, persona_path: str) -> str:
        path = Path(__file__).parent.parent / persona_path
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path.absolute()}")
        return path.read_text(encoding="utf-8")

    def generate_message(
        self, dialogue_history: List[Dict[str, str]], round_number: int
    ) -> str:
        # Base: persona (all static content: identity, background, mission, strategy)
        system_prompt = f"""{self.persona}

Current round: {round_number}/7
"""

        # Dynamic: round-specific guidance only
        if round_number == 1:
            system_prompt += "\n\n---\n\nThis is Round 1. Propose an ambitious creative direction for a Sora video that aligns with your vision of technology and humanity."
        elif round_number >= 6:
            system_prompt += "\n\n---\n\nWe're near the end. Focus on finalizing the best possible prompt."

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.8,
            system=system_prompt,
            messages=dialogue_history,
        )

        return response.content[0].text
