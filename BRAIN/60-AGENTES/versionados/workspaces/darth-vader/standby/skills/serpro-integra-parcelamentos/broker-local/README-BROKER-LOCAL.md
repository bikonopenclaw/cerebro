# Broker local SERPRO com certificado A1

Objetivo: testar Integra Contador sem entregar o certificado A1 para servidor, OpenClaw, chat ou terceiros.

## Modelo de segurança

- O `.pfx/.p12` fica somente no Mac do Hebert.
- A senha do certificado é digitada no terminal e fica só em memória enquanto o broker roda.
- O broker escuta apenas em `127.0.0.1`.
- A automação consome token temporário via `http://127.0.0.1:8766/token`.
- Não commitar `.serpro-broker.env`, certificado, senha, token ou resposta fiscal bruta.

## Preparar no Mac

Na pasta da skill/projeto:

```bash
cd ~/Projetos/serpro-integra-parcelamentos/broker-local
cp .serpro-broker.env.example .serpro-broker.env
nano .serpro-broker.env
chmod 600 .serpro-broker.env
```

Preencher somente localmente:

```env
SERPRO_CONSUMER_KEY=...
SERPRO_CONSUMER_SECRET=...
SERPRO_CERT_PATH=/caminho/local/do/certificado.pfx
SERPRO_ROLE_TYPE=TERCEIROS
BROKER_PORT=8766
BROKER_CACHE_SECONDS=300
```

## Rodar broker

```bash
python3 serpro_cert_broker.py
```

Ele vai pedir:

```text
Senha do certificado A1, não será salva:
```

## Teste local

Em outro terminal:

```bash
curl -sS http://127.0.0.1:8766/health
curl -sS http://127.0.0.1:8766/token | python3 -m json.tool
```

Resultado esperado:

- `ok: true`
- objeto `token` com `access_token` e/ou `jwt_token`

Se vier erro `401`, `403` ou resposta sem token, revisar credenciais SERPRO, contrato, Role-Type, certificado e senha.

## Uso pela skill SERPRO

A skill de parcelamentos não deve ler certificado.
Ela deve chamar o broker local e usar só token temporário:

```bash
TOKEN_JSON=$(curl -sS http://127.0.0.1:8766/token)
```

Depois extrair:

```bash
ACCESS_TOKEN=$(python3 - <<'PY'
import json,sys
print(json.load(sys.stdin)["token"].get("access_token", ""))
PY
<<< "$TOKEN_JSON")
```

## Guardrails

- Não chamar `/Emitir` nesta fase.
- Começar por endpoints de consulta.
- Não salvar payload fiscal bruto.
- Não colar token no chat.
- Não expor o broker fora de `127.0.0.1`.

## Teste simplificado, v2

Se você estiver dentro da pasta `broker-local`, use:

```bash
bash testar_broker_local.sh
```

Se estiver na pasta pai, use:

```bash
bash broker-local/testar_broker_local.sh
```
