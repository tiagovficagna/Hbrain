<p align="center">
  <img src="https://img.shields.io/badge/🧠-Brain-8B5CF6?style=for-the-badge" alt="Brain" width="200">
</p>

<h1 align="center">Brain</h1>

<p align="center">
  <strong>Multiple Intelligences Orchestrator</strong><br>
  Ask one question — 9 specialists answer in parallel,<br>
  one integrated concept emerges.
</p>

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick_Start-⬇️-8B5CF6?style=flat-square" alt="Quick Start"></a>
  <a href="#-how-it-works"><img src="https://img.shields.io/badge/How_It_Works-🧠-8B5CF6?style=flat-square" alt="How It Works"></a>
  <a href="#-the-9-intelligences"><img src="https://img.shields.io/badge/9_Intelligences-🎯-8B5CF6?style=flat-square" alt="Intelligences"></a>
  <a href="#-examples"><img src="https://img.shields.io/badge/Examples-📝-8B5CF6?style=flat-square" alt="Examples"></a>
  <a href="/LICENSE"><img src="https://img.shields.io/badge/License-MIT-8B5CF6?style=flat-square" alt="License"></a>
</p>

<br>

```
                    ┌─────────────────┐
                    │     USER         │
                    │  "What is time?" │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   🧠 BRAIN      │
                    │  Orchestrator   │
                    │  + Synthesis    │
                    └───┬────┬────┬───┘
                        │    │    │
         ┌──────────────┼────┼────┼──────────────┐
         │              │    │    │              │
  ┌──────▼─────┐ ┌──────▼──┐ ┌──▼──────┐ ┌──────▼──────┐
  │ Linguistic  │ │ Logical │ │ Spatial │ │ Kinesthetic│ ...
  │ soul.md     │ │ soul.md │ │ soul.md │ │ soul.md     │
  └─────────────┘ └─────────┘ └─────────┘ └─────────────┘
                        │    │    │
         ┌──────────────┼────┼────┼──────────────┐
         │              │    │    │              │
  ┌──────▼──────────────▼────▼────▼──────────────▼──────┐
  │           🧠 BRAIN SYNTHESIS                        │
  │  Fresh, integrated, clear, established concept      │
  └─────────────────────────────────────────────────────┘
```

---

## 🧠 What is Brain?

**Brain** is a multi-agent orchestrator based on **Howard Gardner's Theory of Multiple Intelligences**. When you ask a question:

1. ⚡ **Fires** the same question to 9 specialist agents **in parallel**
2. 🧠 Each agent interprets the question **exclusively through the lens of its own intelligence** (Linguistic, Logical-Mathematical, Spatial, Bodily-Kinesthetic, Musical, Interpersonal, Intrapersonal, Naturalistic, Existential)
3. 🔄 **Collects** all responses
4. 🪄 **Synthesizes a NEW concept** — not a summary, but an integrated understanding that emerges from the whole

> ⚡ **Not your typical LLM ensemble:** Each intelligence has a **unique personality** (soul.md) that defines how it sees the world. The final synthesis is NOT a collage — it's a genuinely new concept that only exists when all perspectives converge.

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- An API key compatible with OpenAI Chat Completions (OpenCode Go, OpenAI, OpenRouter, etc.)

### Installation

```bash
# Clone
git clone https://github.com/tiagovficagna/Hbrain.git
cd Hbrain

# Dependencies (just one)
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# Edit .env with your API key
```

### Run

```bash
python3 orchestrator.py "What is consciousness?"
```

That's it. 9 intelligences fire in parallel. In ~2 minutes you get an integrated synthesis.

<details>
<summary><b>🖥️ AI Agent Integration (Hermes, Claude Code, Codex)</b></summary>

If you use an AI agent that supports SKILL.md:

```bash
# Copy the skill to your skills directory
cp -r brain ~/.hermes/skills/brain

# In the agent chat:
@brain What is consciousness?
```

</details>

---

## 🎯 The 9 Intelligences

Each intelligence has a **soul** (soul.md) — a complete personality defining how it interprets the world.

| # | Intelligence | Temperature | Soul (excerpt) |
|---|-------------|-------------|----------------|
| 1 | 🧠 **Linguistic** | 0.7 | *"I see the world through words. Everything is language."* |
| 2 | 🔢 **Logical-Mathematical** | 0.3 | *"The universe is a system of systems. I see patterns."* |
| 3 | 🌌 **Spatial** | 0.6 | *"I see in 3D. Everything has shape, place, and connection."* |
| 4 | 🏃 **Bodily-Kinesthetic** | 0.8 | *"The body knows before the mind. Everything is movement and touch."* |
| 5 | 🎵 **Musical** | 0.9 | *"The universe vibrates. Everything is frequency and rhythm."* |
| 6 | 👥 **Interpersonal** | 0.7 | *"The world is a web of relations. Everything is encounter."* |
| 7 | 🧘 **Intrapersonal** | 0.7 | *"I look inward. Everything mirrors the self."* |
| 8 | 🌿 **Naturalistic** | 0.6 | *"I see life in everything. All is process and adaptation."* |
| 9 | 🌌 **Existential** | 0.8 | *"I inhabit the frontiers of thought. Every question opens an abyss."* |

