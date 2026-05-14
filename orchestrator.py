#!/usr/bin/env python3
"""
BRAIN ORCHESTRATOR v1.1
========================
Orquestrador multi-agente baseado na Teoria das Inteligências Múltiplas
de Howard Gardner.

Fluxo:
  1. Recebe uma pergunta via argumento CLI
  2. Dispara chamadas paralelas para 9 "inteligências" (cada uma com seu soul.md)
  3. Coleta respostas
  4. Dispara chamada de SÍNTESE — cria um conceito NOVO e integrado
  5. Retorna resultado final
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import aiohttp
except ImportError:
    print("aiohttp não instalado. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp", "-q"])
    import aiohttp

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda p: None


# ─── Configuração ────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent.resolve()
INTELLIGENCES_DIR = SKILL_DIR / "intelligences"

# Tenta carregar .env de múltiplos locais (prioridade: local > home)
for env_candidate in [
    SKILL_DIR / ".env",                         # Local (projeto)
    Path.cwd() / ".env",                        # Working directory
    Path.home() / ".hermes" / ".env",           # Hermes agent
    Path.home() / ".env",                       # Home
]:
    if env_candidate.exists():
        load_dotenv(env_candidate)
        break

API_KEY = (
    os.environ.get("OPENCODE_GO_API_KEY")
    or os.environ.get("OPENCODE_ZEN_API_KEY")
    or os.environ.get("OPENAI_API_KEY")
)
BASE_URL = os.environ.get("OPENCODE_BASE_URL", "https://opencode.ai/zen/go/v1")
MODEL = os.environ.get("BRAIN_MODEL", "deepseek-v4-flash")
SYNTHESIS_MODEL = os.environ.get("BRAIN_SYNTHESIS_MODEL", MODEL)

# Temperatura por inteligência (algumas pedem mais criatividade, outras mais precisão)
TEMPERATURES = {
    "linguistic": 0.7,
    "logical-mathematical": 0.3,
    "spatial": 0.6,
    "bodily-kinesthetic": 0.8,
    "musical": 0.9,
    "interpersonal": 0.7,
    "intrapersonal": 0.7,
    "naturalistic": 0.6,
    "existential": 0.8,
}

# Nomes amigáveis para exibição
INTELLIGENCE_NAMES = {
    "linguistic": "Linguística (Verbal)",
    "logical-mathematical": "Lógico-Matemática",
    "spatial": "Espacial",
    "bodily-kinesthetic": "Corporal-Cinestésica",
    "musical": "Musical",
    "interpersonal": "Interpessoal",
    "intrapersonal": "Intrapessoal",
    "naturalistic": "Naturalista",
    "existential": "Existencial",
}

INTELLIGENCE_ORDER = [
    "linguistic", "logical-mathematical", "spatial", "bodily-kinesthetic",
    "musical", "interpersonal", "intrapersonal", "naturalistic", "existential"
]

# Emojis para exibição
INTELLIGENCE_EMOJIS = {
    "linguistic": "🧠",
    "logical-mathematical": "🔢",
    "spatial": "🌌",
    "bodily-kinesthetic": "🏃",
    "musical": "🎵",
    "interpersonal": "👥",
    "intrapersonal": "🧘",
    "naturalistic": "🌿",
    "existential": "🌌",
}

# Timeouts configuráveis via env var (útil para modelos locais lentos)
# Max tokens configuráveis via env var (reduzir para modelos locais lentos)
AGENT_MAX_TOKENS = int(os.environ.get("BRAIN_AGENT_MAX_TOKENS", "16000"))
SYNTHESIS_MAX_TOKENS = int(os.environ.get("BRAIN_SYNTHESIS_MAX_TOKENS", "16000"))
AGENT_TIMEOUT = int(os.environ.get("BRAIN_AGENT_TIMEOUT", "90"))
SYNTHESIS_TIMEOUT = int(os.environ.get("BRAIN_SYNTHESIS_TIMEOUT", "180"))

# Permite rodar com subset de agentes (ex: BRAIN_AGENTS=linguistic,spatial,existential)
_ENV_AGENTS = os.environ.get("BRAIN_AGENTS", "")
if _ENV_AGENTS:
    _filtered = [a.strip() for a in _ENV_AGENTS.split(",") if a.strip() in INTELLIGENCE_ORDER]
    if _filtered:
        INTELLIGENCE_ORDER = _filtered

# Modo sequencial: roda um agente de cada vez (útil para modelos locais lentos)
SEQUENTIAL = os.environ.get("BRAIN_SEQUENTIAL", "").lower() in ("1", "true", "yes", "sim")


# ─── Utilitários ────────────────────────────────────────────────────────────

def load_soul(intelligence_id: str) -> str:
    """Carrega o soul.md de uma inteligência."""
    path = INTELLIGENCES_DIR / intelligence_id / "soul.md"
    if not path.exists():
        return f"[Soul não encontrado para {intelligence_id}]"
    return path.read_text(encoding="utf-8").strip()


# ─── Chamada LLM ────────────────────────────────────────────────────────────

def build_headers() -> dict:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def extract_content(msg: dict) -> tuple[str, str]:
    """Extrai conteúdo da mensagem, lidando com modelos de raciocínio.

    O deepseek-v4-flash é um modelo de raciocínio que separa o pensamento
    (reasoning_content) da resposta final (content). Mas às vezes o modelo
    coloca o raciocínio no content também. Esta função lida com todos os casos.

    Returns: (resposta_limpa, finish_reason)
    """
    content = (msg.get("content") or "").strip()
    reasoning = (msg.get("reasoning_content") or "").strip()
    finish_reason = msg.get("finish_reason", "stop")

    # ─── Estratégia 1: content limpo, reasoning separado ─────────────────
    # Se content não parece ser chain-of-thought, é a resposta real
    if content and not _looks_like_cot(content):
        return content, finish_reason

    # ─── Estratégia 2: content vazio, reasoning tem a resposta ──────────
    if not content and reasoning:
        return reasoning, finish_reason

    # ─── Estratégia 3: content tem CoT misturado com resposta ──────────
    # Tenta separar o raciocínio da resposta real
    result = _strip_cot_from_content(content)
    if result:
        return result, finish_reason

    # ─── Estratégia 4: fallback — reasoning pode ter resposta melhor ───
    if reasoning and len(reasoning) > 200:
        return reasoning, finish_reason

    # ─── Último caso: devolve content mesmo que pareça CoT ─────────────
    return content if content else "[resposta vazia]", finish_reason


def _looks_like_cot(text: str) -> bool:
    """Detecta se um texto parece ser chain-of-thought (raciocínio interno)."""
    # Normaliza para comparação
    lower = text.lower().strip()

    # Padrões de abertura de chain-of-thought
    cot_openers = [
        "thinking", "analyze the request", "deconstruct",
        "brainstorming", "drafting the structure", "let me",
        "key points", "paragraph 1", "structure:",
    ]
    for opener in cot_openers:
        if lower.startswith(opener):
            return True

    # Se tem marcadores de planejamento no início, é CoT
    return False


def _strip_cot_from_content(text: str) -> str | None:
    """Tenta extrair a resposta real de um texto que começa com CoT.

    Estratégia: procura por seções que claramente NÃO são chain-of-thought.
    O CoT tem marcadores característicos como bullets, numeração, linguagem
    de planejamento. A resposta real tem parágrafos contínuos.
    """
    if not text:
        return None

    lines = text.split("\n")

    # ─── Abordagem 1: Marcadores de transição explícitos ───────────────
    # Procura por linhas que marcam explicitamente o início da resposta
    response_markers = [
        "**response**", "**answer**", "**final answer**",
        "**paragraph 1**", "**paragraph 2**", "**paragraph 3**",
        "**parágrafo 1**", "**parágrafo 2**", "**parágrafo 3**",
        # Variações com : e sem ** no final
        "**response", "**answer", "**paragraph 1", "**paragraph 2",
        "**paragraph 3", "**parágrafo 1", "**parágrafo 2", "**parágrafo 3",
        "**final answer",
    ]

    for i, line in enumerate(lines):
        stripped = line.strip().lower()
        for marker in response_markers:
            if marker in stripped:
                # Pula a linha do marcador e pega o que vem depois
                candidate = "\n".join(lines[i+1:]).strip()
                if len(candidate) >= 60:
                    return candidate

    # ─── Abordagem 2: Primeiro parágrafo substancial não-CoT ──────────
    # Pula todas as linhas que parecem ser de planejamento/análise
    # e pega o primeiro bloco de texto corrido
    in_cot = True
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        if in_cot:
            # Verifica se ainda estamos no CoT
            lower = stripped.lower()
            is_cot_line = (
                stripped.startswith(("*", "-", "•", "1.", "2.", "3.", "4.", "5.", "6."))
                or any(w in lower for w in ["analyze", "paragraph", "draft",
                    "structure", "step", "constraint", "approach", "outline"])
                or len(stripped) < 40
            )
            if not is_cot_line and len(stripped) > 40:
                # Achou o início da resposta real
                candidate = "\n".join(lines[i:]).strip()
                if len(candidate) > 80:
                    return candidate
                else:
                    in_cot = False  # Era falso alarme, continua
        else:
            # Já passamos do CoT, coleta o que falta
            candidate = "\n".join(lines[i:]).strip()
            if len(candidate) > 80:
                return candidate

    # ─── Abordagem 3: Fallback — último bloco grande ───────────────────
    blocks = [b.strip() for b in text.split("\n\n") if len(b.strip()) > 150]
    if blocks:
        return blocks[-1]

    return None


async def call_intelligence(
    session: aiohttp.ClientSession,
    intelligence_id: str,
    question: str,
) -> dict:
    """Chama uma inteligência específica."""
    soul = load_soul(intelligence_id)
    temperature = TEMPERATURES.get(intelligence_id, 0.7)
    name = INTELLIGENCE_NAMES[intelligence_id]
    emoji = INTELLIGENCE_EMOJIS.get(intelligence_id, "🧠")

    system_prompt = (
        f"Você é um especialista que enxerga o mundo através da "
        f"inteligência {name} da "
        f"Teoria das Inteligências Múltiplas de Howard Gardner.\n\n"
        f"SUA PERSONALIDADE:\n{soul}\n\n"
        f"REGRAS:\n"
        f"1. Interprete a pergunta do usuário EXCLUSIVAMENTE através da lente "
        f"da sua inteligência.\n"
        f"2. Seja profundo, específico e use a linguagem e metáforas "
        f"características da sua forma de pensar.\n"
        f"3. NÃO tente responder de forma genérica — sua perspectiva única "
        f"é o que importa.\n"
        f"4. Escreva entre 3-6 parágrafos densos e interessantes.\n"
        f"5. Contexto vital: você é um dos 9 especialistas sendo consultados "
        f"em paralelo. Sua resposta será integrada com as outras em uma "
        f"síntese. Seja fiel à sua inteligência.\n"
        f"6. ⚠️ NÃO inclua seu raciocínio interno (chain-of-thought) na "
        f"resposta. Não comece com 'Thinking', 'Analyze', 'Deconstruct' ou "
        f"qualquer análise do processo. Escreva APENAS a resposta final "
        f"diretamente, em parágrafos fluentes."
    )

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "temperature": temperature,
        "max_tokens": AGENT_MAX_TOKENS,
    }

    start = time.monotonic()
    try:
        async with session.post(
            f"{BASE_URL}/chat/completions",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=AGENT_TIMEOUT)
        ) as resp:
            elapsed = time.monotonic() - start
            data = await resp.json()

            if resp.status != 200:
                return {
                    "id": intelligence_id,
                    "name": f"{emoji} {name}",
                    "response": f"[Erro {resp.status}]: {data.get('error', {}).get('message', str(data)[:200])}",
                    "elapsed": f"{elapsed:.1f}s",
                    "status": "error",
                }

            content, finish_reason = extract_content(data["choices"][0]["message"])

            # Se finish_reason == "length" significa que o modelo não conseguiu
            # completar a resposta — ainda assim entregamos o que temos
            truncated_note = ""
            if finish_reason == "length":
                truncated_note = " [⚠️ truncado — max_tokens insuficiente]"

            return {
                "id": intelligence_id,
                "name": f"{emoji} {name}",
                "response": content,
                "elapsed": f"{elapsed:.1f}s",
                "status": "ok",
                "truncated": finish_reason == "length",
            }
    except asyncio.TimeoutError:
        return {
            "id": intelligence_id,
            "name": f"{emoji} {name}",
            "response": "[Timeout após 90s]",
            "elapsed": "90.0s+",
            "status": "timeout",
        }
    except Exception as e:
        return {
            "id": intelligence_id,
            "name": f"{emoji} {name}",
            "response": f"[Erro: {str(e)[:200]}]",
            "elapsed": "-",
            "status": "error",
        }


async def synthesize(
    session: aiohttp.ClientSession,
    question: str,
    responses: list[dict],
) -> str:
    """Chamada de SÍNTESE integrativa."""
    # Monta o contexto com todas as respostas
    sections = [f"PERGUNTA ORIGINAL:\n{question}\n"]
    sections.append("=" * 60)
    sections.append("RESPOSTAS DOS 9 ESPECIALISTAS:")
    sections.append("=" * 60)
    sections.append("")

    for r in responses:
        if r["status"] == "ok":
            sections.append(f"--- {r['name']} ({r['elapsed']}) ---")
            sections.append(r["response"])
            sections.append("")

    context = "\n".join(sections)

    synthesis_prompt = (
        "Você é o BRAIN — uma inteligência integrativa e sintetizadora. "
        "Sua função NÃO é resumir as respostas dos especialistas, mas sim "
        "DIGERIR todas as perspectivas e CRIAR um conceito NOVO, claro e "
        "profundo que emerge da integração delas.\n\n"
        "REGRAS:\n"
        "1. NÃO faça um resumo de cada inteligência.\n"
        "2. NÃO liste as perspectivas uma por uma.\n"
        "3. Absorva cada ângulo e PRODUZA UMA COMPREENSÃO ÚNICA "
        "que não existiria sem todas elas juntas.\n"
        "4. O resultado deve ser um CONCEITO CLARO, ESTABELECIDO e AUTÔNOMO "
        "— não um mosaico de citações.\n"
        "5. Use linguagem rica, fluida e integradora. O leitor deve sentir "
        "que recebeu uma VISÃO COMPLETA.\n"
        "6. Se houver contradições, resolva-as no nível conceitual — "
        "mostre como ambas podem ser verdade em diferentes níveis de análise.\n\n"
        "ESTRUTURA SUGERIDA:\n"
        "- Abertura: uma frase/parágrafo que captura a essência do conceito integrado\n"
        "- Desenvolvimento: aprofunda, tecendo os fios de cada inteligência "
        "em um tecido único (sem nomear as fontes)\n"
        "- Fechamento: reflexão que conecta ao significado mais amplo — "
        "o que esta compreensão revela sobre a pergunta original\n\n"
        "IMPORTANTE: Sua resposta deve ser AUTÔNOMA. Alguém que ler apenas "
        "a sua síntese deve sentir que entendeu o fenômeno em profundidade."
    )

    payload = {
        "model": SYNTHESIS_MODEL,
        "messages": [
            {"role": "system", "content": synthesis_prompt},
            {"role": "user", "content": context}
        ],
        "temperature": 0.5,
        'max_tokens': SYNTHESIS_MAX_TOKENS,
    }

    try:
        async with session.post(
            f'{BASE_URL}/chat/completions',
            json=payload,
            timeout=aiohttp.ClientTimeout(total=SYNTHESIS_TIMEOUT)
        ) as resp:
            data = await resp.json()
            if resp.status != 200:
                return f'[Erro na síntese {resp.status}]: {data.get("error", {}).get("message", str(data)[:200])}'

            msg = data['choices'][0]['message']
            result, finish_reason = extract_content(msg)
            if result == '[resposta vazia]':
                return '[A síntese não conseguiu gerar conteúdo. As respostas das inteligências podem ter sido extensas demais para o contexto máximo.]'
            return result
    except Exception as e:
        return f"[Erro na síntese: {str(e)[:300]}"


# ─── Main ────────────────────────────────────────────────────────────────────

async def main(question: str):
    print(f"\n{'='*60}")
    print(f"🧠 BRAIN — Orquestrador de Inteligências Múltiplas")
    print(f"{'='*60}")
    print(f"📝 Pergunta: {question}")
    print(f"🤖 Modelo: {MODEL}")
    print(f"🌐 API: {BASE_URL}")
    print(f"{'='*60}\n")

    if not API_KEY:
        print("❌ ERRO: OPENCODE_GO_API_KEY não encontrada no .env")
        sys.exit(1)

    mode_str = "em sequência" if SEQUENTIAL else "em paralelo"
    print(f"⏳ Disparando {len(INTELLIGENCE_ORDER)} inteligências {mode_str}...\n")
    start_time = time.monotonic()

    async with aiohttp.ClientSession(headers=build_headers()) as session:
        # Dispara as inteligências
        responses = []
        if SEQUENTIAL:
            for i, intel_id in enumerate(INTELLIGENCE_ORDER):
                print(f"  [{i+1}/{len(INTELLIGENCE_ORDER)}] {INTELLIGENCE_EMOJIS.get(intel_id, '🧠')} {INTELLIGENCE_NAMES[intel_id]}... ", end="", flush=True)
                result = await call_intelligence(session, intel_id, question)
                print(f"({result['elapsed']})")
                responses.append(result)
        else:
            tasks = [
                call_intelligence(session, intel_id, question)
                for intel_id in INTELLIGENCE_ORDER
            ]
            responses = await asyncio.gather(*tasks)

        # Mostra resultados parciais
        print(f"{'─'*60}")
        truncated_count = 0
        for r in responses:
            status_icon = "✅" if r["status"] == "ok" else "❌"
            resp_len = len(r["response"])
            trunc_flag = " ⚠️" if r.get("truncated") else ""
            if r.get("truncated"):
                truncated_count += 1
            status_line = f"  {status_icon} {r['name']}: {r['elapsed']} | {resp_len} chars{trunc_flag}"
            print(status_line)
        print(f"{'─'*60}")
        if truncated_count:
            print(f"  ⚠️  {truncated_count}/9 respostas foram truncadas (max_tokens atingido)")
        print()

        # Síntese
        successful = sum(1 for r in responses if r["status"] == "ok")
        print(f"🧠 BRAIN está sintetizando ({successful}/9 respostas)...\n")
        synthesis = await synthesize(session, question, responses)

        elapsed = time.monotonic() - start_time

        # ─── Output Final ────────────────────────────────────────────────
        print(f"\n{'='*60}")
        print(f"🧠  SÍNTESE DO BRAIN")
        print(f"{'='*60}")
        print(f"📝 {question}")
        print(f"⏱️  {elapsed:.1f}s • {successful}/9 inteligências\n")
        print(synthesis)
        print(f"\n{'─'*60}")
        mode_label = "em sequência" if SEQUENTIAL else "em paralelo"
        print(f"{len(INTELLIGENCE_ORDER)} inteligências consultadas ({mode_label}) • Síntese integrativa • {elapsed:.1f}s")
        print(f"{'='*60}\n")

        # ─── Salva sessão ────────────────────────────────────────────────
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = SKILL_DIR / "responses"
        session_dir.mkdir(exist_ok=True)
        session_file = session_dir / f"session_{timestamp}.json"

        output = {
            "question": question,
            "model": MODEL,
            "timestamp": timestamp,
            "elapsed_seconds": round(elapsed, 1),
            "intelligences": {
                r["id"]: {
                    "name": r["name"],
                    "response": r["response"],
                    "elapsed": r["elapsed"],
                    "status": r["status"],
                    "truncated": r.get("truncated", False),
                }
                for r in responses
            },
            "synthesis": synthesis,
        }

        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"💾 Sessão salva em: {session_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python orchestrator.py \"<sua pergunta>\"")
        print("")
        print("Exemplo: python orchestrator.py \"Como funciona uma sinapse?\"")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    asyncio.run(main(question))
