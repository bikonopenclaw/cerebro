# Plano Roteador de Execução v1

## Controle

- Solicitante: Hebert Mattedi
- Proposta apresentada: 2026-07-23
- Etapa 0 autorizada: 2026-07-23 19:04 UTC
- Estado: Etapa 0 concluída em 2026-07-23
- Escopo autorizado: salvar o plano e executar somente a Etapa 0 em modo read-only
- Fora do escopo: alterar modelo, nível de pensamento, fast mode, agente, cron, skill, gateway, configuração ou produção

## Objetivo

Selecionar automaticamente o modelo e o nível de pensamento mais adequados para cada tarefa, considerando qualidade, risco, latência, reversibilidade, padrão conhecido e custo operacional.

A escolha do modelo nunca amplia autorização. Produção, root, gasto, envio externo, alteração real, risco financeiro e mudança no próprio ambiente continuam sujeitos aos gates aprovados por Hebert.

## Arquitetura proposta

1. Roteador
   - Classifica tarefa, risco, padrão conhecido, ambiguidade, reversibilidade e confiança.
   - Emite um perfil de execução estruturado.

2. Executor
   - Recebe modelo, pensamento, fast mode e política de fallback definidos para a tarefa.
   - Executa somente dentro do escopo e dos gates vigentes.

3. Validador
   - Compara resultado, latência, retrabalho, falhas e aderência aos gates.
   - Alimenta a recalibração do roteador.

4. Gate D0, determinístico
   - Antes de escolher um modelo, verifica se a tarefa pode ser executada integralmente por ferramenta, script ou validador com resultado objetivo.
   - Hash, empacotamento, contagem, validação estrutural e transcrição local não devem consumir um modelo no caminho feliz.
   - Qualquer divergência, exceção ou necessidade de julgamento volta ao roteador.

## Perfis de execução

### Perfil 1. Rápido técnico

- Modelo: `gpt-5.3-codex-spark`
- Pensamento: `medium` ou `high`
- Uso: patch pequeno, script conhecido, ajuste seguindo padrão aprovado, teste repetível e alteração granular com rollback simples.
- Não usar: arquitetura nova, incidente obscuro, migração, produção sensível, financeiro ou mudança no próprio OpenClaw.

### Perfil 2. Padrão profissional

- Modelo: `gpt-5.5`
- Pensamento: `high`
- Uso: relatórios, análise operacional, financeiro, documentos, estratégia, síntese entre fontes, comunicação e tarefas com ambiguidade moderada.
- Regra: porto seguro quando a confiança do roteador não permite rebaixar para Spark.

### Perfil 3. Profundo

- Modelo: `gpt-5.6-sol`
- Pensamento: `high` ou `xhigh`
- Uso: código novo, diagnóstico difícil, integração entre sistemas, segurança, refatoração ampla, arquitetura e causa raiz.

### Perfil 4. Crítico

- Modelo: `gpt-5.6-sol`
- Pensamento: `max`
- Uso: migração de banco, risco de perda de dados, correção no próprio ambiente OpenClaw, recuperação de incidente e mudança com grande impacto potencial.
- Gates: plano, backup, rollback, validação e aprovação.

### Perfil 5. Paralelo

- Modelo: `gpt-5.6-sol`
- Pensamento: `ultra`
- Uso: somente quando houver duas ou mais frentes independentes, critério de pronto objetivo e ganho real com delegação.
- Não usar: tarefa simples, mudança urgente ou investigação dependente de uma sequência única.

## Critérios do roteador

Cada tarefa deve ser classificada por:

1. Padrão conhecido.
2. Ambiguidade.
3. Impacto se der errado.
4. Quantidade de sistemas e arquivos envolvidos.
5. Reversibilidade.
6. Confiança da classificação.

## Regras duras

- Padrão alto, risco baixo e rollback simples: avaliar Spark.
- Ambiguidade média ou trabalho não técnico: GPT-5.5.
- Novidade, integração ou diagnóstico difícil: GPT-5.6-Sol.
- Alto impacto ou ambiente próprio: GPT-5.6-Sol `max`.
- Frentes independentes: avaliar `ultra`.
- Confiança baixa: nunca rebaixar automaticamente para Spark.
- Tarefa crítica: sem fallback silencioso para modelo inferior.
- Falha de modelo ou rota em tarefa crítica: parar no último estado seguro.
- Produção, root, gasto, envio externo e alteração real mantêm os gates existentes.
- Fast mode é decisão separada do nível de pensamento e depende de política de custo aprovada.

