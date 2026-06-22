---
name: enviar-email-arx-backup
description: Enviar e-mails de relatórios ARX Backup para clientes somente quando acionado pela skill arx-backup, usando jobs aprovados em /data/.openclaw/workspace-kowalski/arx-backup/jobs; use para validar, preparar dry-run ou disparar e-mail ARX Backup com anexo após aprovação explícita do Hebert/Puppet Master.
---

# Enviar e-mail ARX Backup

Use esta skill apenas como etapa de envio da skill `arx-backup`.

Não use para e-mail genérico, prospecção, cobrança, suporte avulso ou comunicação fora do fluxo de relatórios ARX Backup.

## Regra de segurança

Envio real para cliente externo só pode acontecer quando o job estiver com `status: "aprovado"` e houver aprovação explícita do Hebert/Puppet Master na conversa.

Relatório mensal ARX Backup só pode ser enviado se cada PDF tiver HTML irmão gerado pelo modelo aprovado `modelo-padrao-relatorio-mensal-arx-backup.html`, com marcador `ARX_APPROVED_MODEL:modelo-padrao-relatorio-mensal-arx-backup`.

Se faltar aprovação ou marcador do modelo, faça apenas validação ou dry-run.

Nunca invente destinatário. Use somente destinatários informados no job ou aprovados pelo Hebert/Puppet Master.

## Caminhos

- Workspace ARX: `/data/.openclaw/workspace-kowalski/arx-backup`
- Jobs de envio: `/data/.openclaw/workspace-kowalski/arx-backup/jobs`
- Relatórios/anexos: `/data/.openclaw/workspace-kowalski/arx-backup/relatorios`
- Rascunhos: `/data/.openclaw/workspace-kowalski/arx-backup/email-rascunhos`
- Config local: `/data/.openclaw/workspace-kowalski/arx-backup/config/.env`
- Script de envio: `scripts/enviar_email_arx_backup.py`
- Schema do job: `references/job-email-arx-backup.md`

## Workflow

1. Receber da skill `arx-backup` um job `.json` em `/jobs`.
2. Validar cliente, destinatários, assunto, corpo e anexos.
3. Conferir se `status` é `aprovado` antes de envio real.
4. Fazer dry-run quando ainda estiver em revisão.
5. Enviar pelo SMTP configurado no `.env` somente após aprovação.
6. Registrar resultado em `/jobs/envios.log.jsonl`.
7. Se solicitado, marcar o job como `enviado` após sucesso.

## Comandos

Validar sem enviar:

```bash
python3 /data/.openclaw/agents/kowalski/agent/skills/enviar-email-arx-backup/scripts/enviar_email_arx_backup.py --job /data/.openclaw/workspace-kowalski/arx-backup/jobs/NOME.json --dry-run
```

Enviar após aprovação explícita:

```bash
python3 /data/.openclaw/agents/kowalski/agent/skills/enviar-email-arx-backup/scripts/enviar_email_arx_backup.py --job /data/.openclaw/workspace-kowalski/arx-backup/jobs/NOME.json --mark-sent
```

## Config SMTP

Ler credenciais do ambiente ou de `/data/.openclaw/workspace-kowalski/arx-backup/config/.env`.

Variáveis aceitas:

- `ARX_SMTP_HOST` ou `SMTP_HOST`
- `ARX_SMTP_PORT` ou `SMTP_PORT`
- `ARX_SMTP_USER` ou `SMTP_USER`
- `ARX_SMTP_PASSWORD` ou `SMTP_PASSWORD`
- `ARX_SMTP_FROM` ou `SMTP_FROM`
- `ARX_SMTP_FROM_NAME` ou `SMTP_FROM_NAME`, opcional
- `ARX_SMTP_TLS`, opcional, padrão `true`
- `ARX_SMTP_BCC`, opcional, cópia oculta padrão aprovada: `backup@bikon.com.br`
- `ARX_EMAIL_SUBJECT_TEMPLATE`, opcional, padrão aprovado: `Relatório Mensal - {{mes_ano}}`

SMTP ARX Backup aprovado:

- Host: `smtp.dreamhost.com`
- Porta: `587`
- TLS: `true`
- Usuário/de: `backup@arxcore.com.br`
- BCC padrão: `backup@bikon.com.br`

Não imprimir senha ou token em resposta, log ou relatório.

## Padrão de assunto

Para relatório mensal, usar:

```text
Relatório Mensal - {{mes_ano}}
```

Substituir `{{mes_ano}}` pelo mês/ano do relatório, por exemplo `Junho/2026`.

## Padrão de assinatura

Usar assinatura ARX Backup quando o relatório for ARX:

```text
ARX Backup
backup@arxcore.com.br
```

Se o corpo vier pronto no job, não reescrever sem necessidade.
