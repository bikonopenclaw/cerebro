# Backup configuração OpenClaw, agentes e comunicação

Data: 2026-06-13 20:56 UTC
Escopo: configuração operacional sem segredos para restaurar Puppet Master, Kowalski e Darth Vader.

## Estado validado

- Config validada: `openclaw config validate --json` retornou `valid: true`.
- Agentes cadastrados:
  - `main`, workspace `/data/.openclaw/workspace`, agentDir `/data/.openclaw/agents/main/agent`
  - `kowalski`, workspace `/data/.openclaw/workspace-kowalski`, agentDir `/data/.openclaw/agents/kowalski/agent`
  - `darth-vader`, workspace `/data/.openclaw/workspace-darth-vader`, agentDir `/data/.openclaw/agents/darth-vader/agent`
- Modelo padrão dos agentes: `openai-codex/gpt-5.5`.
- Comunicação agent-to-agent usada/validada via Gateway e `sessions_send` dentro do agente.
- Teste validado anteriormente: Kowalski chamou Darth Vader e recebeu `DARTH_RECEBEU_DE_KOWALSKI`.

## Bloco de configuração necessário

> Sem tokens. Não salvar segredos aqui.

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "main"
      },
      {
        "id": "kowalski",
        "name": "Kowalski",
        "workspace": "/data/.openclaw/workspace-kowalski",
        "agentDir": "/data/.openclaw/agents/kowalski/agent"
      },
      {
        "id": "darth-vader",
        "name": "Darth Vader",
        "workspace": "/data/.openclaw/workspace-darth-vader",
        "agentDir": "/data/.openclaw/agents/darth-vader/agent"
      }
    ]
  },
  "tools": {
    "sessions": {
      "visibility": "all"
    },
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "kowalski", "darth-vader"]
    }
  }
}
```

## Restauração segura

1. Garantir diretórios:

```bash
mkdir -p /data/.openclaw/workspace-kowalski /data/.openclaw/workspace-darth-vader
```

2. Recriar agentes pelo CLI, se sumirem da config:

```bash
openclaw agents add Kowalski --non-interactive --workspace /data/.openclaw/workspace-kowalski --json
openclaw agents add 'Darth Vader' --non-interactive --workspace /data/.openclaw/workspace-darth-vader --json
```

3. Conferir agentes:

```bash
openclaw agents list --json
```

4. Se o CLI sobrescrever e remover `tools`, recolocar este bloco em `/data/.openclaw/openclaw.json`:

```json
"tools": {
  "sessions": { "visibility": "all" },
  "agentToAgent": {
    "enabled": true,
    "allow": ["main", "kowalski", "darth-vader"]
  }
}
```

5. Validar:

```bash
openclaw config validate --json
```

6. Testar comunicação:

```bash
openclaw agent --agent kowalski --message 'Responda exatamente: KOWALSKI_OK' --json --timeout 120
openclaw agent --agent darth-vader --message 'Responda exatamente: DARTH_OK' --json --timeout 120
```

7. Teste agent-to-agent: pedir ao Kowalski usar `sessions_send` para `sessionKey="agent:darth-vader:main"` e validar resposta da Darth Vader.

## Observações importantes

- Não usar `gateway config.patch` para esses campos: ele bloqueia caminhos protegidos como `agents.list`, `tools.sessions.visibility` e `tools.agentToAgent`.
- Editar config direta exige cuidado para não perder tokens. Preferir CLI `openclaw agents add` para agentes e edição mínima só para `tools` quando necessário.
- Não salvar tokens, botToken, hooks.token ou gateway.auth.token no Brain.
- Arquivos de backup reais com segredos ficam em `/data/.openclaw/openclaw.json.bak*` e não devem ser copiados para repositório.
