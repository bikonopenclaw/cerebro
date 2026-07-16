---
name: "execucao-visivel"
description: "Regra durável para progresso visível e execução real sem encerramento prematuro."
---

# Execução visível

## Objetivo

Garantir que tarefas operacionais iniciem execução real no mesmo turno, mantenham progresso visível sem encerrar prematuramente e parem com evidência quando houver falha.

## Regra obrigatória

1. Usar o canal `commentary` para informar o início da execução e todo progresso intermediário.
2. Nunca usar `message.send` no meio da execução.
3. Reservar `message.send` exclusivamente para a entrega final quando o canal ou a tarefa exigir envio explícito; na conversa de origem, concluir pela resposta final normal.
4. Depois do aviso inicial, iniciar uma ferramenta real no mesmo turno.
5. Em tarefas com duração superior a 5 minutos, informar no `commentary`, a cada 10 minutos:
   - etapa atual;
   - último avanço confirmado.
6. Se qualquer ferramenta, consulta ou validação falhar:
   - parar a execução;
   - apresentar a evidência exata da falha;
   - aguardar decisão do solicitante.
7. Nunca usar fallback, rota alternativa, fonte substituta ou método diferente do autorizado.
8. Não transformar progresso em entrega final enquanto ainda houver trabalho executável pendente.

## Checklist de execução

- Aviso inicial em `commentary`.
- Ferramenta real iniciada no mesmo turno.
- Nenhum `message.send` intermediário.
- Progresso periódico quando aplicável.
- Falha resulta em parada com evidência.
- Nenhum fallback.
- Entrega final somente após conclusão ou bloqueio explícito.
