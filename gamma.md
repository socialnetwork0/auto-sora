# Auto-Sora Hackathon Pitch Deck

**Project Title:** Auto-Sora: Fully Autonomous L4 AI Partner for Creators

**Brief Description:**
Auto-Sora is a fully autonomous L4 dialogue system generating cinema-quality Sora video prompts through AI-to-AI collaboration. Two specialized agents engage in 5-7 conversational rounds, debating and refining until producing professional prompts with technical precision. Sam Altman AI demonstrates our showcase persona—the system adapts to any creator, company, or brand voice for customized strategies. Built with Claude Sonnet 4.5, it features intelligent dialogue flow, real-time streaming, and automatic extraction. Transform vague ideas into prompts with camera specs, lighting, and cinematic details in 3 minutes at $0.45. Scalable from solo creators to enterprise production teams, democratizing expert video prompt engineering.

**Gamma.app Instructions**: Copy each slide's content into Gamma's AI generator, select "Modern/Tech" theme, use auto-layout with images.

---

## SLIDE 1: WHY - The Problem

### Title
**Writing Effective Sora Prompts Requires Expertise**

### Main Content

**The Challenge:**

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

**What's Needed:**
A system that bridges creative vision and technical execution automatically.

### Visual Suggestions for Gamma:
- Simple side-by-side: basic prompt vs detailed professional prompt
- Three challenge icons (film knowledge, technical vocabulary, iteration)
- Clean, minimal design

---

## SLIDE 2: WHAT - Our Solution

### Title
**Auto-Sora: L4 Autonomous Dialogue System**

### Main Content

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
   - Persona-driven for consistent creative strategy

3. **Dual Interface**
   - Web UI: Real-time streaming visualization
   - CLI: Batch generation for production workflows

**Example Output:**

> *"A contemplative medium shot of a street artist in Brooklyn during golden hour, spray-painting a vibrant mural of interconnected hands reaching skyward. Warm amber light filters through urban architecture, casting long shadows. Shot on Arri Alexa with 50mm lens, shallow depth of field isolating the artist against soft bokeh background. Slow tracking shot following the fluid motion of creation, capturing authentic urban storytelling with cinematic color grading."*

### Visual Suggestions for Gamma:
- Clean dialogue flow diagram with arrows
- Screenshot of Web UI showing agent conversation
- Example prompt in quote card format
- Emphasis on "Any Persona" with multiple avatar silhouettes

---

## SLIDE 3: HOW - Technical Implementation

### Title
**Architecture & Performance**

### Technical Stack

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

### Use Cases

- Filmmakers: Storyboard descriptions → Sora prompts
- Marketers: Campaign concepts → Video ads
- Educators: Teaching concepts → Explainer videos
- Studios: Scene descriptions → Production prompts

### Try It

```bash
streamlit run app.py
```

**Open to:**
- Testing and feedback
- Partnership discussions
- Collaboration opportunities

### Visual Suggestions for Gamma:
- Clean architecture flowchart (User → Agent 1 ↔️ Agent 2 → Output)
- Performance metrics in simple cards
- Use case icons
- Terminal command in code block style

---

## GAMMA.APP PRODUCTION GUIDE

### Step-by-Step Instructions:

1. **Go to gamma.app** → Sign in → "Create new"

2. **Choose "Paste in text"** → Paste each slide's content

3. **Select Theme:**
   - Recommended: "Midnight" (professional) or "Ink" (minimal)
   - Avoid: Overly colorful or playful themes

4. **AI Generation Prompt for Gamma:**
   ```
   "Create a 3-slide technical pitch deck for Auto-Sora. Use clean, professional aesthetic:
   - Minimal text, maximum clarity
   - Technical diagrams for Slide 2 and 3
   - Neutral color palette (blue/gray)
   - Code blocks in monospace font
   - 70% visual, 30% text balance
   - Professional, understated design"
   ```

5. **Customization:**
   - **Slide 1**: Simple problem illustration
   - **Slide 2**: Dialogue flow diagram + Web UI screenshot
   - **Slide 3**: Architecture diagram + metrics

6. **Export:**
   - PDF for judges
   - Web link for sharing

### Presentation Flow (4 minutes):

**Slide 1 (90 sec)**: The problem
- "Sora is powerful, but most users struggle with prompting"
- Explain the expertise gap simply
- Transition: "We built a system that automates this expertise"

**Slide 2 (90 sec)**: The solution
- "Two AI agents collaborate autonomously"
- Key point: "Sam Altman is our demo—you can use any persona"
- Show example prompt output

**Slide 3 (60 sec)**: Technical details + demo
- Brief architecture overview
- Performance metrics (3 min, $0.45)
- Show live demo or screenshot
- "We're open to feedback and collaboration"

---

## ONE-LINER PITCH

**Technical version:**
"Auto-Sora uses L4 autonomous dialogue between two AI agents to generate professional Sora prompts from simple ideas."

**Analogy version:**
"Like pair programming for video prompts—two AIs debate until they produce cinema-quality output."

Use when:
- Quick introduction to judges
- Networking conversations
- Social media posts

---

## VISUAL ASSETS CHECKLIST

Prepare these for optimal Gamma results:

1. **Web UI screenshot**: Show the agent dialogue interface
2. **Architecture diagram**: Simple flowchart showing system components
3. **Example prompt comparison**: Before (simple) vs After (detailed)
4. **Persona flexibility visual**: Show multiple personas (not just Sam)

Keep visuals clean and minimal—let the content speak for itself.

---

## JUDGE Q&A PREPARATION

**Q: Why two AIs instead of one?**
A: Dialogue creates iterative refinement. One AI generates, the other critiques and improves. Our testing shows more detailed and technically accurate prompts compared to single-shot generation.

**Q: Why Sam Altman as the persona?**
A: He's our showcase example. The system is persona-agnostic—users can define any creative voice: Spielberg, their brand, their CEO, etc.

**Q: What if Sora API isn't available?**
A: System works with any text-to-video model. We've tested with Runway and Pika. Sora is the target but not a dependency.

**Q: How do you ensure prompt quality?**
A: Expert agent is grounded in 200+ high-performing prompts. Creative agent uses controlled temperature (0.8) to balance creativity with coherence.

**Q: Business model?**
A: Freemium model similar to other AI tools. Free tier for testing, paid tiers for production use. Focus is on demonstrating technical capability first.

**Q: Open source?**
A: Considering options. Current focus is proving the concept and gathering feedback.

---

## PRESENTATION TIPS

**Do:**
- Speak calmly and clearly
- Let the system speak for itself
- Emphasize technical innovation (L4, role flipping)
- Show real output examples
- Be open about limitations

**Don't:**
- Overhype or exaggerate
- Make unsupported claims
- Rush through technical details
- Ignore questions or deflect

**Remember:**
Good engineering speaks louder than marketing hype. Focus on what works.
