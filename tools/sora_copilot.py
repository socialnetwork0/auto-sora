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

    def get_system_prompt(self, round_number: int = 0, max_rounds: int = 7) -> str:
        # Base: persona + prompts database
        system_prompt = self.persona
        system_prompt += "\n\n---\n\n"
        system_prompt += self.prompts_db

        # Dynamic: round-specific guidance only
        if round_number == 0:
            system_prompt += "\n\n---\n\nThis is the opening. Greet Sam warmly and ask about his vision."
        elif round_number >= max_rounds - 2:
            system_prompt += "\n\n---\n\nWe're approaching the end. Focus on delivering the final prompt(s)."

        return system_prompt
