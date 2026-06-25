# Backup configuração agentes OpenClaw, 2026-06-25

```json
{
  "gerado_em": "2026-06-25T19:35:20+00:00",
  "objetivo": "Backup sanitizado da configuração de agentes OpenClaw após inclusão do Robotnik.",
  "agents": [
    {
      "id": "main",
      "name": "main",
      "workspace": "/data/.openclaw/workspace",
      "agentDir": "/data/.openclaw/agents/main"
    },
    {
      "id": "kowalski",
      "name": "Kowalski",
      "workspace": "/data/.openclaw/workspace-kowalski",
      "agentDir": "/data/.openclaw/agents/kowalski"
    },
    {
      "id": "darth-vader",
      "name": "Darth Vader",
      "workspace": "/data/.openclaw/workspace-darth-vader",
      "agentDir": "/data/.openclaw/agents/darth-vader"
    },
    {
      "id": "robotnik",
      "name": "Robotnik",
      "workspace": "/data/.openclaw/workspace-robotnik",
      "agentDir": "/data/.openclaw/agents/robotnik"
    }
  ],
  "tools": {
    "sessions": {
      "visibility": "all"
    },
    "agentToAgent": {
      "enabled": true,
      "allow": [
        "main",
        "kowalski",
        "darth-vader",
        "robotnik"
      ]
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "allowFrom": [
        "5760416853"
      ],
      "groups": {
        "*": {
          "requireMention": false
        }
      },
      "botToken": "REDACTED"
    }
  }
}
```

## Observações

- Robotnik foi incluído como agente interno, sem canal Telegram direto próprio.
- Telegram direto segue restrito ao Puppet Master/main via allowlist atual.
- `tools.sessions.visibility` está em `all`.
- `tools.agentToAgent.enabled` está ligado com allowlist `main`, `kowalski`, `darth-vader` e `robotnik`.
- Segredos foram removidos/redigidos neste backup.
