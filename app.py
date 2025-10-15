#!/usr/bin/env python3
"""
Streamlit frontend for Auto-Sora dialogue system.

Usage:
    streamlit run app.py
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))

from sam_altman_ai import SamAltmanAI
from sora_copilot import SoraCopilot
from autonomous_sora_chat import ChatConfig
import anthropic

# Load environment variables
load_dotenv()


# Page configuration
st.set_page_config(
    page_title="Auto-Sora Prompt Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "dialogue_history" not in st.session_state:
        st.session_state.dialogue_history = []
    if "rounds" not in st.session_state:
        st.session_state.rounds = []
    if "current_round" not in st.session_state:
        st.session_state.current_round = 0
    if "is_running" not in st.session_state:
        st.session_state.is_running = False
    if "final_prompt" not in st.session_state:
        st.session_state.final_prompt = ""
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY", "")


def extract_final_prompt(text: str) -> str:
    """Extract final prompt from Copilot's message."""
    # Pattern 1: Italic quote format *"..."*
    italic_pattern = r'\*"([^"]+)"\*'
    matches = re.findall(italic_pattern, text)
    if matches:
        return matches[-1]  # Return last match

    # Pattern 2: Markdown headers
    header_patterns = [
        r"## \*\*FINAL PROMPT\*\*\s*\n(.+?)(?:\n##|\Z)",
        r"## FINAL PROMPT\s*\n(.+?)(?:\n##|\Z)",
        r"### Final Prompt\s*\n(.+?)(?:\n##|\Z)",
    ]

    for pattern in header_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return ""


def flip_roles(history):
    """Flip user/assistant roles for Sam AI's perspective."""
    return [
        {
            "role": "assistant" if msg["role"] == "user" else "user",
            "content": msg["content"],
        }
        for msg in history
    ]


def run_dialogue(max_rounds: int, temperature: float, api_key: str):
    """Run the autonomous dialogue with streaming output."""
    try:
        # Avatar images
        sora_avatar = "public/sora.png"
        sam_avatar = "public/sama.jpeg"

        # Initialize clients
        config = ChatConfig(max_rounds=max_rounds, temperature=temperature)
        sam = SamAltmanAI(api_key=api_key)
        copilot = SoraCopilot()
        client = anthropic.Anthropic(api_key=api_key)

        # Initialize dialogue with first user message
        st.session_state.dialogue_history = [
            {
                "role": "user",
                "content": [{"type": "text", "text": config.initial_prompt}],
            }
        ]

        # Round 0: Copilot greeting
        st.session_state.current_round = 0

        with st.chat_message("assistant", avatar=sora_avatar):
            st.markdown("**Sora Copilot (Round 0)**")
            message_placeholder = st.empty()

            # Stream Copilot's greeting with prompt caching
            system_blocks = copilot.get_system_prompt(0, max_rounds)
            full_response = ""

            with client.messages.stream(
                model=config.model,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                system=system_blocks,
                messages=st.session_state.dialogue_history,
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            # Save to history
            st.session_state.dialogue_history.append(
                {
                    "role": "assistant",
                    "content": [{"type": "text", "text": full_response}],
                }
            )

        # Main dialogue loop
        for round_num in range(1, max_rounds + 1):
            st.session_state.current_round = round_num

            # === Sam's turn ===
            with st.chat_message("user", avatar=sam_avatar):
                st.markdown(f"**Sam Altman (Round {round_num})**")
                sam_placeholder = st.empty()

                # Stream Sam's response
                sam_response = ""
                flipped_history = flip_roles(st.session_state.dialogue_history)

                for text_chunk in sam.generate_message(
                    flipped_history, round_num, stream=True
                ):
                    sam_response += text_chunk
                    sam_placeholder.markdown(sam_response + "▌")

                sam_placeholder.markdown(sam_response)

                # Save to history
                st.session_state.dialogue_history.append(
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": sam_response}],
                    }
                )

            # === Copilot's turn ===
            with st.chat_message("assistant", avatar=sora_avatar):
                st.markdown(f"**Sora Copilot (Round {round_num})**")
                copilot_placeholder = st.empty()

                # Stream Copilot's response with prompt caching
                copilot_response = ""
                system_blocks = copilot.get_system_prompt(round_num, max_rounds)

                with client.messages.stream(
                    model=config.model,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    system=system_blocks,
                    messages=st.session_state.dialogue_history,
                ) as stream:
                    for text in stream.text_stream:
                        copilot_response += text
                        copilot_placeholder.markdown(copilot_response + "▌")

                copilot_placeholder.markdown(copilot_response)

                # Save to history
                st.session_state.dialogue_history.append(
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": copilot_response}],
                    }
                )

                # Try to extract final prompt
                extracted = extract_final_prompt(copilot_response)
                if extracted:
                    st.session_state.final_prompt = extracted

        st.success(f"✅ Dialogue completed! Generated {max_rounds} rounds.")

    except Exception as e:
        st.error(f"Error during dialogue: {str(e)}")
        st.session_state.is_running = False


