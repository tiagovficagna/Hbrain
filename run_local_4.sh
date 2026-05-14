#!/bin/bash
# Hbrain local runner — Qwen3 1.7B com timeout ajustado
# Uso: bash run_local.sh "Sua pergunta"

export BRAIN_MODEL="qwen3-1.7b"
export BRAIN_SYNTHESIS_MODEL="qwen3-1.7b"
export OPENCODE_BASE_URL="http://localhost:1234/v1"
export OPENCODE_GO_API_KEY="not-needed"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 -c "
import asyncio, sys, os
sys.path.insert(0, '$SCRIPT_DIR')

# Patch: usar só 4 inteligências (cabe no parallel=4 do LM Studio)
from orchestrator import *
import orchestrator as mod

mod.INTELLIGENCE_ORDER = ['linguistic', 'logical-mathematical', 'spatial', 'existential']
mod.INTELLIGENCE_NAMES = {k: v for k, v in mod.INTELLIGENCE_NAMES.items() if k in mod.INTELLIGENCE_ORDER}
mod.TEMPERATURES = {k: v for k, v in mod.TEMPERATURES.items() if k in mod.TEMPERATURES}

asyncio.run(mod.main(' '.join(sys.argv[1:])))
" "$@"
