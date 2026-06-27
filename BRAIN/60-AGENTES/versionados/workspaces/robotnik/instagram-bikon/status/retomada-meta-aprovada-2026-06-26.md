# Retomada, integração Instagram Bikon

Status: verificação de segurança da Meta aprovada, informado pelo Hebert em 2026-06-26.

## Estado técnico

- Workspace: `/data/.openclaw/workspace-robotnik/instagram-bikon`
- Script validado por `python3 -m py_compile scripts/instagram_graph.py`
- Arquivo de segredos criado em `secrets/instagram-bikon.env`
- Permissão aplicada: `chmod 600 secrets/instagram-bikon.env`
- Publicação permanece travada em `ROBOTNIK_INSTAGRAM_MODE=draft`

## Pendente

Preencher `META_ACCESS_TOKEN` com token Meta de longa duração e, depois, rodar:

```bash
python3 scripts/instagram_graph.py me
python3 scripts/instagram_graph.py pages
```

Depois de identificar a Página da Bikon e a conta Instagram vinculada, preencher:

- `META_PAGE_ID`
- `INSTAGRAM_BUSINESS_ACCOUNT_ID`

Publicação real somente com aprovação explícita do Hebert.
