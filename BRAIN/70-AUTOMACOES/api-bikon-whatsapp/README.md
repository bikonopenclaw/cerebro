# Integração API WhatsApp Bikon

Client local para testar e operar `https://api.bikon.tech`.

## Setup

```bash
cp secrets/.env.example secrets/.env
chmod 600 secrets/.env
# preencher BIKON_API_TOKEN no arquivo
```

## Testes seguros

```bash
./scripts/bikon_whatsapp_api.py channel
./scripts/bikon_whatsapp_api.py status
```

## Envio de texto, só com aprovação

```bash
./scripts/bikon_whatsapp_api.py send-text --number 5527999999999 --message "teste" --force-send
```

## Listar atendimentos manuais individuais

```bash
./scripts/bikon_whatsapp_api.py list-chats --page 1 --type-chat 2 --status 2
```

## Rotina segura de templates

Dry-run, não envia:

```bash
./scripts/envio_seguro_template.py --number 27993090119 --template retomar_solicitacao --reason "teste"
```

Envio real, só com confirmação explícita:

```bash
./scripts/envio_seguro_template.py --number 27993090119 --template retomar_solicitacao --reason "retomar solicitação" --force-send --confirm ENVIAR
```

Ver detalhes em `docs/ROTINA-SEGURA-TEMPLATES.md`.
