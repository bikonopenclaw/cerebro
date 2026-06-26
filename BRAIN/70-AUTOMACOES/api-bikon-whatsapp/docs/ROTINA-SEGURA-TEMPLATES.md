# Rotina segura, envio de templates WhatsApp Bikon

## Regra operacional

Envio real para cliente externo só com confirmação explícita do Hebert/Puppet Master.

A rotina sempre roda em `dry-run` por padrão. Para enviar de verdade, precisa passar:

```bash
--confirm ENVIAR
```

## Template aprovado inicialmente

```json
retomar_solicitacao
```

Dados:

- Template: `retomar_solicitacao (pt_BR)`
- Template ID: `69b4c7d2ab61bd013ee12989`
- Uso: retomar atendimento com botões “Sim” e “Não”
- Header: imagem pública da Bikon `logo-white.png`

Configuração fica em:

```bash
config/templates-aprovados.json
```

## Dry-run, não envia

```bash
./scripts/envio_seguro_template.py \
  --number 27993090119 \
  --template retomar_solicitacao \
  --reason "teste interno"
```

## Envio real, exige confirmação

```bash
./scripts/envio_seguro_template.py \
  --number 27993090119 \
  --template retomar_solicitacao \
  --reason "retomar solicitação do cliente X" \
  --force-send \
  --confirm ENVIAR
```

## Logs

Todo dry-run e envio real registra auditoria em:

```bash
logs/envios-template.jsonl
```

Campos registrados:

- timestamp UTC
- número normalizado
- template
- templateId
- motivo
- dryRun true/false
- resultado da API

## Guardrails

- Não enviar texto livre para cliente externo por padrão.
- Preferir template aprovado via WhatsApp Cloud.
- Não expor token em logs, chat ou relatório.
- Se adicionar novo template, registrar em `config/templates-aprovados.json` antes de usar.
