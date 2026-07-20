---
name: "praxis-gws"
description: "Google Workspace Bikon mínimo: Gmail, Drive e Calendar"
---

# Praxis GWS

Skill operacional Bikon para usar Google Workspace somente nestas superfícies:

- Gmail: preparar, ler e enviar e-mails via Gmail API.
- Drive: listar, buscar, baixar, renomear, criar pastas e manipular arquivos via Drive API.
- Calendar: consultar e criar eventos quando houver token autorizado.

## Limites obrigatórios

- Não usar escopos Google Docs, Sheets, Slides, Cloud Support ou APIs fora de Gmail, Drive e Calendar.
- Não guardar `credentials.json`, `token.json`, service account, refresh token, client secret ou qualquer segredo dentro da skill.
- Credenciais devem ficar em `/data/.openclaw/secrets/praxis-gws/` ou no caminho compatível `~/.config/praxis-gws/`, com diretório `700` e arquivos `600`.
- Comunicação externa real em nome da Bikon exige aprovação explícita do Hebert antes do envio.
- Não abrir navegador automaticamente por script; quando precisar autenticar, gerar URL e pedir ação humana.
- Não instalar dependências ou manter `node_modules` dentro da pasta da skill como artefato operacional.

## Escopos permitidos

Use o menor escopo possível dentro destes grupos:

- Gmail: preferir `https://www.googleapis.com/auth/gmail.send` para envio; usar `gmail.modify` só quando precisar ler/mover/marcar mensagens.
- Drive: preferir `https://www.googleapis.com/auth/drive.file` quando bastar; usar `drive` só quando a tarefa exigir acesso amplo.
- Calendar: preferir `https://www.googleapis.com/auth/calendar.events`; usar `calendar` só quando precisar administração ampla da agenda.

## Fluxo seguro

1. Confirmar a tarefa: Gmail, Drive ou Calendar.
2. Verificar se a credencial/token existe fora da skill.
3. Usar script específico da superfície, sem improvisar envio externo.
4. Para e-mail real: apresentar destinatário, assunto e corpo para aprovação do Hebert antes de enviar.
5. Registrar erro sem imprimir segredo.

## Scripts operacionais esperados

Manter somente scripts diretamente ligados a Gmail, Drive, Calendar e OAuth mínimo:

- `generate-auth-url.js`: gera URL OAuth apenas com Gmail, Drive e Calendar.
- `trocar-token.js`: troca código OAuth por token e salva fora da skill.
- `enviar-email.js`: envia e-mail texto ou com anexo pela Gmail API.
- `send-email-html.js`: envia e-mail HTML pela Gmail API.
- `send-email-attachment.js`: envia e-mail com anexo pela Gmail API.
- `listar-emails.js`: lista mensagens do Gmail quando autorizado.
- `drive-cli.js`: busca/lista metadata no Drive.
- `list-folders.js`: lista pastas do Drive.
- `list-drive-structure.js`: lista estrutura do Drive.
- `download-pdf.js`: baixa arquivo do Drive.
- `download-doc.js`: exporta Google Doc via Drive API apenas quando o arquivo estiver no Drive e sem usar Docs API.
- `rename-file.js`: renomeia arquivo via Drive API.
- `scripts/praxis-gws.js`: CLI consolidado se mantiver apenas Gmail, Drive e Calendar.

## Remover da skill operacional

Remover ou arquivar fora da skill ativa:

- scripts com escopos fora de Gmail, Drive e Calendar;
- scripts de Google Docs/Sheets/Slides dedicados;
- service account paralelo;
- scripts específicos de NFS-e;
- auth duplicado ou que abre navegador automaticamente;
- arquivos de teste soltos;
- `node_modules` dentro da skill;
- documentação auxiliar duplicada como README/INSTALL/status antigo, quando não for necessária para o agente.

## Aprovação externa

Para qualquer envio real por Gmail:

- mostrar destinatário;
- mostrar assunto;
- mostrar corpo resumido ou arquivo HTML usado;
- aguardar confirmação explícita do Hebert.

## Estado esperado após limpeza

A skill deve ficar pequena, auditável e focada. Se o audit ainda acusar execução de processo externo, revisar o arquivo indicado antes de usar em produção.
