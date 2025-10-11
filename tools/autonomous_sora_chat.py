#!/usr/bin/env python3
"""
Autonomous Sora Chat - L4 autonomous dialogue system.

Two AIs engage in autonomous dialogue to generate exceptional Sora prompts:
- Sam Altman AI (User): Strategic creative visionary
- Sora Copilot (System): Expert prompt consultant

Usage:
    python tools/autonomous_sora_chat.py
    python tools/autonomous_sora_chat.py --rounds 7 --output outputs/
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import anthropic
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from sam_altman_ai import SamAltmanAI
from sora_copilot import SoraCopilot


class AutonomousSoraChat:
    """Manages autonomous dialogue between Sam Altman AI and Sora Copilot."""

    def __init__(self, api_key: str, max_rounds: int = 7):
        self.api_key = api_key
        self.max_rounds = max_rounds
        self.sam = SamAltmanAI(api_key)
        self.copilot = SoraCopilot()
        self.client = anthropic.Anthropic(api_key=api_key)
        self.dialogue_history: List[Dict[str, str]] = []
        self.model = "claude-sonnet-4-5-20250929"

    def start_dialogue(self) -> List[Dict[str, any]]:
        """
        Start autonomous dialogue and return complete conversation.

        Returns:
            List of dialogue rounds with metadata
        """
        print("🚀 Starting Autonomous Sora Prompt Generation")
        print(f"   Max rounds: {self.max_rounds}")
        print(f"   Model: {self.model}\n")

        rounds = []

        # Initialize with a user prompt first (API requires first message to be user role)
        initial_prompt = (
            "I want to create an exceptional Sora video. Help me brainstorm."
        )
        self.dialogue_history.append(
            {"role": "user", "content": [{"type": "text", "text": initial_prompt}]}
        )

        # Get Copilot's greeting/response
        copilot_greeting = self._copilot_response(self.dialogue_history, round_number=0)
        self.dialogue_history.append(
            {
                "role": "assistant",
                "content": [{"type": "text", "text": copilot_greeting}],
            }
        )

        rounds.append(
            {
                "round": 0,
                "speaker": "Sora Copilot",
                "message": copilot_greeting,
                "role": "assistant",
            }
        )

        print(f"{'='*70}")
        print(f"Round 0 - Sora Copilot:")
        print(f"{'-'*70}")
        print(copilot_greeting)
        print()

        # Main dialogue loop
        for round_num in range(1, self.max_rounds + 1):
            # Sam's turn
            print(f"{'='*70}")
            print(f"Round {round_num} - Sam Altman:")
            print(f"{'-'*70}")

            sam_message = self.sam.generate_message(self.dialogue_history, round_num)
            self.dialogue_history.append(
                {"role": "user", "content": [{"type": "text", "text": sam_message}]}
            )

            rounds.append(
                {
                    "round": round_num,
                    "speaker": "Sam Altman",
                    "message": sam_message,
                    "role": "user",
                }
            )

            print(sam_message)
            print()

            # Check if Sam is done
            if self._is_dialogue_complete(sam_message, round_num):
                print("✅ Sam has indicated completion. Generating final response...")
                break

            # Copilot's turn
            print(f"{'='*70}")
            print(f"Round {round_num} - Sora Copilot:")
            print(f"{'-'*70}")

            copilot_message = self._copilot_response(self.dialogue_history, round_num)
            self.dialogue_history.append(
                {
                    "role": "assistant",
                    "content": [{"type": "text", "text": copilot_message}],
                }
            )

            rounds.append(
                {
                    "round": round_num,
                    "speaker": "Sora Copilot",
                    "message": copilot_message,
                    "role": "assistant",
                }
            )

            print(copilot_message)
            print()

            # Check if we have a final prompt
            if self._has_final_prompt(copilot_message, round_num):
                print("✅ Final prompt generated. Dialogue complete.")
                break

        print(f"{'='*70}\n")
        print(f"✅ Dialogue completed in {len(rounds)} exchanges")

        return rounds

    def _copilot_response(
        self, history: List[Dict[str, str]], round_number: int
    ) -> str:
        """Generate Copilot's response using Claude API."""
        system_prompt = self.copilot.get_system_prompt()

        # Add round-specific guidance
        if round_number == 0:
            system_prompt += (
                "\n\nThis is the opening. Greet Sam warmly and ask about his vision."
            )
        elif round_number >= self.max_rounds - 2:
            system_prompt += "\n\nWe're approaching the end. Focus on delivering the final prompt(s)."

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            temperature=0.7,
            system=system_prompt,
            messages=(
                history
                if history
                else [{"role": "user", "content": [{"type": "text", "text": "Begin"}]}]
            ),
        )

        return response.content[0].text

    def _is_dialogue_complete(self, message: str, round_num: int) -> bool:
        """Check if Sam has indicated completion."""
        # More specific completion signals to avoid false positives
        completion_signals = [
            "that's perfect",
            "looks perfect",
            "let's go with this",
            "let's go with that",
            "i'm satisfied with",
            "this works for me",
            "approved, let's",
            "ready to generate",
            "generate the prompt",
        ]
        message_lower = message.lower()

        # Only check for completion signals if we're past round 3
        # Early rounds are still brainstorming
        if round_num >= 3:
            if any(signal in message_lower for signal in completion_signals):
                return True

        # Always respect max_rounds limit
        return round_num >= self.max_rounds

    def _has_final_prompt(self, message: str, round_num: int) -> bool:
        """Check if Copilot has provided final prompt(s)."""
        final_indicators = [
            "final prompt",
            "here is the prompt",
            "here are the prompts",
            "final version",
            "polished prompt",
        ]
        message_lower = message.lower()
        return (
            any(indicator in message_lower for indicator in final_indicators)
            or round_num >= self.max_rounds
        )

    def extract_final_prompt(self, rounds: List[Dict]) -> str:
        """Extract the final Sora prompt from the dialogue."""
        # Look in the last 2-3 exchanges for the actual prompt text
        for round_data in reversed(rounds[-3:]):
            message = round_data["message"]

            # Look for the actual prompt in italic format with asterisks
            import re

            # Pattern: *"...prompt text..."* (italic quote format)
            italic_quote_pattern = r'\*"([^"]+)"\*'
            matches = re.findall(italic_quote_pattern, message, re.DOTALL)
            if matches:
                # Return the longest match (likely the main prompt)
                return max(matches, key=len).strip()

            # Look for ## FINAL PROMPT section
            if "## **FINAL PROMPT**" in message or "## FINAL PROMPT" in message:
                # Extract content after this marker
                for marker in ["## **FINAL PROMPT**", "## FINAL PROMPT"]:
                    if marker in message:
                        after_marker = message.split(marker)[1]
                        # Look for italic quote in this section
                        matches = re.findall(
                            italic_quote_pattern, after_marker, re.DOTALL
                        )
                        if matches:
                            return matches[0].strip()

            # Look for **FINAL PROMPT** or **DRAFT PROMPT**
            if "**FINAL PROMPT**" in message or "**DRAFT PROMPT v" in message:
                matches = re.findall(italic_quote_pattern, message, re.DOTALL)
                if matches:
                    return max(matches, key=len).strip()

        # Fallback: return last Copilot message
        for round_data in reversed(rounds):
            if round_data["speaker"] == "Sora Copilot":
                return round_data["message"]

        return "No final prompt extracted"

    def save_output(self, rounds: List[Dict], output_dir: str = "outputs") -> Path:
        """Save dialogue and final prompt to markdown file."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sora_prompt_{timestamp}.md"
        filepath = output_path / filename

        # Extract final prompt
        final_prompt = self.extract_final_prompt(rounds)

        # Build markdown content
        content = f"""# Sora Video Prompt

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Created by**: Sam Altman (AI Persona) + Sora Creator Copilot
**Dialogue Rounds**: {len(rounds)}
**Model**: {self.model}

