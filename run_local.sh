#!/bin/bash
# Hbrain local — Qwen3 1.7B via LM Studio, MODO SEQUENCIAL
# Roda as 9 inteligências uma após a outra (mais lento, mas funciona)
# Uso: bash run_local.sh "Sua pergunta"

export BRAIN_MODEL="qwen3-1.7b"
export BRAIN_SYNTHESIS_MODEL="qwen3-1.7b"
export OPENCODE_BASE_URL="http://localhost:1234/v1"
export OPENCODE_GO_API_KEY="not-needed"

# Modo sequencial — 1 agente por vez (cabe em qualquer PC)
export BRAIN_SEQUENTIAL="true"

# Timeouts folgados pra modelo local
export BRAIN_AGENT_TIMEOUT="180"
export BRAIN_SYNTHESIS_TIMEOUT="300"
export BRAIN_AGENT_MAX_TOKENS="8000"
export BRAIN_SYNTHESIS_MAX_TOKENS="8000"

cd "$(dirname "$0")"
python3 orchestrator.py "$@"