def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Header
    st.title("🎬 Auto-Sora Prompt Generator")
    st.markdown(
        "**Autonomous AI-to-AI dialogue** for generating exceptional Sora video prompts"
    )

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key input
        api_key_input = st.text_input(
            "Anthropic API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your Anthropic API key (or set ANTHROPIC_API_KEY env var)",
        )

        if api_key_input:
            st.session_state.api_key = api_key_input

        # Dialogue parameters
        max_rounds = st.slider(
            "Max Rounds",
            min_value=3,
            max_value=10,
            value=7,
            help="Number of dialogue rounds",
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Creativity level (higher = more creative)",
        )

        st.divider()

        # Start button
        if st.button(
            "🚀 Start Dialogue", type="primary", disabled=st.session_state.is_running
        ):
            if not st.session_state.api_key:
                st.error("Please provide an Anthropic API key")
            else:
                st.session_state.is_running = True
                st.session_state.dialogue_history = []
                st.session_state.rounds = []
                st.session_state.final_prompt = ""
                st.rerun()

        # Reset button
        if st.button("🔄 Reset"):
            st.session_state.dialogue_history = []
            st.session_state.rounds = []
            st.session_state.current_round = 0
            st.session_state.is_running = False
            st.session_state.final_prompt = ""
            st.rerun()

        st.divider()

        # Info section
        st.markdown("### ℹ️ About")
        st.markdown(
            """
            This app demonstrates L4 autonomous dialogue between:
            - **Sam Altman AI** (👤): Creative visionary
            - **Sora Copilot** (🤖): Prompt consultant

            The AIs collaborate to create exceptional Sora video prompts.
            """
        )

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("💬 Dialogue")

        # Progress indicator
        if st.session_state.current_round > 0:
            progress_text = f"Round {st.session_state.current_round} / {max_rounds}"
            st.progress(
                st.session_state.current_round / max_rounds,
                text=progress_text,
            )

        # Display dialogue
        if st.session_state.is_running and not st.session_state.dialogue_history:
            with st.spinner("Starting dialogue..."):
                run_dialogue(max_rounds, temperature, st.session_state.api_key)
                st.session_state.is_running = False
                st.rerun()
        elif st.session_state.dialogue_history:
            # Display completed dialogue
            for i, msg in enumerate(st.session_state.dialogue_history):
                if i == 0:
                    continue  # Skip initial prompt

                role = "assistant" if msg["role"] == "assistant" else "user"
                avatar = (
                    "public/sora.png" if role == "assistant" else "public/sama.jpeg"
                )
                speaker = "Sora Copilot" if role == "assistant" else "Sam Altman"

                # Calculate round number
                round_num = (i - 1) // 2 if i > 1 else 0

                with st.chat_message(role, avatar=avatar):
                    st.markdown(f"**{speaker} (Round {round_num})**")
                    content = (
                        msg["content"][0]["text"]
                        if isinstance(msg["content"], list)
                        else msg["content"]
                    )
                    st.markdown(content)
        else:
            st.info("👈 Configure parameters and click 'Start Dialogue' to begin")

    with col2:
        st.header("📝 Final Prompt")

        if st.session_state.final_prompt:
            st.success("✨ Extracted final prompt:")
            st.markdown(f'*"{st.session_state.final_prompt}"*')

            # Download button
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sora_prompt_{timestamp}.md"

            # Generate markdown content
            markdown_content = f"""# Sora Video Prompt
**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Rounds**: {st.session_state.current_round}

## 🎬 Final Prompt
{st.session_state.final_prompt}

## 💬 Full Dialogue
"""
            for i, msg in enumerate(st.session_state.dialogue_history):
                if i == 0:
                    continue
                role = "assistant" if msg["role"] == "assistant" else "user"
                speaker = "Sora Copilot" if role == "assistant" else "Sam Altman"
                round_num = (i - 1) // 2 if i > 1 else 0
                content = (
                    msg["content"][0]["text"]
                    if isinstance(msg["content"], list)
                    else msg["content"]
                )
                markdown_content += f"\n### Round {round_num} - {speaker}\n{content}\n"

            st.download_button(
                label="⬇️ Download Full Transcript",
                data=markdown_content,
                file_name=filename,
                mime="text/markdown",
            )
        else:
            st.info("The final prompt will appear here once the dialogue is complete")

        # Display statistics
        if st.session_state.dialogue_history:
            st.divider()
            st.markdown("### 📊 Statistics")
            total_messages = (
                len(st.session_state.dialogue_history) - 1
            )  # Exclude initial prompt
            total_words = sum(
                (
                    len(msg["content"][0]["text"].split())
                    if isinstance(msg["content"], list)
                    else len(msg["content"].split())
                )
                for msg in st.session_state.dialogue_history
            )
            st.metric("Total Messages", total_messages)
            st.metric("Total Words", total_words)


if __name__ == "__main__":
    main()
