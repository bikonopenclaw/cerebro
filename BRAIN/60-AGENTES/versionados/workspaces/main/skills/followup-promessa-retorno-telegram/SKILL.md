---
name: "followup-promessa-retorno-telegram"
description: "Agenda follow-up sem duplicar pendencia"
---

# Follow-up Obrigatorio Para Promessa De Retorno

## Objetivo

Sempre que Puppet Master ou qualquer agente prometer retornar depois porque nao tem resposta imediata, a promessa deve virar pendencia rastreavel e agendamento explicito de follow-up no Telegram.

A regra existe para impedir promessa solta, retorno esquecido, cobranca duplicada e tarefa sem dono.

## Quando Acionar

Acionar esta rotina quando houver qualquer frase ou situacao equivalente a:

- `trago isso assim que ficar pronto`;
- `vou aguardar retorno do agente`;
- `quando terminar eu aviso`;
- `assim que gerar eu te mando`;
- tarefa delegada para Kowalski, Darth Vader ou Robotnik sem resposta final imediata;
- execucao longa, dry-run, relatorio, geracao de arquivo, analise externa ou aprovacao pendente;
- qualquer promessa objetiva de retorno feita ao Hebert.

## Campos Obrigatorios Da Pendencia

Toda promessa deve virar pendencia com:

- `pendencia_id`;
- assunto curto;
- origem da promessa;
- dono responsavel;
- agente executor, se houver;
- status: `pendente`, `em_andamento`, `aguardando_terceiro`, `bloqueada`, `concluida`, `cancelada`;
- prazo do primeiro follow-up;
- proximo check;
- criterio de encerramento;
- ultimo status informado ao Hebert;
- quantidade de follow-ups sem avanco.

## ID Unico

Gerar `pendencia_id` antes de agendar.

Composicao recomendada:

`{{data}}|{{chat}}|{{assunto_normalizado}}|{{dono}}`

Antes de criar novo follow-up, procurar pendencia aberta com mesmo assunto, chat e dono.

Se ja existir, atualizar a pendencia existente e reagendar o proximo check. Nao criar duplicata.

## Regra Operacional

Antes de encerrar a resposta ao Hebert:

1. Identificar se houve promessa de retorno.
2. Criar ou atualizar a pendencia.
3. Criar agendamento one-shot de follow-up.
4. Informar status no Telegram no horario do follow-up, mesmo se nao estiver pronto.
5. Se ainda nao estiver pronto, reagendar novo one-shot.
6. Quando entregar o resultado final, marcar como `concluida` ou `cancelada` e nao reagendar.

Follow-up e lembrete pontual, nao cron operacional permanente.

## Prazo Padrao

- Tarefa curta ou agente especialista: primeiro follow-up em 30 minutos.
- Tarefa media, como dry-run ou relatorio: primeiro follow-up em 1 hora se 30 minutos for irrealista.
- Tarefa externa ou longa: usar o menor prazo honesto e registrar a proxima checagem.
- Sem trava de horario para Hebert: se eu prometi retorno, eu cobro e aviso quando vencer.

## Conteudo Minimo Da Mensagem De Follow-up

A mensagem deve seguir o padrao:

```text
1. O que estava pendente: {{assunto}}
2. Status atual: {{status}}
3. Proximo passo: {{acao_ou_novo_horario}}
```

Se ainda nao estiver pronto, dizer isso sem floreio e ja registrar novo follow-up.

## Escalada

Se houver dois follow-ups seguidos sem avanco real:

1. Puppet Master assume cobranca ativa do agente responsavel.
2. Registra o motivo do atraso.
3. Informa Hebert com status limpo.

Se houver tres follow-ups sem avanco:

1. Tratar como tarefa travada.
2. Sugerir troca de abordagem, novo dono ou decisao do Hebert.
3. Nao deixar a pendencia rodando em loop silencioso.

## Encerramento

Uma pendencia so pode ser encerrada quando:

- o resultado prometido foi entregue;
- Hebert dispensou o retorno;
- a tarefa foi cancelada explicitamente;
- a pendencia virou outro fluxo com novo dono e novo `pendencia_id`.

Ao encerrar, registrar motivo e nao reagendar.

## Restricoes

- Nao prometer retorno sem agendamento.
- Nao criar duplicata para a mesma promessa.
- Nao criar cron de producao operacional disfarçado de follow-up.
- Nao usar follow-up para executar mudanca real sem aprovacao.
- Nao expor segredo, token, credencial ou log sensivel na mensagem de status.
- Nao transformar Hebert em fiscal de agente. Puppet Master cobra, consolida e entrega status.

## Regra Final

Promessa sem follow-up nao existe. Se eu disse que volto, o sistema precisa me puxar de volta para fechar o ciclo.
