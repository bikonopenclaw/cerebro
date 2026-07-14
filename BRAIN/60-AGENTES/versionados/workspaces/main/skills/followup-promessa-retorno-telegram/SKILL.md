---
name: "followup-promessa-retorno-telegram"
description: "Agenda follow-up quando retorno ficar pendente"
---

# Follow-up obrigatório para promessa de retorno

## Objetivo

Sempre que Puppet Master ou qualquer agente prometer retornar depois porque não tem resposta imediata, a promessa deve virar agendamento explícito no Telegram.

## Quando acionar

Acionar esta rotina quando houver qualquer frase ou situação equivalente a:

- "trago isso assim que ficar pronto";
- "vou aguardar retorno do agente";
- "quando terminar eu aviso";
- "assim que gerar eu te mando";
- tarefa delegada para Kowalski, Darth Vader ou Robotnik sem resposta final imediata;
- execução longa, dry-run, relatório, geração de arquivo, análise externa ou aprovação pendente.

## Regra operacional

Antes de encerrar a resposta ao Hebert, criar um agendamento de follow-up no Telegram.

O agendamento deve:

1. verificar o status da pendência;
2. mandar retorno no Telegram mesmo que ainda não esteja pronto;
3. se ainda não estiver pronto, criar novo agendamento de follow-up;
4. não depender de memória humana nem de boa vontade do agente executor.

## Prazo padrão

- Tarefa curta ou agente especialista: primeiro follow-up em 30 minutos.
- Tarefa média, como dry-run ou relatório: primeiro follow-up em 1 hora se 30 minutos for irrealista.
- Tarefa externa ou longa: usar o menor prazo honesto e registrar a próxima checagem.
- Fora do horário de trabalho do Hebert: reagendar para o próximo horário útil, salvo emergência.

## Conteúdo mínimo da mensagem de follow-up

A mensagem deve seguir o padrão:

1. O que estava pendente.
2. Status atual.
3. Próximo passo ou novo horário de follow-up.

## Escalada

Se houver dois follow-ups seguidos sem avanço real, Puppet Master deve assumir cobrança ativa do agente responsável e reportar bloqueio limpo para Hebert.

Se houver três follow-ups sem avanço, tratar como tarefa travada e pedir decisão ou trocar abordagem.

## Restrições

- Não prometer retorno sem agendamento.
- Não criar cron de produção operacional disfarçado de follow-up.
- Não usar follow-up para executar mudança real sem aprovação.
- Não expor segredo, token, credencial ou log sensível na mensagem de status.
