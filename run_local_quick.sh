#!/bin/bash
# Hbrain local runner — versão rápida com 3 agentes
# Uso: bash run_local_quick.sh "Sua pergunta"

export BRAIN_MODEL="qwen3-1.7b"
export BRAIN_SYNTHESIS_MODEL="qwen3-1.7b"
export OPENCODE_BASE_URL="http://localhost:1234/v1"
export OPENCODE_GO_API_KEY="not-needed"

cd "$(dirname "$0")"

python3 -c "
import asyncio, sys
sys.path.insert(0, '.')

# Quick patch: override to only use 3 agents
from orchestrator import *

# Substitui a ordem pra só 3
import orchestrator as mod
mod.INTELLIGENCE_ORDER = ['linguistic', 'logical-mathematical', 'existential']
mod.INTELLIGENCE_NAMES = {k: v for k, v in mod.INTELLIGENCE_NAMES.items() if k in mod.INTELLIGENCE_ORDER}
mod.TEMPERATURES = {k: v for k, v in mod.TEMPERATURES.items() if k in mod.TEMPERATURES}

asyncio.run(mod.main(' '.join(sys.argv[1:])))
" "$@"
