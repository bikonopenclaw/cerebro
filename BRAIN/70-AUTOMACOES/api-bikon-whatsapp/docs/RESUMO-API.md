# API WhatsApp Bikon, resumo operacional

Base URL: `https://api.bikon.tech`
Versão: v2
Autenticação: header `access-token: <TOKEN_DO_CANAL>`

## Como obter o token
Na plataforma: **Empresas > Canais > três pontos do canal > Copiar Token API**.

Nunca colar o token em Telegram. Salvar em:

```bash
/data/.openclaw/workspace/api-bikon-whatsapp/secrets/.env
```

Formato:

```env
BIKON_API_BASE=https://api.bikon.tech
BIKON_API_TOKEN=TOKEN_DO_CANAL
```

## Endpoints principais

- `GET /core/v2/api/channel` consulta dados do canal.
- `GET /core/v2/api/channel/status` consulta status: STARTING, OPENING, PAIRING, UNPAIRED, CONNECTED, CONFLICT, CLOSING, OFFLINE.
- `POST /core/v2/api/chats/send-text` envia texto.
- `POST /core/v2/api/chats/send-media` envia mídia por link ou base64.
- `POST /core/v2/api/chats/create-new` cria atendimento.
- `POST /core/v2/api/chats/list` lista atendimentos, paginação de 100.
- `GET /core/v2/api/contacts/number/{number}` busca contato pelo número.
- `POST /core/v2/api/contacts` cria contato.

## Rate limit

- 50 req/s por token.
- 2.500 req/min por token.
- Em 429, usar backoff exponencial.

## Guardrail Bikon

Envio real para cliente externo exige aprovação explícita do Hebert/Puppet Master.
Começar por `channel` e `status`, depois teste controlado para número interno.