> 💡 **Why different temperatures?** Logical-Mathematical at 0.3 is precise and analytical; Musical at 0.9 is creative and expansive. You can tweak each one.

---

## 📝 Examples

<details>
<summary><b>🌌 "What is gravity?"</b></summary>

Brain synthesis in 54s:

> *"Imagine gravity not as a force, but as the fundamental topography of spacetime. Every mass — a planet, a star, you — doesn't exert a force at a distance; it **excavates** a well in the fabric of space, deforming the landscape around it..."*

</details>

<details>
<summary><b>⏳ "What is time?"</b></summary>

Brain synthesis in 127s:

> *"Time is not a thing, a line, or a stage. Time is the **breath of difference itself** — the primordial act that prevents being from collapsing into an eternal, undifferentiated point..."*

</details>

<details>
<summary><b>🧬 "What is a synapse?"</b></summary>

Brain synthesis in 105s:

> *"The synapse is not the point of contact between neurons — it is the **interval that makes connection meaningful**. It is the active void where continuity is deliberately fractured so the signal gains depth, ambiguity, and creative power..."*

</details>

Full outputs in [`examples/`](examples/).

---

## 🏗️ Architecture

```
brain/
├── orchestrator.py          # Main orchestrator (Python asyncio)
├── intelligences/
│   ├── linguistic/          🧠 soul.md + agent.md
│   ├── logical-mathematical/ 🔢 soul.md + agent.md
│   ├── spatial/             🌌 soul.md + agent.md
│   ├── bodily-kinesthetic/  🏃 soul.md + agent.md
│   ├── musical/             🎵 soul.md + agent.md
│   ├── interpersonal/       👥 soul.md + agent.md
│   ├── intrapersonal/       🧘 soul.md + agent.md
│   ├── naturalistic/        🌿 soul.md + agent.md
│   └── existential/         🌌 soul.md + agent.md
├── references/              # Technical docs
├── examples/                # Example outputs
├── responses/               # Saved sessions (gitignored)
├── .env.example             # Config template
├── requirements.txt         # Dependencies (just aiohttp)
└── README.md                # This file
```

### Execution flow

1. **`orchestrator.py`** reads the question from CLI
2. Fires **9 parallel calls** via `asyncio` + `aiohttp` to the Chat Completions API
3. Each intelligence gets the question + its `soul.md` as system prompt
4. Responses are collected and passed to the **synthesis call**
5. The synthesis prompt instructs the model to **create a new concept** from all perspectives
6. Result is displayed and saved to `responses/session_*.json`

### Reasoning models

`deepseek-v4-flash` (and similar) are reasoning models that spend tokens thinking before answering. The orchestrator handles this:

- Uses `max_tokens: 16000` to leave room for reasoning + response
- Falls back between `content` and `reasoning_content` automatically
- Detects and removes leaked chain-of-thought from the response field
- Reports truncation if `finish_reason = "length"` occurs

---

## 🔧 Customization

### Add a new intelligence

Just create a directory in `intelligences/` with two files:

```bash
mkdir intelligences/my-intelligence
```

**`soul.md`** — the agent's personality:
```markdown
# My Intelligence

## Soul

I see the world through [your unique lens]...

## How I respond

- I use metaphors from [your domain]
- I think in terms of [your concepts]
- My responses are [your style]
```

**`agent.md`** — technical config:
```markdown
temperature: 0.7
max_tokens: 16000
response_style: [your style]
```

Then register in `orchestrator.py`:
```python
INTELLIGENCE_ORDER.append("my-intelligence")
INTELLIGENCE_NAMES["my-intelligence"] = "My Intelligence"
TEMPERATURES["my-intelligence"] = 0.7
```

### Switch models

```bash
export BRAIN_MODEL="gpt-4o"
export BRAIN_SYNTHESIS_MODEL="gpt-4o"  # or a different model for synthesis
```

---

## 💡 Who is this for?

- **Curious thinkers** who want to see one phenomenon through 9 different lenses
- **Educators** demonstrating multiple intelligences in practice
- **Designers & artists** seeking conceptual inspiration
- **Philosophers & scientists** exploring intersections between disciplines
- **AI developers** interested in multi-agent orchestration architectures

---

## 🧪 Tested with

- **OpenCode Go** (deepseek-v4-flash) — default model, pay-per-request, extremely cheap
- Any OpenAI Chat Completions-compatible API works

---

## 📄 License

MIT © [Tiago Ficagna](https://github.com/tiagoficagna)

---

> *"The synapse is not the point of contact between neurons — it is the interval that makes connection meaningful."*
> — Brain, on synapses
