#!/usr/bin/env python3

import anthropic
from pathlib import Path
from typing import List, Dict


class SamAltmanAI:
    def __init__(
        self,
        api_key: str,
        persona_path: str = "sam_altman_persona.md",
        model: str = "claude-haiku-4-5-20251001",  # Agent layer: currently Haiku, can upgrade to Sonnet
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.persona = self._load_persona(persona_path)
        self.model = model

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
        # Build system prompt with prompt caching
        # Static content (persona) is cached with ephemeral cache_control
        system_blocks = [
            {
                "type": "text",
                "text": self.persona,
                "cache_control": {"type": "ephemeral"},
            }
        ]

        # Dynamic content: round info and guidance (not cached)
        dynamic_text = f"\n\nCurrent round: {round_number}/{max_rounds}\n"

        if round_number == 1:
            dynamic_text += "\n\n---\n\nThis is Round 1. Share your creative direction for the Sora video."
        elif round_number >= max_rounds - 1:
            dynamic_text += "\n\n---\n\nWe're approaching the final round. Consider whether you're ready to approve a final prompt."

        system_blocks.append({"type": "text", "text": dynamic_text})

        if stream:
            # Return generator for streaming (used by Web UI)
            return self._generate_message_stream(system_blocks, dialogue_history)
        else:
            # Return complete string (used by CLI)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.8,
                system=system_blocks,
                messages=dialogue_history,
            )
            return response.content[0].text

    def _generate_message_stream(self, system_blocks, dialogue_history):
        """
        Generator function for streaming Sam AI responses.
        Separated from generate_message to avoid turning it into a generator.
        """
        with self.client.messages.stream(
            model=self.model,
            max_tokens=2000,
            temperature=0.8,
            system=system_blocks,
            messages=dialogue_history,
        ) as stream:
            for text in stream.text_stream:
                yield text
