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
        self,
        dialogue_history: List[Dict[str, str]],
        round_number: int,
        max_rounds: int = 5,
        stream: bool = False,
    ):
        """
        Generate Sam Altman AI's response.

        Args:
            dialogue_history: List of previous messages
            round_number: Current round number
            max_rounds: Maximum number of rounds (default: 5)
            stream: If True, returns a generator for streaming; if False, returns string

        Returns:
            str if stream=False, generator if stream=True
        """
        # Base: persona (all static content: identity, background, mission, strategy)
        system_prompt = f"""{self.persona}

Current round: {round_number}/{max_rounds}
"""

        # Dynamic: round-specific guidance only
        if round_number == 1:
            system_prompt += "\n\n---\n\nThis is Round 1. Share your creative direction for the Sora video."
        elif round_number >= max_rounds - 1:
            system_prompt += "\n\n---\n\nWe're approaching the final round. Consider whether you're ready to approve a final prompt."

        if stream:
            # Return generator for streaming
            with self.client.messages.stream(
                model=self.model,
                max_tokens=2000,
                temperature=0.8,
                system=system_prompt,
                messages=dialogue_history,
            ) as stream:
                for text in stream.text_stream:
                    yield text
        else:
            # Return complete string (original behavior)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.8,
                system=system_prompt,
                messages=dialogue_history,
            )
            return response.content[0].text
