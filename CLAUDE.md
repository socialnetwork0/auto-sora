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
tools/
├── autonomous_sora_chat.py  # Main orchestrator (dialogue loop, termination logic, output generation)
├── sam_altman_ai.py         # Sam Altman persona generator (flips roles for API perspective)
└── sora_copilot.py          # Expert system (loads top prompts, builds system prompt)

Data files:
├── sam_altman_persona.md    # Sam Altman's thinking patterns and leadership principles
└── sora_top_prompts.md      # Top 200 performing Sora prompts database
```

## Development Commands

### Environment Setup
```bash
# This project uses uv for dependency management (NOT pip)
uv venv                              # Create virtual environment
source .venv/bin/activate            # Activate (macOS/Linux)
uv pip install anthropic python-dotenv  # Install dependencies
```

### Running the System
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
`sam_altman_ai.py` implements role flipping (lines 113-121): the dialogue history uses `user=Sam, assistant=Copilot`, but Sam's API perspective requires `user=Copilot (input), assistant=Sam (previous output)`. All roles are flipped before API calls.

### Dialogue Termination Logic
`autonomous_sora_chat.py:_is_dialogue_complete()` (lines 181-204):
- Completion signals only checked after round 3 (avoid premature termination during brainstorming)
- Specific phrases: "that's perfect", "looks perfect", "let's go with this"
- Respects max_rounds as hard limit

### Prompt Extraction
`autonomous_sora_chat.py:extract_final_prompt()` (lines 221-261):
- Uses regex to find italic quote format: `*"...prompt text..."*`
- Checks markdown headers: `## **FINAL PROMPT**`, `## FINAL PROMPT`
- Falls back to last Copilot message if no explicit marker found

### Data Loading
- `SoraCopilot._load_prompts_db()`: Attempts multiple paths, limits to ~50KB to avoid token limits
- `SamAltmanAI._load_persona()`: Supports test mode with mock persona for faster development iterations

## Model Configuration

- **Model**: `claude-sonnet-4-5-20250929` (used by both agents)
- **Temperature**: Sam=0.8 (creative), Copilot=0.7 (professional)
- **Max tokens**: Sam=2000, Copilot=3000
- **Typical usage**: ~15,000 tokens per full dialogue

## Output Format

Generated files in `outputs/` follow this structure:
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
python tools/autonomous_sora_chat.py
```
