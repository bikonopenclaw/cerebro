# Roteador de Execução v1

```yaml
nome: Roteador de Execução v1
status: etapa_0_concluida
responsavel: Puppet Master
inicio: 2026-07-23
prioridade: media
ultima_revisao: 2026-07-23
tags: [openclaw, modelos, roteamento, governanca, gate-d0]
```

## Objetivo

Selecionar automaticamente o modelo e o nível de pensamento adequados para cada tarefa, considerando padrão conhecido, ambiguidade, impacto, quantidade de sistemas, reversibilidade e confiança.

A seleção cognitiva não amplia autorização. Produção, root, gasto, comunicação externa, mudança real, risco financeiro, backup e rollback permanecem sujeitos aos gates aprovados pelo Hebert.

## Arquitetura proposta

1. Gate D0: decide se a tarefa inteira é determinística e dispensa LLM.
2. Roteador: classifica tarefa, risco, ambiguidade, reversibilidade e confiança.
3. Executor: recebe modelo, pensamento e política de fallback.
4. Validador: mede resultado, latência, retrabalho, falhas e aderência aos gates.

## Perfis propostos

- Determinístico, sem LLM: hashes, contagens, empacotamento, validações estruturais, coletas fixas e transcrição local.
- `gpt-5.3-codex-spark` medium/high: código, patch ou script técnico conhecido, baixo risco, alta confiança e rollback simples.
- `gpt-5.5` high: relatórios, análise profissional, financeiro em leitura, documentos, comunicação e ambiguidade moderada.
- `gpt-5.6-sol` high/xhigh: arquitetura nova, diagnóstico difícil, código novo, integração, segurança e causa raiz.
- `gpt-5.6-sol` max: banco, gateway, incidente, ambiente próprio, risco de perda ou grande impacto.
- `gpt-5.6-sol` ultra: apenas quando houver duas ou mais frentes independentes, ganho real de paralelismo e critério de pronto objetivo.

## Regras duras

- Confiança baixa nunca rebaixa automaticamente para Spark.
- Tarefa crítica não aceita fallback silencioso para modelo inferior.
- Falha de rota em tarefa crítica para no último estado seguro.
- `Ultra` não é sinônimo de qualidade máxima. É perfil de paralelismo.
- Modelo mais forte não substitui aprovação, backup, rollback, teste ou evidência.
- Divergência em rota determinística volta ao roteador para classificação.

## Etapa 0 concluída

- 40 tarefas reais analisadas, oito por agente.
- 36 concluídas, uma parcial, uma bloqueada e duas com falha.
- Quatro casos com retrabalho documentado.
- Oito casos deveriam usar rota determinística sem LLM.
- 12 casos foram recomendados para GPT-5.5 high.
- 14 casos foram recomendados para GPT-5.6-Sol high ou xhigh.
- Seis casos foram recomendados para GPT-5.6-Sol max.
- Nenhum caso justificou ultra.

## Limitações

- A amostra teve boa cobertura de operação, relatório, financeiro e conteúdo, mas pouca cobertura de código e patches técnicos independentes.
- Oito linhas financeiras vieram de subtarefas reais do mesmo pacote NFS-e, o que cria correlação na amostra.
- A latência não pôde ser calculada em 36 dos 40 casos.
- O modelo efetivo apareceu no nível da sessão em parte das tarefas, não necessariamente no nível da subtarefa.

## Decisão atual

- Etapa 0 concluída.
- Troca automática de modelo não autorizada.
- Etapas 1 a 4 não autorizadas.
- Recomendação: ampliar a subamostra técnica e instrumentar timestamps antes de propor a Etapa 1.
- Se aprovada depois, a Etapa 1 deve ser somente shadow mode, sem alteração real de modelo.

## Critério futuro para Etapa 1

- Zero subdimensionamento em tarefa crítica.
- Pelo menos 90% de concordância útil entre recomendação e revisão.
- Registro em UTC de tarefa, risco, modelo, pensamento, confiança, justificativa, fallback e resultado.
- Rollback único para desativar o roteador e restaurar o padrão aprovado.

## Relações

- Diário: `BRAIN/01-DIARIO/2026/2026-07-23.md`.
- Agente operacional: `BRAIN/60-AGENTES/SENTINEL.md`.
- Diretrizes: `BRAIN/99-SISTEMA/MEMORY.md`.
- Artefatos de evidência fora do Brain: `/data/.openclaw/workspace/entregas/roteador-execucao-v1-20260723/`.
