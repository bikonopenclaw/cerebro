---
name: "codex-limite-status"
description: "Consulta consumo e limites do Codex pelos logs locais."
---

# Comando de limite Codex

## Objetivo

Responder corretamente quando Hebert pedir consumo ou limites do Codex a partir dos logs locais do Codex CLI.

## Gatilhos

- `limite codex`
- `uso codex` como alias histórico. Interpretar como consulta de limite, não como pergunta sobre o motor em uso.

## Fonte autorizada

Leitura local, sem chamada de rede e sem credencial adicional:

`/data/.openclaw/agents/main/codex-home/sessions`

Quando relevante, consultar também o mesmo diretório de sessões dos agentes especialistas.

Os arquivos são JSONL no padrão:

`<CODEX_HOME>/sessions/<AAAA>/<MM>/<DD>/rollout-<timestamp>-<uuid>.jsonl`

## Regra canônica de identificação das janelas

Nunca inferir a janela pela posição `primary` ou `secondary`. Essas posições não são fixas.

Identificar exclusivamente pelo campo `window_minutes`:

- `300`: janela móvel de 5 horas.
- `10080`: janela de 7 dias.

Campos úteis em cada bloco:

- `used_percent`
- `window_minutes`
- `resets_at`

Registrar também o `timestamp` do evento que originou o número.

## Procedimento

1. Localizar os rollouts com atividade mais recente.
2. Ler o trecho final de cada arquivo, começando pelo mais recente.
3. Percorrer os eventos de trás para frente.
4. Para cada bloco em `rate_limits.primary` e `rate_limits.secondary`, classificar pela duração em `window_minutes`.
5. Guardar a observação mais recente de cada janela.
6. Parar quando encontrar as duas janelas ou quando acabar o recorte pesquisado.
7. Se uma janela não aparecer, reportar `desconhecida` ou `não encontrada no recorte`. Nunca assumir 0%.
8. Converter `resets_at` e o timestamp do evento para horário de Brasília.
9. Não expor conteúdo sensível dos logs.

Se uma janela estiver ausente, ampliar primeiro o número de arquivos e o trecho final lido. Não fazer chamada de rede como fallback.

## Formato de resposta

Responder em português BR, curto e direto:

```text
5h [██████░░░░░░░░░░░░] 27% usado, 73% livre. Reset: 14:30 BRT.
Semana [███░░░░░░░░░░░░░░░] 15% usado, 85% livre. Reset: sexta 09:00 BRT.
Última leitura registrada: HH:MM BRT.
```

Se os timestamps das janelas forem diferentes, informar a idade de cada leitura ou indicar qual delas está desatualizada.

## Honestidade obrigatória

- O dado é o último rate limit gravado localmente pelo Codex CLI durante uso normal.
- Não é uma consulta ativa ao provedor.
- Não mede saldo financeiro, custo ou teto absoluto em tokens.
- `total_token_usage`, quando existir, é contexto da sessão e não saldo restante.
- Ausência de dado significa desconhecido, nunca 0%.
- O formato do log é interno e pode mudar. Se o padrão deixar de aparecer, reportar possível quebra do coletor.
