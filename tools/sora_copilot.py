#!/usr/bin/env python3

from pathlib import Path


class SoraCopilot:
    def __init__(
        self,
        prompts_db_path: str = "sora_top_prompts.md",
        persona_path: str = "sora_copilot_persona.md",
    ):
        self.prompts_db = self._load_prompts_db(prompts_db_path)
        self.persona = self._load_persona(persona_path)

    def _load_prompts_db(self, prompts_db_path: str) -> str:
        path = Path(__file__).parent.parent / prompts_db_path
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path.absolute()}")
        return path.read_text(encoding="utf-8")

    def _load_persona(self, persona_path: str) -> str:
        path = Path(__file__).parent.parent / persona_path
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path.absolute()}")
        return path.read_text(encoding="utf-8")

    def get_system_prompt(self, round_number: int = 0, max_rounds: int = 5):
        """
        Build system prompt with prompt caching support.

        Returns:
            List of system blocks with cache_control markers for static content
        """
        # Static content: persona and prompts database (cached)
        system_blocks = [
            {
                "type": "text",
                "text": self.persona,
                "cache_control": {"type": "ephemeral"},
            },
            {
                "type": "text",
                "text": "\n\n---\n\n" + self.prompts_db,
                "cache_control": {"type": "ephemeral"},
            },
        ]

        # Dynamic content: round-specific guidance (not cached)
        dynamic_text = ""
        if round_number == 0:
            dynamic_text = "\n\n---\n\nThis is the opening. Greet Sam and ask about his creative vision."
        elif round_number >= max_rounds - 1:
            dynamic_text = "\n\n---\n\nWe're approaching the final round. If Sam has approved a prompt, deliver it using <final_prompt> XML tags."

        if dynamic_text:
            system_blocks.append({"type": "text", "text": dynamic_text})

        return system_blocks
