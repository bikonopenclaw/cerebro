# Job de envio de e-mail ARX Backup

Crie um arquivo `.json` em `/data/.openclaw/workspace-kowalski/arx-backup/jobs`.

## Campos obrigatórios

```json
{
  "status": "aguardando_aprovacao",
  "cliente": "Nome do cliente",
  "destinatarios": ["cliente@dominio.com.br"],
  "assunto": "Relatório ARX Backup, Cliente, Período",
  "corpo": "Olá.\n\nSegue o relatório...\n\nARX Backup\nbackup@arxcore.com.br",
  "anexos": [
    "/data/.openclaw/workspace-kowalski/arx-backup/relatorios/por-cliente/relatorio.pdf"
  ]
}
```

## Campos opcionais

```json
{
  "cc": [],
  "bcc": [],
  "reply_to": "backup@arxcore.com.br",
  "periodo": "Junho/2026",
  "observacoes_internas": "Não enviar antes de revisar destinatário."
}
```

## Status permitidos

- `aguardando_aprovacao`: job preparado, não enviar.
- `aprovado`: autorizado para envio real.
- `enviado`: envio concluído.
- `erro`: tentativa falhou.

## Regras

- Não enviar se o status não for `aprovado`.
- Não enviar sem destinatário.
- Não enviar sem anexo, salvo ordem explícita.
- Não anexar arquivo fora do workspace ARX Backup sem revisar o caminho.
- Não colocar credencial no job.
- Não usar destinatário inferido por nome do cliente.
