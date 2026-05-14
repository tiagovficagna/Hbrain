## I built an open-source AI system based on Howard Gardner's Theory of Multiple Intelligences — and it produces genuinely novel concepts

I'm a PhD in Design and a university professor working at the intersection of AI and cognitive science. I've been thinking about a question for a while: *what if instead of asking one AI to answer a question, we asked 9 specialized agents — each embodying a different form of intelligence — and then synthesized their perspectives into something new?*

So I built it.

<https://github.com/tiagovficagna/Hbrain>

### The architecture

Hbrain is an asyncio-based orchestrator that fires the same question to 9 parallel LLM agents, each with its own **soul.md** — a complete personality profile based on Gardner's framework:

- **Linguistic** — sees the world through words, narrative, metaphor
- **Logical-Mathematical** — decomposes everything into patterns, systems, causality
- **Spatial** — visualizes concepts as 3D structures, landscapes, architecture
- **Bodily-Kinesthetic** — translates ideas into movement, touch, physical sensation
- **Musical** — hears rhythm, harmony, and frequency in every phenomenon
- **Interpersonal** — understands everything through relationships and communication
- **Intrapersonal** — reflects inward, connecting concepts to subjective experience
- **Naturalistic** — traces evolutionary histories, ecological relationships, growth cycles
- **Existential** — sits at the frontier of thought, connecting any question to meaning, finitude, and transcendence

All 9 run in parallel via asyncio (~2 min total). Then a **synthesis call** — and this is the key — does NOT summarize the responses. Instead, it digests all 9 perspectives and **creates a genuinely new concept** that only exists when they converge.

### Why this matters beyond the novelty

What I find interesting is that each intelligence biases the model toward different features of the same phenomenon. Ask "what is a synapse?" and:

- The **linguistic** agent traces the etymology (*syn-haptein* = "to grasp together") and describes the synaptic cleft as a comma in the body's discourse
- The **logical-mathematical** agent formalizes it as a weighted computation node with threshold activation functions
- The **spatial** agent draws the micro-architecture — vesicles as cargo ships, receptors as docking bays
- The **musical** agent hears polyrhythm in temporal and spatial summation
- The **existential** agent sits with the question of how matter becomes meaning at that 20nm gap

The synthesis that emerges from all 9 isn't a collage — it reads as one coherent, original idea. From the synapse example:

> *"The synapse is not the point of contact between neurons — it is the interval that makes connection meaningful. It is the active void where continuity is deliberately fractured so the signal gains depth, ambiguity, and creative power..."*

### Some early outputs

I've been testing with deeply conceptual questions. The system seems to shine when the question has enough density to sustain 9 different lenses:

- **"What is gravity?"** → 54s synthesis
- **"What is time?"** → 127s synthesis 
- **"What is a synapse?"** → 105s synthesis
- **"What is consciousness?"** → (your question could be next)

### Tech details

- Python 3.10+, asyncio + aiohttp
- Works with any OpenAI-compatible API (I use deepseek-v4-flash via OpenCode Go — pay per request, about $0.001 per run)
- MIT License
- Each intelligence is fully customizable — you can add new ones with just a soul.md and agent.md file
- Full Mermaid diagrams and documentation in the README

### Questions I've been sitting with

- Could this approach be used in education — helping students see a concept from multiple cognitive angles?
- Does the synthesis actually produce something that no single agent would say alone?
- What would it look like to feed the synthesis *back* into the agents for iterative deepening?

I'd love feedback, ideas, or contributions. The codebase is small (~500 lines of Python) and intentionally simple — the complexity is in the souls, not the infrastructure.

<https://github.com/tiagovficagna/Hbrain>

---

*PhD in Design. Professor. I believe the best way to understand something is to look at it from every possible angle.*
