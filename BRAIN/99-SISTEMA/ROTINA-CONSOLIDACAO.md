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
