# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**auto-sora** is an autonomous L4 dialogue system that generates high-quality Sora video prompts through AI-to-AI conversations.

### Architecture

Two AI agents engage in autonomous dialogue:
- **Sam Altman AI (User role)**: Strategic creative visionary using persona-driven responses from `sam_altman_persona.md`
- **Sora Copilot (System role)**: Expert prompt consultant leveraging success patterns from `sora_top_prompts.md`

The dialogue runs for 5-7 rounds, producing optimized Sora video prompts saved as timestamped markdown files.

### Core Components

```
app.py                       # Streamlit web UI (streaming dialogue, real-time visualization)
tools/
├── autonomous_sora_chat.py  # CLI orchestrator (dialogue loop, termination logic, file output)
├── sam_altman_ai.py         # Sam Altman persona generator (flips roles for API perspective)
└── sora_copilot.py          # Expert system (loads top prompts, builds system prompt)

Data files:
├── sam_altman_persona.md    # Sam Altman's thinking patterns and leadership principles
└── sora_top_prompts.md      # Top 200 performing Sora prompts database

Assets:
├── public/sora.png          # Sora Copilot avatar (Web UI)
└── public/sama.jpeg         # Sam Altman avatar (Web UI)
```

**Dual Interface Architecture:**
- **CLI**: `autonomous_sora_chat.py` - Batch processing, saves to `outputs/` directory
- **Web UI**: `app.py` - Interactive streaming, real-time visualization, in-browser download

## Development Commands

### Environment Setup
```bash
# This project uses uv for dependency management (NOT pip)
uv venv                              # Create virtual environment
source .venv/bin/activate            # Activate (macOS/Linux)

# Install all dependencies (includes streamlit, anthropic, python-dotenv, black, watchdog)
uv pip install -r pyproject.toml     # Or install individually:
uv pip install anthropic python-dotenv streamlit black watchdog
```

### Running the System

**CLI Mode (Command Line):**
```bash
# Set API key (required)
export ANTHROPIC_API_KEY='your-key-here'

# Basic run (default 7 rounds)
python tools/autonomous_sora_chat.py

# Custom parameters
python tools/autonomous_sora_chat.py --rounds 5 --output my_outputs/

# Test mode (uses mock persona, faster for development)
python tools/autonomous_sora_chat.py --test
```

**Web UI Mode (Streamlit):**
```bash
# Set API key (or enter in UI)
export ANTHROPIC_API_KEY='your-key-here'

# Start web interface
streamlit run app.py

# The UI will open at http://localhost:8501
# Configure parameters (rounds, temperature) in the sidebar
# Click "Start Dialogue" to generate prompts with streaming output
```

### Testing Individual Components
```bash
# Test Sam Altman AI generator
python tools/sam_altman_ai.py

# Test Sora Copilot system prompt
python tools/sora_copilot.py

# View latest output
ls -lt outputs/ | head -n 2
cat outputs/sora_prompt_*.md
```

### Code Formatting
```bash
black .                              # Format all Python files
black tools/autonomous_sora_chat.py  # Format specific file
```

## Key Implementation Details

### Role Flipping Pattern
Both [autonomous_sora_chat.py](tools/autonomous_sora_chat.py) and [app.py](app.py) implement role flipping: the dialogue history uses `user=Sam, assistant=Copilot`, but Sam's API perspective requires `user=Copilot (input), assistant=Sam (previous output)`. The `flip_roles()` function swaps all roles before Sam AI's API calls.

### Dialogue Termination Logic
`autonomous_sora_chat.py:_is_dialogue_complete()` (lines 181-204):
- Completion signals only checked after round 3 (avoid premature termination during brainstorming)
- Specific phrases: "that's perfect", "looks perfect", "let's go with this"
- Respects max_rounds as hard limit

### Prompt Extraction
Both CLI and Web UI implement `extract_final_prompt()` with identical logic:
- Pattern 1: Italic quote format `*"...prompt text..."*`
- Pattern 2: Markdown headers `## **FINAL PROMPT**`, `## FINAL PROMPT`, `### Final Prompt`
- CLI fallback: Returns last Copilot message if no explicit marker
- Web UI: Real-time extraction on each Copilot response, stores in `session_state.final_prompt`

### Data Loading
- [SoraCopilot._load_prompts_db()](tools/sora_copilot.py): Attempts multiple paths, limits to ~50KB to avoid token limits
- [SamAltmanAI._load_persona()](tools/sam_altman_ai.py): Supports test mode with mock persona for faster development iterations

### Streaming Implementation
[app.py](app.py) implements real-time streaming for better UX:
- **Sam AI**: Uses `sam.generate_message(..., stream=True)` which yields text chunks
- **Sora Copilot**: Uses `client.messages.stream()` context manager with `stream.text_stream`
- Both display animated cursor (`"▌"`) during streaming, removed when complete
- Streamlit `st.empty()` placeholder enables incremental text updates without re-rendering entire UI

## Model Configuration

- **Model**: `claude-sonnet-4-5-20250929` (used by both agents)
- **Temperature**: Sam=0.8 (creative), Copilot=0.7 (professional)
- **Max tokens**: Sam=2000, Copilot=3000
- **Typical usage**: ~15,000 tokens per full dialogue

## Output Format

**CLI Output** (`outputs/sora_prompt_YYYYMMDD_HHMMSS.md`):
```markdown
# Sora Video Prompt
**Generated**: [timestamp]
**Dialogue Rounds**: [count]
**Model**: [model-id]

## 🎬 Final Prompt
[Extracted prompt text]

## 💬 Dialogue History
[Complete conversation with round numbers]

## 📊 Metadata
[Statistics and generation info]
```

**Web UI Output** (downloaded via browser):
- Same markdown format as CLI
- Generated on-demand when clicking "Download Full Transcript" button
- Includes real-time word count and message count statistics
- Displays final prompt in sidebar during and after dialogue

## Common Issues

### Missing API Key
If you see `ANTHROPIC_API_KEY environment variable not set`, run:
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

### Persona/Prompts File Not Found
- Production mode requires `sam_altman_persona.md` at project root
- Use `--test` flag during development to skip persona file requirement
- Copilot gracefully handles missing `sora_top_prompts.md` (returns empty string)

### Module Import Errors
Always run from project root:
```bash
cd /Users/yuanlu/Code/auto-sora
python tools/autonomous_sora_chat.py  # CLI mode
streamlit run app.py                  # Web UI mode
```

### Streamlit Port Already in Use
If port 8501 is occupied:
```bash
streamlit run app.py --server.port 8502  # Use different port
```

### Missing Avatar Images
Web UI requires `public/sora.png` and `public/sama.jpeg` for agent avatars. If missing, Streamlit will show default avatars but functionality remains unaffected.
