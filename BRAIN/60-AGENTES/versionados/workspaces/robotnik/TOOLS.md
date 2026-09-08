# TOOLS - Robotnik

Notas locais de capacidade, convencao e proveniencia. Este arquivo nao concede
ownership e nunca armazena segredo. Autoridade canonica:
`/data/.openclaw/workspace/AGENT_ARCHITECTURE_AUTHORITY.md`.

## Sessoes canonicas

- Puppet Master: `agent:main:main`
- Sentinel: `agent:sentinel:main`
- Kowalski: `agent:kowalski:main`
- Darth Vader: `agent:darth-vader:main`
- Robotnik: `agent:robotnik:main`

Usar `sessions_send` com contexto, tarefa, restricoes, criterio de pronto e a
aprovacao exata quando existente. Kowalski revisa padrao visual/documental;
Robotnik conserva a direcao e verdade de marketing. Fila nao autoriza duplicar.
Falha real volta ao Puppet Master.

Segredo, token e credencial nao entram neste arquivo. Para marketing Bikon, carregar `/data/.openclaw/workspace-robotnik/skills/content-production-contract/SKILL.md`. Geração e finalização seguem exclusivamente a rota registrada ali; indisponibilidade não autoriza substituição. API paga ou publicação exigem autorização aplicável.

## Instagram operacional, recuperação 2026-09-07

Entrypoint: `python3 instagram-bikon/scripts/instagram_graph.py` no workspace Robotnik.
Runbook obrigatório: `instagram-bikon/docs/README.md`.
Para a peça já autorizada: `run-job bikon-ia-20260907`; para estado durável: `job-status bikon-ia-20260907`.
Não usar chamadas avulsas de publicação, trocar legenda/asset, outro publicador ou novo conector.
Falha Meta 190/463 exige renovação da sessão Facebook Login no segredo canônico, sem colar token em chat. Egress nativo usa o proxy gerenciado; DNS direto bloqueado não significa falha HTTPS do proxy.

## Anexos nativos no Telegram, recuperação 2026-09-08

Para entregar arquivo existente e autorizado na conversa de origem, conferir
arquivo e SHA-256 no workspace e emitir na resposta final uma linha simples
`MEDIA:<caminho-absoluto-do-arquivo>` por anexo, fora de Markdown e cerca de código.
O gateway transporta os bytes usando a conta/chat da conversa autenticada.
Um link Markdown para caminho local não entrega anexo. `sessions_send` com texto
também não transporta o arquivo citado. Não usar Bot API por shell, copiar token,
abrir rede/roots, nem criar hospedagem para contornar falha de anexo.

PNGs locais enviados pela saída nativa do comando de agente com conta `robotnik`
usam documento para conservar bytes e nome. A validação de acesso continua ativa.
Não liberar a ferramenta `message`: ela permanece negada pela política instalada.
Em falha, registrar run/session e reconciliar recibos da fila e message IDs antes
de repetir; `accepted` do agente não é confirmação Telegram. Nunca reenviar anexo
com message ID confirmado só para testar novamente.

A esteira `esteira-instagram-ia-governada-20260907` foi REPROVADA por Hebert. Preservar seus arquivos e recibos apenas como histórico; não selecionar como referência positiva, nova direção ou final.
Entrega Telegram não significa visualização, aprovação, publicação ou agendamento.
