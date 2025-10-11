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
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import anthropic
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from sam_altman_ai import SamAltmanAI
from sora_copilot import SoraCopilot

# Setup logger
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",  # Simple format to maintain current output style
        handlers=[logging.StreamHandler()],
    )


@dataclass
class ChatConfig:
    """Configuration for Autonomous Sora Chat."""

    model: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 3000
    temperature: float = 0.7
    max_rounds: int = 7
    initial_prompt: str = (
        "I want to create an exceptional Sora video. Help me brainstorm."
    )


class AutonomousSoraChat:
    """Manages autonomous dialogue between Sam Altman AI and Sora Copilot."""

    def __init__(self, api_key: str, config: ChatConfig = None):
        self.api_key = api_key
        self.config = config or ChatConfig()
        self.max_rounds = self.config.max_rounds  # Maintain compatibility
        self.model = self.config.model

        self.sam = SamAltmanAI(api_key)
        self.copilot = SoraCopilot()
        self.client = anthropic.Anthropic(api_key=api_key)
        self.dialogue_history: List[Dict[str, str]] = []

    def _flip_roles(self, history: List[Dict]) -> List[Dict]:
        """
        Flip user/assistant roles for Sam AI's perspective.

        Storage format: user=Sam, assistant=Copilot (Copilot's API perspective)
        Sam AI needs: user=Copilot (input), assistant=Sam (previous output)
        """
        return [
            {
                "role": "assistant" if msg["role"] == "user" else "user",
                "content": msg["content"],
            }
            for msg in history
        ]

    def start_dialogue(self) -> List[Dict[str, any]]:
        """
        Start autonomous dialogue and return complete conversation.

        Returns:
            List of dialogue rounds with metadata
        """
        logger.info("🚀 Starting Autonomous Sora Prompt Generation")
        logger.info(f"   Max rounds: {self.max_rounds}")
        logger.info(f"   Model: {self.model}\n")

        rounds = []

        # Initialize with a user prompt first (API requires first message to be user role)
        self.dialogue_history.append(
            {
                "role": "user",
                "content": [{"type": "text", "text": self.config.initial_prompt}],
            }
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

        logger.info(f"{'='*70}")
        logger.info(f"Round 0 - Sora Copilot:")
        logger.info(f"{'-'*70}")
        logger.info(copilot_greeting)
        logger.info("")

        # Main dialogue loop - let AIs talk freely
        for round_num in range(1, self.max_rounds + 1):
            # Sam's turn
            logger.info(f"{'='*70}")
            logger.info(f"Round {round_num} - Sam Altman:")
            logger.info(f"{'-'*70}")

            sam_message = self.sam.generate_message(
                self._flip_roles(self.dialogue_history), round_num
            )
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

            logger.info(sam_message)
            logger.info("")

            # Copilot's turn
            logger.info(f"{'='*70}")
            logger.info(f"Round {round_num} - Sora Copilot:")
            logger.info(f"{'-'*70}")

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

            logger.info(copilot_message)
            logger.info("")

            # Simple check: should we continue?
            if not self._should_continue(copilot_message, rounds, round_num):
                break

        logger.info(f"{'='*70}\n")
        logger.info(f"✅ Dialogue completed in {len(rounds)} exchanges")

        return rounds

    def _copilot_response(
        self, history: List[Dict[str, str]], round_number: int
    ) -> str:
        """Generate Copilot's response using Claude API."""
        system_prompt = self.copilot.get_system_prompt(round_number, self.max_rounds)

        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=system_prompt,
            messages=(
                history
                if history
                else [{"role": "user", "content": [{"type": "text", "text": "Begin"}]}]
            ),
        )

        return response.content[0].text

    def _ai_should_stop(self, rounds: List[Dict]) -> bool:
        """Ask AI if the dialogue has naturally concluded."""
        # Take last 3 rounds for context
        recent_rounds = rounds[-3:] if len(rounds) > 3 else rounds

        dialogue_text = "\n\n".join(
            [
                f"**{r['speaker']}** (Round {r['round']}):\n{r['message']}"
                for r in recent_rounds
            ]
        )

        termination_prompt = f"""Analyze the last few rounds of this dialogue between Sam Altman and Sora Copilot.

{dialogue_text}

Has the conversation reached a natural conclusion where:
- Sam Altman has approved or accepted a final prompt
- Sora Copilot has delivered a polished final version
- Both parties seem satisfied with the result

Answer with ONLY 'YES' or 'NO'."""

        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=10,
            temperature=0.1,  # Low temperature for consistent judgment
            messages=[{"role": "user", "content": termination_prompt}],
        )

        answer = response.content[0].text.strip().upper()
        if answer == "YES":
            logger.info("✅ AI detected natural dialogue completion")
            return True
        return False

    def _should_continue(
        self, copilot_message: str, rounds: List[Dict], round_num: int
    ) -> bool:
        """
        Simple 3-level termination check:
        1. XML tag detection (most reliable)
        2. AI judgment after round 4 (intelligent)
        3. max_rounds fallback (safety net)
        """
        # Level 1: Check for explicit <final_prompt> tags
        if "<final_prompt>" in copilot_message and "</final_prompt>" in copilot_message:
            logger.info("✅ <final_prompt> tag detected. Dialogue complete.")
            return False

        # Level 2: AI judges natural conclusion (after round 4)
        if round_num >= 4 and self._ai_should_stop(rounds):
            return False

        # Level 3: Respect max_rounds limit
        if round_num >= self.max_rounds:
            logger.info(f"⚠️  Reached maximum rounds ({self.max_rounds})")
            return False

        return True  # Continue dialogue

    def extract_final_prompt(self, rounds: List[Dict]) -> str:
        """Use AI to intelligently extract the final prompt from dialogue."""
        import re

        # Quick check: Try XML tags first (most reliable)
        for round_data in reversed(rounds[-3:]):
            message = round_data["message"]
            xml_pattern = r"<final_prompt>\s*(.+?)\s*</final_prompt>"
            matches = re.findall(xml_pattern, message, re.DOTALL)
            if matches:
                prompt = matches[0].strip()
                logger.info(
                    f"✅ Extracted using <final_prompt> tags ({len(prompt)} chars)"
                )
                return prompt

        # Use AI to extract from dialogue
        recent_rounds = rounds[-5:] if len(rounds) > 5 else rounds

        dialogue_text = "\n\n".join(
            [
                f"**{r['speaker']}** (Round {r['round']}):\n{r['message']}"
                for r in recent_rounds
            ]
        )

        extraction_system = """You are a precise prompt extractor.
Analyze the dialogue and extract the FINAL approved Sora video prompt.
Return ONLY the pure prompt text itself, with no explanations or meta-commentary."""

        extraction_prompt = f"""Analyze this dialogue between Sam Altman and Sora Copilot:

{dialogue_text}

Extract the FINAL approved Sora video prompt. Look for:
- The most complete and detailed version
- The last prompt that both parties agreed upon
- Content that describes an actual video scene

Return ONLY the prompt text itself."""

        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=2000,
            temperature=0.3,  # Lower temperature for precise extraction
            system=extraction_system,
            messages=[{"role": "user", "content": extraction_prompt}],
        )

        extracted = response.content[0].text.strip()
        logger.info(f"✅ AI extracted final prompt ({len(extracted)} chars)")

        return extracted

    def save_output(self, rounds: List[Dict], output_dir: str = "outputs") -> Path:
        """Save dialogue and final prompt to markdown file."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sora_prompt_{timestamp}.md"
        filepath = output_path / filename

        # Extract final prompt
        final_prompt = self.extract_final_prompt(rounds)

        # VALIDATION: Warn if prompt seems too short or is just metadata
        if len(final_prompt) < 100:
            logger.warning(
                f"⚠️  WARNING: Extracted prompt is very short ({len(final_prompt)} chars)"
            )
            logger.warning(f"   This might not be the actual video prompt.")

        if len(final_prompt) < 50 and any(
            keyword in final_prompt.lower()
            for keyword in ["threshold", "title", "concept"]
        ):
            logger.warning(
                f"⚠️  WARNING: Extracted prompt might be just a title, not the full prompt"
            )

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
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging (DEBUG level)",
    )
    parser.add_argument(
        "--initial-prompt",
        type=str,
        help="Custom initial prompt for Sam Altman AI (overrides default)",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Load .env file
    load_dotenv()

    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        logger.error("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    # Create config
    config = ChatConfig(max_rounds=args.rounds)
    if args.initial_prompt:
        config.initial_prompt = args.initial_prompt
        logger.debug(f"Using custom initial prompt: {args.initial_prompt}")

    # Create chat system
    chat = AutonomousSoraChat(api_key, config=config)

    # Run dialogue
    logger.info("\n" + "=" * 70)
    logger.info("🤖 AUTONOMOUS SORA PROMPT GENERATOR")
    logger.info("=" * 70 + "\n")

    rounds = chat.start_dialogue()

    # Save output
    output_file = chat.save_output(rounds, args.output)

    logger.info("\n" + "=" * 70)
    logger.info("✅ SUCCESS!")
    logger.info("=" * 70)
    logger.info(f"\n📄 Output saved to: {output_file}")
    logger.info(f"📊 Total rounds: {len(rounds)}")
    logger.info(f"🎬 Final prompt extracted and saved\n")


if __name__ == "__main__":
    main()
