#!/usr/bin/env python3

from pathlib import Path


class SoraCopilot:
    def __init__(
        self,
        prompts_db_path: str = "sora_top_prompts.md",
        persona_path: str = "sora_copilot_persona.md",
        model: str = "claude-haiku-4-5-20251001",  # Agent layer: currently Haiku, can upgrade to Sonnet
    ):
        self.prompts_db = self._load_prompts_db(prompts_db_path)
        self.persona = self._load_persona(persona_path)
        self.model = model

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
            dynamic_text = """

---

CRITICAL: This is the final round. You MUST deliver the approved prompt using this exact format:

<final_prompt>
[Pure prompt text only - no explanations, no formatting, no markdown]
</final_prompt>

The <final_prompt> XML tags are MANDATORY for extraction. Do not forget them."""

        if dynamic_text:
            system_blocks.append({"type": "text", "text": dynamic_text})

        return system_blocks