---

## 🎬 Final Prompt

```
{final_prompt}
```

---

## 💬 Dialogue History

"""

        # Add each round
        for round_data in rounds:
            round_num = round_data["round"]
            speaker = round_data["speaker"]
            message = round_data["message"]

            content += f"""### Round {round_num}: {speaker}

{message}

---

"""

        # Add metadata
        content += f"""## 📊 Metadata

- **Total Rounds**: {len(rounds)}
- **Final Round**: {rounds[-1]['round']}
- **Prompt Length**: {len(final_prompt)} characters
- **Generated At**: {datetime.now().isoformat()}
- **API Model**: {self.model}

---

*This prompt was generated through an autonomous L4 dialogue between Sam Altman AI (persona-driven) and Sora Creator Copilot (expert system).*
"""

        # Write to file
        filepath.write_text(content, encoding="utf-8")

        return filepath


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Autonomous Sora prompt generation through AI dialogue"
    )
    parser.add_argument(
        "--rounds", type=int, default=7, help="Maximum dialogue rounds (default: 7)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs",
        help="Output directory (default: outputs)",
    )

    args = parser.parse_args()

    # Load .env file
    load_dotenv()

    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    # Create chat system
    chat = AutonomousSoraChat(api_key, max_rounds=args.rounds)

    # Run dialogue
    print("\n" + "=" * 70)
    print("🤖 AUTONOMOUS SORA PROMPT GENERATOR")
    print("=" * 70 + "\n")

    rounds = chat.start_dialogue()

    # Save output
    output_file = chat.save_output(rounds, args.output)

    print("\n" + "=" * 70)
    print("✅ SUCCESS!")
    print("=" * 70)
    print(f"\n📄 Output saved to: {output_file}")
    print(f"📊 Total rounds: {len(rounds)}")
    print(f"🎬 Final prompt extracted and saved\n")


if __name__ == "__main__":
    main()
