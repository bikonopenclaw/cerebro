---
name: "codex-limite-status"
description: "Consulta limites Codex por comando curto"
---

# Comando de limite Codex

## Objetivo

Responder corretamente quando Hebert pedir consumo/limites do Codex nos logs locais.

## Gatilho principal

Quando Hebert mandar:

`limite codex`

Puppet Master deve consultar o consumo/limites do Codex nos logs locais e responder em formato executivo.

## Alias antigo

Manter como alias válido:

`uso codex`

Esse alias existe por histórico, mas pode ser ambíguo. Se Hebert usar `uso codex`, tratar como pedido de limite Codex, não como pergunta sobre qual motor está sendo usado.

## Fonte

Ler o evento mais recente `token_count` nos logs `codex-home/sessions` dos agentes, principalmente:

`/data/.openclaw/agents/main/codex-home/sessions`

Quando relevante, considerar também sessões dos agentes especialistas.

## Campos relevantes

- `rate_limits.primary.used_percent`: janela de 5h.
- `rate_limits.primary.resets_at`: reset da janela de 5h.
- `rate_limits.secondary.used_percent`: janela semanal.
- `rate_limits.secondary.resets_at`: reset semanal.
- `total_token_usage`: contexto de tokens da sessão, quando existir.

## Como responder

Responder em português BR, curto e direto.

Usar horário de Brasília.

Formato preferido:

```text
5h [██████░░░░░░░░░░░░] 27% usado, 73% livre. Reset: 14:30 BRT.
Semana [███░░░░░░░░░░░░░░░] 15% usado, 85% livre. Reset: sexta 09:00 BRT.
Última rodada registrada: HH:MM BRT.
```

## Honestidade obrigatória

Explicar quando necessário:

- isso mede percentual de limite/rate limit do Codex registrado nos logs locais;
- não é saldo financeiro oficial da conta OpenAI;
- se não houver evento recente, informar que o dado local está ausente ou velho, sem inventar número.

## Restrições

- Não responder que Hebert está usando Codex como motor quando o comando for `limite codex` ou `uso codex`.
- Não inventar consumo.
- Não converter UTC mentalmente para Hebert; sempre mostrar horário de Brasília.
- Não expor conteúdo sensível de logs.