## Plano cadenciado

### Etapa 0. Baseline read-only

- Prazo de referência: 1 dia.
- Selecionar 40 tarefas reais já executadas.
- Medir resultado, retrabalho, latência observável, risco e perfil recomendado.
- Entregar matriz de roteamento v0 e conjunto de testes.
- Nenhuma configuração alterada.

### Etapa 1. Shadow mode

- Duração de referência: 5 dias úteis.
- O roteador recomenda modelo e pensamento, mas não troca nada.
- Comparar recomendação com resultado real.
- Gate: zero subdimensionamento em tarefas críticas e pelo menos 90% de concordância útil.
- Estado: não autorizada.

### Etapa 2. Piloto controlado

- Duração de referência: 7 dias.
- Automatizar somente tarefas técnicas mapeadas e de baixo risco com Spark.
- Usar GPT-5.6-Sol em tarefas profundas com registro e revisão.
- Limite inicial: 20% das execuções.
- Rollback para GPT-5.5 `high` em erro de rota.
- Estado: não autorizada.

### Etapa 3. Expansão por agente

- Duração de referência: 7 dias.
- Kowalski: Spark para rotinas técnicas fechadas; GPT-5.5 para relatórios e exceções.
- Darth Vader: GPT-5.5 para análise financeira; GPT-5.6 para automação e integração complexa.
- Robotnik: Spark para ajustes técnicos padronizados; GPT-5.5 para campanha, copy e julgamento de marca.
- Sentinel: manter GPT-5.6 até os testes provarem que alguma rotina read-only pode ser rebaixada sem perda de sensibilidade.
- Puppet Master: GPT-5.5 para coordenação normal; GPT-5.6 para estratégia, arquitetura e crise.
- Estado: não autorizada.

### Etapa 4. Produção governada

- Registrar em UTC: tarefa, risco, modelo, pensamento, confiança, justificativa, fallback e resultado.
- Revisão semanal no primeiro mês.
- Recalibração mensal ou quando entrar modelo novo.
- Rollback único desativa o roteador e devolve todos ao GPT-5.5 `high`.
- Estado: não autorizada.

## Critérios de avaliação da Etapa 0

- Amostra: 40 tarefas reais.
- Distribuição: 8 tarefas de cada agente, Puppet Master, Kowalski, Darth Vader, Robotnik e Sentinel.
- Cobertura mínima:
  - sucesso;
  - bloqueio;
  - falha;
  - rotina padronizada;
  - diagnóstico;
  - relatório;
  - conteúdo;
  - financeiro;
  - operação.
- Latência: do primeiro pedido até a primeira resposta final útil, somente quando os timestamps permitirem.
- Retrabalho: somente quando houver correção, repetição por falha, reabertura ou entrega refeita documentada.
- Dados ausentes devem ser marcados como `N/D`.

## Entregáveis da Etapa 0

1. Baseline com 40 tarefas e evidências.
2. Matriz de roteamento v0.
3. Conjunto de 40 casos de teste.
4. Estatísticas agregadas.
5. Limitações da amostra.
6. Recomendação para decidir se a Etapa 1 merece aprovação.

## Fechamento da Etapa 0

- Os 40 casos foram coletados e revisados.
- A amostra mostrou que o primeiro gate deve decidir se a tarefa precisa de LLM.
- O uso de Spark ainda não foi validado empiricamente por tarefas técnicas independentes suficientes.
- O modo `ultra` não foi recomendado em nenhum dos 40 casos.
- A Etapa 1 permanece não autorizada.

## Rollback futuro

Se uma etapa posterior for aprovada e produzir erro de rota, o rollback proposto é:

1. Desativar o roteador.
2. Limpar overrides criados pela etapa.
3. Restaurar GPT-5.5 com pensamento `high` como padrão.
4. Validar agentes, sessões e jobs afetados.
5. Registrar evento de auditoria e causa do rollback.

Este rollback é apenas planejado. Nenhuma ação de implementação está autorizada neste documento.
