# 🧠 Brain — Architecture Guide

## How It Works

The Brain is a multi-agent orchestrator based on Howard Gardner's **Theory of Multiple Intelligences**. Instead of asking one LLM to answer a question, it asks **9 specialized agents** in parallel, then **synthesizes** their responses into a single integrated concept.

## Flow

```
User Question
    │
    ▼
┌─────────────────────────────────────┐
│         orchestrator.py             │
│   ┌─────────────────────────────┐  │
│   │  1. Parse question (CLI)    │  │
│   │  2. Fire 9 parallel API     │  │
│   │     calls (asyncio)         │  │
│   │  3. Collect responses       │  │
│   │  4. Fire synthesis call     │  │
│   │  5. Print + save to JSON    │  │
│   └─────────────────────────────┘  │
└──────────┬──────────┬──────────────┘
           │          │
           ▼          ▼
    ┌──────────┐  ┌──────────┐
    │ Agent 1  │  │ Agent 2  │  ... 9 agents
    │ Linguistic│  │ Logical  │      in parallel
    │ soul.md  │  │ soul.md  │
    └──────────┘  └──────────┘
           │          │
           └────┬─────┘
                ▼
    ┌──────────────────────┐
    │   SYNTHESIS CALL     │
    │  Creates NEW concept │
    │  from all responses  │
    └──────────────────────┘
                │
                ▼
         Final Output
```

## Key Components

### 1. Orchestrator (`orchestrator.py`)

The main script. It:
- Reads a question from the CLI arguments
- Loads each intelligence's `soul.md` and `agent.md`
- Makes 9 concurrent HTTP requests to the LLM API
- Each request uses the intelligence's soul as its **system prompt**
- Aggregates all responses
- Makes a **final synthesis request** that creates a new, integrated concept

### 2. Souls (`intelligences/<id>/soul.md`)

Each soul is a **personality profile** — a complete description of how that intelligence sees the world. It includes:
- **Self-concept**: "I see the world through words..."
- **Response style**: how it formulates answers
- **What it does NOT do**: boundaries of its perspective

### 3. Agents (`intelligences/<id>/agent.md`)

Technical configuration for each agent:
- `temperature`: controls creativity (0.3 for analytical, 0.9 for creative)
- `response_style`: qualitative description of expected output
- Quality checkboxes for self-evaluation

### 4. Synthesis Prompt

A separate system prompt for the final LLM call that:
- Does **NOT** summarize individual responses
- Instead, **digests** all perspectives and **creates a new concept**
- The output must be self-contained and autonomous
- Handles contradictions by showing they can coexist at different analysis levels

## Why Parallel?

- **Synergy**: 9 responses in ~2 minutes (not 18 minutes sequential)
- **Independence**: Each agent has its own temperature and context
- **Bass Model**: Each intelligence is unbiased by the others' responses
- **Resilience**: If one agent times out, the synthesis still works with 8

## Model Compatibility

The system works with any OpenAI-compatible Chat Completions API:

| Provider | URL | Model tested |
|----------|-----|-------------|
| OpenCode Go | `https://opencode.ai/zen/go/v1` | deepseek-v4-flash |
| OpenAI | `https://api.openai.com/v1` | gpt-4o |
| OpenRouter | `https://openrouter.ai/api/v1` | various |

### Reasoning Models (deepseek-v4-flash, etc.)

These models output a `reasoning_content` field (chain-of-thought) before the final `content`. The orchestrator handles this:
- Uses `max_tokens: 16000` to give room for both reasoning and response
- Falls back to `reasoning_content` if `content` is empty
- Strips chain-of-thought preamble from `content` if the model leaks it
- Reports if a response was truncated (`finish_reason: "length"`)

## Adding a New Intelligence

```bash
mkdir intelligences/my-intelligence
```

**soul.md** — who they are:
```markdown
# 🌟 My Intelligence

## Soul

I see the world through...

## How I respond

...
```

**agent.md** — how they behave:
```markdown
temperature: 0.7
max_tokens: 16000
response_style: descriptive
```

Then register in `orchestrator.py`:
```python
INTELLIGENCE_ORDER.append("my-intelligence")
INTELLIGENCE_NAMES["my-intelligence"] = "🌟 My Intelligence"
TEMPERATURES["my-intelligence"] = 0.7
```

## File Structure

```
brain/
├── orchestrator.py          # Main script
├── intelligences/           # Agent configurations
│   └── <id>/
│       ├── soul.md          # Personality & worldview
│       └── agent.md         # Technical configuration
├── references/              # Documentation
├── examples/                # Example outputs
├── responses/               # Saved sessions (gitignored)
├── requirements.txt         # Dependencies
├── .env.example             # Configuration template
└── README.md                # This file
```

## Output Format

Each run saves a JSON file to `responses/session_<timestamp>.json`:

```json
{
  "question": "What is consciousness?",
  "model": "deepseek-v4-flash",
  "elapsed_seconds": 105.1,
  "intelligences": {
    "linguistic": {
      "name": "🧠 Linguistic",
      "response": "Consciousness is...",
      "elapsed": "16.9s",
      "status": "ok",
      "truncated": false
    },
    ...
  },
  "synthesis": "The integrated concept..."
}
```
