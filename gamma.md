# Auto-Sora Hackathon Pitch Deck

**Project Title:** Auto-Sora: Fully Autonomous L4 AI Partner for Creators

**Brief Description:**
Auto-Sora is a fully autonomous L4 dialogue system generating cinema-quality Sora video prompts through AI-to-AI collaboration. Two specialized agents engage in 5-7 conversational rounds, debating and refining until producing professional prompts with technical precision. Sam Altman AI demonstrates our showcase persona—the system adapts to any creator, company, or brand voice for customized strategies. Built with Claude Sonnet 4.5, it features intelligent dialogue flow, real-time streaming, and automatic extraction. Transform vague ideas into prompts with camera specs, lighting, and cinematic details in 3 minutes at $0.45. Scalable from solo creators to enterprise production teams, democratizing expert video prompt engineering.

---

## SLIDE 1: The Problem

**Writing Effective Sora Prompts Requires Expertise**

Getting quality results from Sora requires specific knowledge:

- **Film production**: Camera angles, lenses, lighting, shot composition
- **Technical vocabulary**: How to structure prompts for AI interpretation
- **Iterative refinement**: Understanding what works and why

**The Gap:**
Creators have ideas but lack the technical language to express them effectively.

**Current Solutions Fall Short:**
- Trial and error → time-consuming
- Prompt templates → limited creativity
- Prompt engineers → expensive, not scalable

---

## SLIDE 2: Our Solution

**Auto-Sora: L4 Autonomous Dialogue System**

**How It Works:**

```
👤 Creative Agent        🤖 Expert Agent
   (Any persona)         (Prompt specialist)
        ↓                        ↓
     Proposes              Refines with
      vision              technical detail
        ↓                        ↓
    5-7 rounds of autonomous conversation
        ↓
    Production-ready prompt
```

**System Design:**

1. **L4 Autonomous Dialogue**
   - Two agents debate and iterate without human intervention
   - Creative agent: Strategic vision (we demo with Sam Altman persona)
   - Expert agent: Technical refinement using 200+ proven patterns

2. **Customizable Personas**
   - Sam Altman AI is our showcase example
   - System adapts to any creator, brand, or company voice

3. **Dual Interface**
   - Web UI: Real-time streaming visualization
   - CLI: Batch generation for production workflows

**Example Output:**

> *"A contemplative medium shot of a street artist in Brooklyn during golden hour, spray-painting a vibrant mural of interconnected hands reaching skyward. Warm amber light filters through urban architecture, casting long shadows. Shot on Arri Alexa with 50mm lens, shallow depth of field isolating the artist against soft bokeh background. Slow tracking shot following the fluid motion of creation, capturing authentic urban storytelling with cinematic color grading."*

---

## SLIDE 3: Technical Implementation

**Architecture & Performance**

**Tech Stack:**

```
Claude Sonnet 4.5 (Dual agent orchestration)
Persona engineering (Customizable .md files)
Prompt database (200+ reference examples)
Role-flipping architecture (Bidirectional context)
Streamlit + Python (Production-ready deployment)
```

**Key Technical Features:**

1. **Role Flipping Pattern**
   - Maintains conversational context from both agent perspectives
   - Enables authentic debate between agents

2. **Intelligent Termination**
   - Detects natural conversation completion
   - Averages 5-7 rounds (optimized for quality vs efficiency)

3. **Multi-Format Extraction**
   - Parses prompts from markdown, quotes, headers
   - Fallback mechanisms ensure reliable output

**Performance:**
- 3 minutes average generation time
- $0.45 per dialogue (~15k tokens)
- 5-7 rounds typical
- Scalable architecture

---

## SLIDE 4: Use Cases & Demo

**Use Cases:**

- **Filmmakers**: Storyboard descriptions → Sora prompts
- **Marketers**: Campaign concepts → Video ads
- **Educators**: Teaching concepts → Explainer videos
- **Studios**: Scene descriptions → Production prompts