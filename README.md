# Auto-Sora 🎬

**Autonomous AI-to-AI dialogue system for generating exceptional Sora video prompts**

Auto-Sora leverages cutting-edge L4 autonomous dialogue between two AI agents to collaboratively create high-quality prompts for OpenAI's Sora video generation model. Through strategic conversation and iterative refinement, the system produces professionally crafted prompts that capture cinematic vision and technical precision.

---

## Features

✨ **Dual AI Collaboration**
- **Sam Altman AI**: Strategic creative visionary with persona-driven thinking patterns
- **Sora Copilot**: Expert prompt consultant leveraging 200+ top-performing prompt examples

🎯 **Intelligent Dialogue System**
- 5-7 rounds of autonomous conversation with natural completion detection
- Role-flipping architecture for authentic bidirectional dialogue
- Temperature-tuned creativity levels (Sam: 0.8, Copilot: 0.7)

🖥️ **Dual Interface**
- **CLI Mode**: Batch processing with file output for automation
- **Web UI Mode**: Interactive Streamlit interface with real-time streaming

📊 **Smart Output Management**
- Automatic prompt extraction from multiple markdown formats
- Timestamped markdown files with full dialogue history
- Real-time statistics and metadata tracking

---

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/auto-sora.git
cd auto-sora

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install anthropic python-dotenv streamlit black watchdog

# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Usage

#### Web Interface (Recommended)

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser:
1. Enter your API key in the sidebar (or use environment variable)
2. Configure dialogue rounds and temperature
3. Click "Start Dialogue" to watch the AIs collaborate in real-time
4. Download the final prompt as markdown when complete

#### Command Line Interface

```bash
# Basic usage (7 rounds, default settings)
python tools/autonomous_sora_chat.py

# Custom configuration
python tools/autonomous_sora_chat.py --rounds 5 --output my_prompts/

# Test mode (faster, uses mock persona)
python tools/autonomous_sora_chat.py --test
```

Output files are saved to `outputs/sora_prompt_YYYYMMDD_HHMMSS.md`

---

## How It Works

### The Dialogue Flow

```
Round 0: Sora Copilot greets Sam and presents initial concepts
   ↓
Round 1-N: Iterative refinement through natural conversation
   - Sam proposes creative vision and strategic direction
   - Copilot refines with technical expertise and proven patterns
   - Each round builds on previous insights
   ↓
Auto-termination when both agents reach consensus
   ↓
Final prompt extracted and saved
```

### Architecture Overview

- **Sam Altman AI** (`tools/sam_altman_ai.py`): Loads persona from `sam_altman_persona.md`, generates creative responses with strategic thinking patterns
- **Sora Copilot** (`tools/sora_copilot.py`): Leverages success patterns from `sora_top_prompts.md` database, provides expert consultation
- **Orchestrator** (`tools/autonomous_sora_chat.py` or `app.py`): Manages dialogue flow, role flipping, termination detection, and output generation

---

## Example Output

A typical generated prompt might look like:

> *"A contemplative medium shot of a street artist in Brooklyn during golden hour, spray-painting a vibrant mural of interconnected hands reaching skyward. Warm amber light filters through urban architecture, casting long shadows. Shot on Arri Alexa with 50mm lens, shallow depth of field isolating the artist against soft bokeh background. Slow tracking shot following the fluid motion of creation, capturing authentic urban storytelling with cinematic color grading."*

Each output includes:
- 🎬 **Final Prompt**: Polished, production-ready prompt
- 💬 **Full Dialogue**: Complete conversation history with round numbers
- 📊 **Metadata**: Generation timestamp, model info, statistics

---

## Project Structure

```
auto-sora/
├── app.py                        # Streamlit web interface
├── tools/
│   ├── autonomous_sora_chat.py   # CLI orchestrator
│   ├── sam_altman_ai.py          # Sam Altman persona AI
│   └── sora_copilot.py           # Sora expert consultant
├── sam_altman_persona.md         # Sam's thinking patterns
├── sora_top_prompts.md           # Top 200 prompt database
├── outputs/                      # Generated prompts (CLI mode)
└── public/                       # UI assets (avatars)
```

---

## Configuration

### Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY='sk-ant-...'

# Optional (CLI mode)
export SORA_MAX_ROUNDS=7
export SORA_OUTPUT_DIR='./outputs'
```

### Model Configuration

- **Model**: Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- **Max Tokens**: Sam=2000, Copilot=3000
- **Temperature**: Sam=0.8 (creative), Copilot=0.7 (professional)
- **Average Cost**: ~15,000 tokens per full dialogue (~$0.45)

---

## Development

### Code Formatting

```bash
black .                              # Format all Python files
black tools/autonomous_sora_chat.py  # Format specific file
```

### Testing Individual Components

```bash
# Test Sam Altman AI
python tools/sam_altman_ai.py

# Test Sora Copilot system prompt
python tools/sora_copilot.py

# View latest output
ls -lt outputs/ | head -n 2
```

### Project Guidelines

This project uses `uv` for dependency management (NOT `pip`). Always use:
- `uv venv` to create environments
- `uv pip install <package>` to install dependencies

For detailed development instructions, see [CLAUDE.md](CLAUDE.md).

---

## Troubleshooting

**API Key Not Found**
```bash
export ANTHROPIC_API_KEY='your-key-here'
# Or add to .env file in project root
```

**Streamlit Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

**Missing Persona Files**
- Production mode requires `sam_altman_persona.md` at project root
- Use `--test` flag for development without persona file

---

## Technical Details

### Role Flipping Pattern

The dialogue history is maintained from Copilot's perspective (`user=Sam, assistant=Copilot`), but Sam's API calls require the opposite perspective. The `flip_roles()` function automatically inverts all roles before each Sam AI API call, ensuring consistent dialogue flow.

### Termination Detection

The system intelligently detects conversation completion after round 3 by monitoring for phrases like:
- "that's perfect"
- "looks perfect"
- "let's go with this"

This prevents premature termination during brainstorming while ensuring natural conclusion.

### Prompt Extraction

Supports multiple output formats:
1. Italic quotes: `*"prompt text"*`
2. Markdown headers: `## **FINAL PROMPT**` or `## FINAL PROMPT`
3. Fallback: Last Copilot message if no explicit marker

---

## Roadmap

- [ ] Multi-language persona support
- [ ] Custom persona templates
- [ ] Prompt library with tagging and search
- [ ] A/B testing framework for prompt variations
- [ ] Integration with actual Sora API (when available)
- [ ] Collaborative editing mode (human-in-the-loop)

---

## License

This is a private project. No license file is included.

---

## Credits

Powered by [Anthropic Claude](https://www.anthropic.com/claude) with prompt engineering inspired by top-performing Sora community examples.

---

## Support

For issues, questions, or contributions, please open an issue on GitHub or contact the maintainers.

**Built with ❤️ for the AI creative community**
