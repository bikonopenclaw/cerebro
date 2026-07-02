---
name: whatsapp-bikon-kpi
description: Gerar relatórios e KPIs de atendimento do WhatsApp oficial da Bikon via API api.bikon.tech, incluindo volume por status, atendente, tempo médio, mediana, P90, satisfação, abertos e finalizados. Use quando o pedido envolver métricas, relatório, produtividade, SLA ou análise operacional do WhatsApp Bikon.
---

# WhatsApp Bikon KPI

## Escopo do Kowalski

Kowalski é dono de **relatórios e KPIs** do WhatsApp Bikon.

Pode fazer:
- status do canal;
- contagem de atendimentos por status;
- relatório por atendente;
- tempo médio, mediana, P90 e outliers;
- volume diário, semanal e mensal;
- satisfação;
- atendimentos abertos, aguardando e finalizados;
- recomendações operacionais com base nos dados.

Não pode fazer:
- enviar mensagem;
- criar campanha;
- alterar contato, tag, atendimento, setor ou usuário;
- finalizar, transferir ou mexer em atendimento;
- expor token, `.env`, logs brutos ou dados sensíveis.

## Fonte operacional

Workspace ativo:

```bash
/data/.openclaw/workspace/api-bikon-whatsapp
```

Client principal:

```bash
/data/.openclaw/workspace/api-bikon-whatsapp/scripts/bikon_whatsapp_api.py
```

Token real fica em:

```bash
/data/.openclaw/workspace/api-bikon-whatsapp/secrets/.env
```

Nunca imprimir, copiar, versionar ou colar token.

## Guardrails

- Rodar somente endpoints de leitura.
- Antes de entregar relatório, mascarar telefone quando o relatório for para chat.
- Relatório final deve seguir padrão Bikon e, quando for documento, usar a skill `padrao-relatorios-bikon`.
- Se o pedido envolver campanha, template, copy ou retomada de lead, devolver para Puppet Master encaminhar ao Robotnik.
- Se o pedido envolver envio real, devolver para Puppet Master. Envio é travado por aprovação do Hebert.

## Métricas padrão

Sempre que fizer relatório de atendimento, incluir quando disponível:

- total por status;
- abertos manuais;
- aguardando;
- finalizados;
- tempo médio;
- mediana;
- P90;
- maior atendimento;
- outliers;
- satisfação;
- recomendação operacional.

## Observação técnica

A API documenta filtro por `byStartDate`. Se o pedido for por mês fechado, declarar se a métrica foi filtrada por data de início ou por data de finalização.
