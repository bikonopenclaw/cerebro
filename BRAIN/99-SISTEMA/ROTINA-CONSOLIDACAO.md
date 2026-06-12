# ROTINA DE CONSOLIDAÇÃO DO BRAIN

## Princípio

O Brain não é agente. O Brain é o sistema vivo de conhecimento.

O Puppet Master administra o Brain e executa a consolidação com apoio dos agentes quando necessário.

## Frequência

Diária, em modo silencioso, sem interromper o Hebert.

## Horário recomendado

18:05 UTC, depois do horário operacional principal.

## O que analisar

- Decisões tomadas no dia.
- Aprendizados relevantes.
- Projetos citados ou atualizados.
- Empresas citadas ou atualizadas.
- Pessoas relevantes citadas ou atualizadas.
- Riscos identificados.
- Oportunidades identificadas.
- Processos novos ou alterados.
- Alterações nos agentes.
- Automações criadas ou alteradas.

## O que não registrar

- Cumprimentos.
- Conversas triviais.
- Repetições.
- Ruído operacional.
- Informação sem utilidade futura clara.

## Fluxo da consolidação

1. Revisar contexto recente disponível.
2. Identificar conhecimento com utilidade futura.
3. Procurar duplicidade no Brain antes de criar arquivo novo.
4. Atualizar registros existentes quando fizer sentido.
5. Criar registro novo apenas se necessário.
6. Criar ou atualizar diário do dia.
7. Atualizar `BRAIN/99-SISTEMA/CHANGELOG.md`.
8. Atualizar `BRAIN/99-SISTEMA/HEALTH.md` se houver impacto estrutural.
9. Commitar mudanças no Git local.

## Modelo de diário diário

Arquivo: `BRAIN/01-DIARIO/YYYY/YYYY-MM-DD.md`

```markdown
# YYYY-MM-DD

## Pessoas

## Empresas

## Projetos

## Oportunidades

## Problemas

## Decisões

## Aprendizados

## Ideias

## Próximas ações
```

## Regra de ouro

Se a informação não melhora decisão futura, não entra no Brain.

## Rotina semanal

Horário: domingo, 03:00 BRT.

Objetivo:

1. Revisar as daily notes dos últimos 7 dias.
2. Identificar padrões recorrentes.
3. Criar ou atualizar resumo semanal em `BRAIN/01-DIARIO/Semanal/`.
4. Elevar 2 a 5 aprendizados para notas permanentes quando fizer sentido.
5. Arquivar informações sem relevância em `BRAIN/99-ARQUIVO/`.

## Rotina mensal

Horário: dia 1 de cada mês, 03:00 BRT.

Objetivo:

1. Revisar resumos semanais do mês anterior.
2. Consolidar aprendizados do mês.
3. Atualizar MOCs relevantes.
4. Identificar padrões de longo prazo.
5. Arquivar notas sem uso ou sem conexão.
6. Atualizar métricas em `BRAIN/99-SISTEMA/HEALTH.md`.
