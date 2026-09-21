---
id: brain-05c5983554b099eafabd
type: state
title: Rotina de consolidação do Brain
created: '2026-09-21T19:14:26.441708Z'
created_semantics: Data de registro estruturado; o documento de rotina é anterior.
updated: '2026-09-21T20:06:54.602140Z'
schema_version: '1.0'
legacy_content_preserved: true
relationships:
- type: references
  target: BRAIN/99-SISTEMA/brain-v2/governance/semantic-coverage-and-archive.md
  reason: Aplica os critérios de cobertura e reconciliação à rotina central existente.
  source: user-request-20260921-brain-coverage; gateway-brain-coverage-20260921.json
---

# ROTINA DE CONSOLIDAÇÃO DO BRAIN

## Princípio

O Brain não é agente. O Brain é o sistema vivo de conhecimento.

O Puppet Master administra o Brain e executa a consolidação com apoio dos agentes quando necessário.

## Frequência

Diária nos dias úteis, em modo silencioso, sem interromper o Hebert.

## Horário verificado

23:00 America/Sao_Paulo, segunda a sexta. Configuração do agendador conferida em 2026-09-21; o horário anterior neste documento estava desatualizado.

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

Horário: dia 1 de cada mês, 04:00 America/Sao_Paulo, conforme configuração verificada em 2026-09-21.

Objetivo:

1. Revisar resumos semanais do mês anterior.
2. Consolidar aprendizados do mês.
3. Atualizar MOCs relevantes.
4. Identificar padrões de longo prazo.
5. Arquivar notas sem uso ou sem conexão.
6. Atualizar métricas em `BRAIN/99-SISTEMA/HEALTH.md`.

## Cobertura entre gateways e pesquisa semântica

Kowalski e Darth Vader usam gateways/perfis separados. A consolidação central não deve presumir que toda conversa desses perfis já está no contexto do Puppet Master. A conferência de 21/09 encontrou memórias Kowalski versionadas e conteúdo FIP/Darth parcialmente consolidado, mas nenhum recibo que provasse cobertura integral por fonte.

Na execução autorizada, delimitar período e inventariar as fontes disponíveis por agente: memórias em `/data/.openclaw/workspace-<agente>/memory/`, registros operacionais pertinentes e históricos explicitamente elegíveis. Usar somente acessos já autorizados; se uma fonte não puder ser lida, registrar lacuna e manter a cobertura parcial. Arquivos iguais por hash não precisam de nova promoção, mas a disposição anterior precisa existir. Não confundir snapshot de código/skill com consolidação cognitiva de conversas.

A habilidade compartilhada `brain-semantic-search` orienta pesquisa, reconciliação e arquivamento semântico. Procurar notas existentes, preservar contexto/data/escopo e qualificar regras superadas por decisões posteriores explícitas. Similaridade e quantidade de links não comprovam significado nem cobertura.

Registrar no fechamento fontes examinadas, hashes ou identidades verificáveis, disposições, notas-alvo e pendências. Separar revisão concluída, commit local e publicação remota confirmada: execução do cron marcada OK não prova push nem cobertura. Quando faltarem recibos por fonte, não declarar que todos os agentes enviaram tudo.

Estas instruções complementam as rotinas existentes. A pesquisa persistente está instalada; não foi implantado um coletor automático completo de todas as fontes ou um mecanismo de exclusão automática. Descarte exige o protocolo de cobertura e autorização aplicável, com nova verificação operacional.

- [[99-SISTEMA/brain-v2/governance/semantic-coverage-and-archive|Protocolo de cobertura e arquivamento]]
- Evidência da agenda e dos perfis: `BRAIN/99-SISTEMA/brain-v2/reports/gateway-brain-coverage-20260921.json`.

## Inventário obrigatório da janela de consolidação

Os agendamentos diário, semanal e mensal já apontam para este documento. Em cada execução, iniciar com `python3 /data/.openclaw/workspace/Brain/scripts/brain-source-inventory.py --days 7`. A janela móvel de sete dias inclui o intervalo do fim de semana; retomar pendências mais antigas registradas nos recibos. Para a mensal, usar também a janela de 35 dias quando a continuidade semanal não estiver comprovada.

O inventário somente lista arquivos e metadados de main, Kowalski, Darth Vader, Robotnik e Sentinel nos perfis reais. Não lê o conteúdo nem atribui cobertura. Selecionar as fontes por agente, ler as unidades pertinentes, calcular sua identidade ao revisar e registrar disposição individual. Mudança de tamanho/data após a leitura exige nova verificação. Memória ausente, fonte inacessível, limite de execução ou fila não lida são lacunas explícitas, não ausência de conhecimento.

Salvar recibo sanitizado em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-<data>-<ciclo>.json`, com janela, agente/perfil, caminho/hash da fonte, unidades ou intervalo efetivamente lido, disposição, nota-alvo, pendências e publicação comprovada. Não registrar payloads brutos ou credenciais. Sem leitura completa do escopo declarado, informar cobertura parcial e carregar a fila para a execução seguinte. Reutilizar recibos apenas quando a identidade da fonte e a disposição anterior coincidirem.

A inclusão deste inventário torna a exigência executável pelas rotinas existentes; não prova que uma execução futura já ocorreu nem que todo histórico vivo está consolidado. Nenhuma exclusão automática foi adicionada.
