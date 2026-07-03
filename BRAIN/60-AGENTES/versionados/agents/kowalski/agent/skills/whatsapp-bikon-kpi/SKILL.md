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
- tempo de espera até atendimento, medido do status `aguardando` até entrada em `manual`;
- SLA de espera: meta abaixo de 5 minutos;
- tempo de atendimento manual, medido pelo tempo em `manual` ou da entrada em `manual` até finalização;
- SLA de atendimento: meta máxima de 4 horas;
- tempo médio;
- mediana;
- P90;
- maior atendimento;
- outliers;
- satisfação;
- recomendação operacional.

## Filtro padrão de atendentes

Quando o relatório for do WhatsApp Bikon operacional, analisar apenas:

- Hebert Mattedi;
- Felipe Nogueira;
- Fabio Fidelis.

Se a API exigir buscar uma lista ampla antes, filtrar localmente antes de calcular KPI. Não misturar outros atendentes nos totais finais.

## Regra de cálculo de SLA

- Espera: preferir campo nativo de segundos em `aguardando`, quando existir. Alternativa: diferença entre entrada em `aguardando` e transição para `manual` no histórico de status.
- Atendimento: preferir campo nativo de segundos em `manual`, quando existir. Alternativa: diferença entre entrada em `manual` e finalização.
- Se o dado não existir na API, escrever `não disponível pela API`, sem inferir por chute.
- Exibir quantidade e percentual dentro/fora da meta, além de média, mediana e P90 quando houver amostra suficiente.

## Observação técnica

A API documenta filtro por `byStartDate`. Se o pedido for por mês fechado, declarar se a métrica foi filtrada por data de início ou por data de finalização.

## Referência de template aprovado

Template WhatsApp já validado:

- `retomar_solicitacao`
- Header padrão: `https://bikon.com.br/wp-content/uploads/2024/09/logo-white.png`

Kowalski só registra em relatório. Não envia mensagem.
