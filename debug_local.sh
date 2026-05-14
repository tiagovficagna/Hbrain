#!/bin/bash
# Debug: roda 1 agente no modelo 1.7B e mostra erro completo
export BRAIN_MODEL="qwen3-1.7b"
export BRAIN_SYNTHESIS_MODEL="qwen3-1.7b"
export OPENCODE_BASE_URL="http://localhost:1234/v1"
export OPENCODE_GO_API_KEY="not-needed"
export BRAIN_AGENT_TIMEOUT="120"
export BRAIN_AGENT_MAX_TOKENS="4000"
export BRAIN_AGENTS="linguistic"

cd "$(dirname "$0")"

python3 -c "
import sys, os, json, traceback, asyncio, aiohttp
sys.path.insert(0, '.')

from orchestrator import INTELLIGENCE_ORDER, INTELLIGENCE_NAMES, TEMPERATURES, INTELLIGENCE_EMOJIS, MODEL, BASE_URL, AGENT_MAX_TOKENS, AGENT_TIMEOUT, call_intelligence, load_soul

print(f'Agentes: {INTELLIGENCE_ORDER}')
print(f'Modelo: {MODEL}')
print(f'Timeout: {AGENT_TIMEOUT}s')
print(f'Max tokens: {AGENT_MAX_TOKENS}')
print()

async def test():
    headers = {'Authorization': f'Bearer {os.environ.get(\"OPENCODE_GO_API_KEY\", \"\")}', 'Content-Type': 'application/json'}
    async with aiohttp.ClientSession(headers=headers) as session:
        result = await call_intelligence(session, 'linguistic', 'What is gravity?')
        print(json.dumps(result, indent=2, ensure_ascii=False))

asyncio.run(test())
" "$@" 2>&1
