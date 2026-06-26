# API WhatsApp Bikon

```yaml
nome: API WhatsApp Bikon
status: validada
responsavel: Puppet Master
ultima_revisao: 2026-06-26
fonte: Swagger enviado por Hebert e teste real via canal Atendimento Bikon
tags: [whatsapp, api, meta, atendimento, bikon]
```

## Objetivo

Conectar o canal oficial de atendimento WhatsApp da Bikon via API `https://api.bikon.tech`, usando token do canal e templates aprovados do WhatsApp Cloud.

## Local operacional

Workspace ativo:

```bash
/data/.openclaw/workspace/api-bikon-whatsapp
```

Snapshot sanitizado versionado:

```bash
BRAIN/70-AUTOMACOES/api-bikon-whatsapp
```

## Segurança

- Token real fica somente em `api-bikon-whatsapp/secrets/.env` no workspace operacional.
- Token não entra no Brain, Git, relatório ou chat.
- Google Doc temporário usado para transferência do token foi apagado após captura.
- Envio externo deve usar rotina segura com confirmação explícita.

## Validação feita

Canal testado com sucesso:

- Descrição: Atendimento Bikon
- Número: +55 (27) 3022-0499
- Status retornado: REGISTERED
- Tipo: WhatsApp Cloud/API oficial Meta

Teste de envio livre inicial para número interno retornou `202 Successfully added to the transmission queue`.

Teste de template oficial confirmado por Hebert:

- Template: `retomar_solicitacao (pt_BR)`
- Template ID interno: `69b4c7d2ab61bd013ee12989`
- Header dinâmico: imagem pública `https://bikon.com.br/wp-content/uploads/2024/09/logo-white.png`
- Mensagem recebida com sucesso no WhatsApp.

## Rotina segura

Dry-run por padrão:

```bash
./scripts/envio_seguro_template.py \
  --number 27993090119 \
  --template retomar_solicitacao \
  --reason "motivo do contato"
```

Envio real exige confirmação explícita:

```bash
./scripts/envio_seguro_template.py \
  --number 27993090119 \
  --template retomar_solicitacao \
  --reason "retomar solicitação" \
  --force-send \
  --confirm ENVIAR
```

Logs locais ficam em `logs/envios-template.jsonl`, fora do snapshot versionado.

## Próximos passos

- Usar somente templates aprovados para contato ativo/externo.
- Registrar novos templates em `config/templates-aprovados.json` antes de uso.
- Se virar rotina recorrente, criar skill/agente específico para atendimento WhatsApp com aprovação humana obrigatória para disparos.
