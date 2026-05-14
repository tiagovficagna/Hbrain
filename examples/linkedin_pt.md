— 🧠 —

**Título:** Por que um Doutor em Design construiu um orquestrador de IA baseado nas Inteligências Múltiplas de Gardner

---

Há algumas semanas eu me fiz uma pergunta que não me largava:

*E se, ao invés de perguntar a um único modelo de IA sobre um fenômeno, eu pudesse perguntar a 9 «especialistas» diferentes — cada um treinado para enxergar o mundo por uma lente cognitiva única — e depois sintetizar tudo num conceito novo?*

Não um resumo. Um conceito que só existe porque 9 perspectivas diferentes se encontraram.

Passei anos estudando Design, lecionei sobre cognição e jogos, e sempre fui fascinado pela Teoria das Inteligências Múltiplas de Howard Gardner. A ideia de que não existe uma única forma de inteligência — mas várias (linguística, lógico-matemática, espacial, musical, interpessoal, intrapessoal, corporal-cinestésica, naturalista, existencial) — sempre ressoou comigo.

Então eu construí: o **Hbrain**.

É um orquestrador multi-agente open source que:
⚡ Dispara a mesma pergunta para 9 agentes de IA em paralelo
🧠 Cada um interpreta a pergunta através de uma inteligência diferente (com personalidade própria definida num `soul.md`)
🔄 Coleta todas as respostas
🪄 **Sintetiza um conceito NOVO** — não uma colagem, mas uma compreensão integrada.

Perguntei "o que é uma sinapse?" para o Hbrain. A inteligência **linguística** traçou a etimologia da palavra (*syn-haptein* = "agarrar junto") e descreveu a fenda sináptica como uma vírgula no discurso do corpo. A **espacial** desenhou a arquitetura microscópica — vesículas como navios-cargueiros, receptores como docas de atracação. A **musical** ouviu polirritmia na soma temporal. A **existencial** sentou-se com a pergunta de como a matéria se torna significado naquele intervalo de 20nm.

A síntese que emergiu:

> *"A sinapse não é o ponto de contato entre neurônios — é o intervalo que torna a conexão significativa. É o vazio ativo onde a continuidade é deliberadamente fraturada para que o sinal ganhe profundidade, ambiguidade e potência criativa."*

Isso não veio de um único modelo. Veio da colisão de 9 perspectivas.

O projeto é 100% open source (MIT), está no GitHub, e tem ~500 linhas de Python com asyncio. Funciona com qualquer API compatível com OpenAI. Usei o deepseek-v4-flash (cerca de $0.001 por execução).

🔗 https://github.com/tiagovficagna/Hbrain

Estou começando essa jornada e adoraria ouvir o que pensam — educadores, cientistas cognitivos, devs, designers. Como vocês usariam uma ferramenta assim?

#IA #MultiAgente #InteligênciasMúltiplas #OpenSource #Design #Cognição #Educação #Python #Asyncio

—

*PhD em Design. Professor. Acredito que a melhor forma de entender algo é olhar de todos os ângulos possíveis.*
