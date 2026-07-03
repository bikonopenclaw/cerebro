# API WhatsApp Bikon

```yaml
nome: API WhatsApp Bikon
status: validada
responsavel: Puppet Master
ultima_revisao: 2026-07-03
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

## Donos operacionais

Regra definida por Hebert em 2026-07-02:

- Relatórios e KPIs de atendimento WhatsApp: Kowalski.
- Campanhas, templates, copies e retomada de lead: Robotnik.
- Envios reais pelo WhatsApp: Puppet Master, sempre travado com aprovação explícita do Hebert.

Skills formais:

- Kowalski: `whatsapp-bikon-kpi`.
- Robotnik: `whatsapp-bikon-campanhas`.


## KPI diário observado em 2026-07-02 BRT

Resumo da rotina diária de atendimento:

- Canal `Atendimento Bikon +55 (27) 3022-0499`: status `REGISTERED`.
- Chats do dia por status: individual manual 1; individual finalizado 9.
- Manuais abertos no momento do relatório: 2; não lidas: 0.
- Finalizados do dia: 11.
- Tempo manual dos finalizados: média 7,4h, mediana 30,3min, P90 22,5h.
- Satisfação registrada: 3 respostas como `Ótimo`.

Aprendizado operacional: média diária pode ficar inflada por outliers antigos finalizados no dia; relatório executivo deve considerar visão com e sem outliers quando a distorção for relevante.

## Próximos passos

- Usar somente templates aprovados para contato ativo/externo.
- Registrar novos templates em `config/templates-aprovados.json` antes de uso.
- Manter envio real centralizado no Puppet Master com aprovação explícita do Hebert.

## Header padrão para modelo aprovado Meta

URL confirmada por Hebert para envio de mensagem com modelo aprovado Meta:

```text
https://bikon.com.br/wp-content/uploads/2024/09/logo-white.png
```

Usar como header padrão do template `retomar_solicitacao`, salvo aprovação explícita para trocar a imagem.
