# DeepSeek V4 Flash — Comportamento de Modelo de Raciocínio

O `deepseek-v4-flash` é um **modelo de raciocínio** (reasoning model). Diferente de modelos tradicionais que geram a resposta diretamente, ele primeiro produz uma cadeia interna de pensamento (`reasoning_content`) e só depois gera a resposta final (`content`).

## ⚠️ Descoberta Crítica (10/05/2026)

**`max_tokens` precisa ser MUITO maior que o esperado.** Com o system prompt completo do Brain (soul.md + instruções, ~2000+ tokens de input), o modelo pode gastar **todos os 3000 tokens** apenas em raciocínio, deixando ZERO para a resposta final.

### Evidência

| max_tokens | reasoning_tokens | completion_tokens | content_length | finish_reason |
|-----------|-----------------|-------------------|----------------|---------------|
| 1200 | 1200 | 1200 | 0 | length |
| 3000 | 3000 | 3000 | 0 | length |
| 16000 | 1780 | 2504 | 2756 chars | stop |

**Conclusão:** Para prompts complexos (system prompt longo + instruções detalhadas), `max_tokens` precisa de **16000+** para garantir que sobre espaço para a resposta após o raciocínio.

## Estrutura da Resposta

```python
{
  "role": "assistant",
  "content": "RESPOSTA FINAL AQUI",               # vazio se max_tokens insuficiente
  "reasoning_content": "CADEIA DE RACIOCÍNIO",    # pode ser vazio se não usado
  "finish_reason": "stop"                         # "stop" | "length" | "error"
}
```

## Três Problemas Conhecidos

### 1. Content Vazio
O modelo gasta todos os tokens em `reasoning_content` e não sobra nada para `content`.

**Sintoma:** Chamada retorna 200 OK, status "ok", mas `content` é `""` e `finish_reason` é `"length"`.

**Solução:** Fallback para `reasoning_content` + `max_tokens >= 16000`.

### 2. CoT Vazado para Content
Às vezes o modelo coloca a cadeia de raciocínio DENTRO do campo `content` em vez de `reasoning_content`. O texto começa com "Thinking..." ou "Analyze the Request...".

**Solução híbrida:**
1. **Preventiva:** Instruir o modelo a não incluir CoT na resposta (system prompt: regra 6)
2. **Corretiva:** `_strip_cot_from_content()` — detecta e remove o preamble de raciocínio, extraindo apenas a resposta real

### 3. Truncamento Silencioso
Quando `finish_reason = "length"`, a resposta foi cortada. O modelo parou de gerar antes de concluir.

**Solução:** Detectar `finish_reason` e marcar como `truncated: true` para que o usuário saiba.

## Implementação de Referência: `extract_content()`

```python
def extract_content(msg: dict) -> tuple[str, str]:
    """Extrai conteúdo, retornando (resposta_limpa, finish_reason)."""
    content = (msg.get("content") or "").strip()
    reasoning = (msg.get("reasoning_content") or "").strip()
    finish_reason = msg.get("finish_reason", "stop")

    # Estratégia 1: content limpo → resposta real
    if content and not _looks_like_cot(content):
        return content, finish_reason

    # Estratégia 2: content vazio → reasoning como fallback
    if not content and reasoning:
        return reasoning, finish_reason

    # Estratégia 3: CoT vazado → tenta extrair resposta real
    result = _strip_cot_from_content(content)
    if result:
        return result, finish_reason

    # Estratégia 4: reasoning pode ser melhor
    if reasoning and len(reasoning) > 200:
        return reasoning, finish_reason

    # Último caso: devolve o que tem
    return content if content else "[resposta vazia]", finish_reason
```

## Consumo Observado no Brain

Teste com 9 inteligências em paralelo (05/2026):

| Cenário | max_tokens | reasoning_tokens médio | content médio | Resultado |
|---------|-----------|----------------------|---------------|-----------|
| Inteligência individual | 16000 | ~1500-2000 | ~2000-4000 chars | ✅ Completo |
| Síntese (9 respostas + contexto) | 16000 | ~2500 | ~3000+ chars | ✅ Completo |
| Inteligência (max_tokens=3000, ANTES da correção) | 3000 | 3000 | 0 chars | ❌ Vazio |

## Efeito da Temperatura

Modelos de raciocínio são **menos sensíveis à temperatura** que modelos padrão. No Brain, usamos:

| Inteligência | Temp | Comportamento observado |
|-------------|------|------------------------|
| Lógico-Matemática | 0.3 | Reasoning mais enxuto, respostas diretas |
| Musical / Existencial | 0.8-0.9 | Reasoning mais criativo, metáforas mais ricas |
| Demais | 0.6-0.7 | Equilíbrio entre precisão e fluência |

O efeito é perceptível mas mais sutil que em modelos não-reasoning.

## Lições para Skills Futuras

Qualquer skill que chame modelos de raciocínio via API HTTP direta DEVE:

1. **Usar `max_tokens >= 8000`** (16000 para prompts complexos com system prompt longo)
2. **Implementar fallback** `content` → `reasoning_content` → `strip CoT`
3. **Checar `finish_reason`** — se `"length"`, resposta possivelmente truncada
4. **Adicionar regra no system prompt** instruindo o modelo a não vazar CoT
5. **Não confiar em `content` sozinho** — sempre extrair com fallback

## Skills que Usam Esta Lógica

- **brain** (`/root/.hermes/skills/brain/orchestrator.py`) — implementação completa com fallback e stripping de CoT. Exemplo funcional e testado.
