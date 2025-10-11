#!/usr/bin/env python3
"""
Sam Altman AI - Autonomous persona-driven message generator.

This module generates Sam Altman-style messages for autonomous dialogue.
"""

import anthropic
from pathlib import Path
from typing import List, Dict


class SamAltmanAI:
    """AI that generates messages in Sam Altman's style."""

    def __init__(
        self,
        api_key: str,
        persona_path: str = "sam_altman_persona.md",
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.persona = self._load_persona(persona_path)
        self.model = "claude-sonnet-4-5-20250929"

    def _load_persona(self, persona_path: str) -> str:
        """Load Sam Altman persona from markdown file."""
        path = Path(persona_path)
        if not path.exists():
            # Try relative to project root
            path = Path(__file__).parent.parent / persona_path

        if not path.exists():
            error_msg = f"❌ ERROR: Persona file not found: {persona_path}"
            print(error_msg)
            print(f"   Tried paths:")
            print(f"   1. {Path(persona_path).absolute()}")
            print(f"   2. {path.absolute()}")
            raise FileNotFoundError(error_msg)

        # Load persona
        persona_content = path.read_text(encoding="utf-8")
        abs_path = path.absolute()

        print(f"✅ Persona loaded: {abs_path}")
        print(f"   Size: {len(persona_content)} characters")
        print(f"   Lines: {len(persona_content.splitlines())} lines\n")

        return persona_content

    def generate_message(
        self, dialogue_history: List[Dict[str, str]], round_number: int
    ) -> str:
        """
        Generate Sam Altman's next message based on dialogue history.

        Args:
            dialogue_history: List of {role: str, content: str} messages
            round_number: Current round number (1-7)

        Returns:
            Generated message content
        """
        # Build system prompt with persona
        system_prompt = f"""You are Sam Altman, CEO of OpenAI. You are having an autonomous dialogue with a Sora Creator Copilot to generate an exceptional Sora video prompt.

{self.persona}

Your goal in this dialogue:
- Round 1-2: Propose a visionary, strategic creative direction for a Sora video
- Round 3-4: Provide specific details, visual preferences, and context
- Round 5-6: Refine and confirm the direction, suggest final adjustments
- Round 7: Make final selection or request the ultimate version

Communication style:
- Be deliberate, strategic, and concise
- Think long-term, not just viral
- Focus on civilization-scale narratives or profound human moments
- Reference technology, progress, and human potential
- Keep responses under 150 words unless elaborating on vision

Current round: {round_number}/7
"""

        # Add context based on round
        if round_number == 1:
            system_prompt += "\n\nThis is Round 1. Propose an ambitious creative direction for a Sora video that aligns with your vision of technology and humanity."
        elif round_number >= 6:
            system_prompt += (
                "\n\nWe're near the end. Focus on finalizing the best possible prompt."
            )

        # Generate response
        try:
            # Transform dialogue_history for Sam's perspective:
            # In autonomous_sora_chat: user=Sam, assistant=Copilot
            # For Sam AI's API call: user=Copilot (what Sam hears), assistant=Sam (what Sam said)
            # So we need to flip all roles
            api_messages = []
            for msg in dialogue_history:
                flipped_msg = msg.copy()
                # Flip roles: user ↔ assistant
                if msg["role"] == "user":
                    flipped_msg["role"] = "assistant"  # Sam's previous messages
                elif msg["role"] == "assistant":
                    flipped_msg["role"] = "user"  # Copilot's messages
                api_messages.append(flipped_msg)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.8,
                system=system_prompt,
                messages=api_messages,
            )

            # Check if response has content
            if not response.content or len(response.content) == 0:
                print(f"⚠️  Warning: Empty response from API")
                print(f"Response: {response}")
                return "I apologize, but I need a moment to gather my thoughts on this."

            return response.content[0].text

        except Exception as e:
            print(f"❌ Error generating Sam's message: {e}")
            print(f"Response object: {response if 'response' in locals() else 'N/A'}")
            return "Let me reconsider this approach..."
