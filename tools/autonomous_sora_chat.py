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
    """Configuration for autonomous dialogue system with layered model architecture."""

    max_rounds: int = 5  # Reduced from 7 for hackathon speed optimization
    max_tokens: int = 3000
    temperature: float = 0.7

    # Agent layer model (high-frequency dialogue generation)
    # Currently Haiku for cost efficiency; can upgrade to Sonnet for higher quality
    agent_model: str = "claude-haiku-4-5-20251001"

    # Orchestrator layer model (low-frequency intelligent decisions)
    # Currently Haiku for development; should upgrade to Sonnet for production
    # Used for: dialogue termination judgment, final prompt extraction, quality validation
    orchestrator_model: str = (
        "claude-haiku-4-5-20251001"  # TODO: Use claude-sonnet-4-5-20250929 in production
    )

    initial_prompt: str = (
        "I want to create an exceptional Sora video. Help me brainstorm."
    )


class AutonomousSoraChat:
    """Manages autonomous dialogue between Sam Altman AI and Sora Copilot."""

    def __init__(self, api_key: str, config: ChatConfig = None):
        self.api_key = api_key
        self.config = config or ChatConfig()
        self.max_rounds = self.config.max_rounds  # Maintain compatibility

        # Agent layer: high-frequency dialogue generation
        self.agent_model = self.config.agent_model
        self.sam = SamAltmanAI(api_key, model=self.agent_model)
        self.copilot = SoraCopilot(model=self.agent_model)

        # Orchestrator layer: low-frequency intelligent decisions
        self.orchestrator_model = self.config.orchestrator_model

        self.client = anthropic.Anthropic(api_key=api_key)
        self.dialogue_history: List[Dict[str, str]] = []

    def _flip_roles(self, history: List[Dict]) -> List[Dict]:
        """Flip user/assistant roles for Sam AI's perspective."""
        return [
            {
                "role": "assistant" if msg["role"] == "user" else "user",
                "content": msg["content"],
            }
            for msg in history
        ]

    def _add_history_cache_control(self, messages: List[Dict]) -> List[Dict]:
        """Add cache_control to the last historical message for prompt caching."""
        if len(messages) < 2:
            return messages

        import copy

        messages_copy = copy.deepcopy(messages)
        last_history_idx = -2
        if "content" in messages_copy[last_history_idx] and isinstance(
            messages_copy[last_history_idx]["content"], list
        ):
            messages_copy[last_history_idx]["content"][-1]["cache_control"] = {
                "type": "ephemeral"
            }

        return messages_copy

    def start_dialogue(self) -> List[Dict[str, any]]:
        """Start autonomous dialogue and return complete conversation."""
        logger.info("🚀 Starting Autonomous Sora Prompt Generation")
        logger.info(f"   Max rounds: {self.max_rounds}")
        logger.info(f"   Agent model: {self.agent_model}")
        logger.info(f"   Orchestrator model: {self.orchestrator_model}\n")

        rounds = []

        self.dialogue_history.append(
            {
                "role": "user",
                "content": [{"type": "text", "text": self.config.initial_prompt}],
            }
        )

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

        for round_num in range(1, self.max_rounds + 1):
            logger.info(f"{'='*70}")
            logger.info(f"Round {round_num} - Sam Altman:")
            logger.info(f"{'-'*70}")

            sam_history = self._flip_roles(self.dialogue_history)
            sam_history = self._add_history_cache_control(sam_history)

            sam_message = self.sam.generate_message(
                sam_history, round_num, self.max_rounds
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

            if not self._should_continue(copilot_message, round_num):
                break

        logger.info(f"{'='*70}\n")
        logger.info(f"✅ Dialogue completed in {len(rounds)} exchanges")

        return rounds

    def _copilot_response(
        self, history: List[Dict[str, str]], round_number: int, stream: bool = False
    ):
        """Generate Copilot's response using Claude API."""
        system_blocks = self.copilot.get_system_prompt(round_number, self.max_rounds)
        messages = (
            history
            if history
            else [{"role": "user", "content": [{"type": "text", "text": "Begin"}]}]
        )
        messages = self._add_history_cache_control(messages)

        if stream:
            return self._copilot_response_stream(system_blocks, messages)
        else:
            response = self.client.messages.create(
                model=self.agent_model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_blocks,
                messages=messages,
            )
            return response.content[0].text

    def _copilot_response_stream(self, system_blocks, messages):
        """Generator for streaming Copilot responses."""
        with self.client.messages.stream(
            model=self.agent_model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=system_blocks,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield text

    def _should_continue(self, copilot_message: str, round_num: int) -> bool:
        """Check if dialogue should continue."""
        if "<final_prompt>" in copilot_message and "</final_prompt>" in copilot_message:
            logger.info("✅ <final_prompt> tag detected. Dialogue complete.")
            return False

        if round_num >= self.max_rounds:
            logger.info(f"⚠️  Reached maximum rounds ({self.max_rounds})")
            return False

        return True

    def extract_final_prompt(self, rounds: List[Dict]) -> str:
        """Extract final prompt from <final_prompt> XML tags."""
        import re

        for round_data in reversed(rounds):
            if round_data["speaker"] != "Sora Copilot":
                continue

            message = round_data["message"]
            xml_pattern = r"<final_prompt>\s*(.*?)\s*</final_prompt>"
            matches = re.findall(xml_pattern, message, re.DOTALL | re.IGNORECASE)

            if matches:
                prompt = matches[0].strip()
                logger.info(
                    f"✅ Extracted using <final_prompt> tags ({len(prompt)} chars)"
                )
                return prompt

        logger.warning(
            "⚠️  No <final_prompt> tags found. Using last Copilot message as fallback."
        )
        for round_data in reversed(rounds):
            if round_data["speaker"] == "Sora Copilot":
                return round_data["message"]

        return "Error: No prompt found in dialogue."

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
**Agent Model**: {self.agent_model}
**Orchestrator Model**: {self.orchestrator_model}

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
- **Agent Model**: {self.agent_model} (dialogue generation)
- **Orchestrator Model**: {self.orchestrator_model} (intelligent decisions)

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
        "--rounds", type=int, default=5, help="Maximum dialogue rounds (default: 5)"
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
