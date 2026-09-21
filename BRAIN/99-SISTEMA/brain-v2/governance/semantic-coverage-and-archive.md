---
id: brain-ad90ba8266d344cdf7d3
type: state
title: Cobertura, conexões e arquivo semântico
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: false
updated: '2026-09-21T19:08:05.502633Z'
relationships:
- type: derived_from
  target: BRAIN/40-CONHECIMENTO/IA/Brain-como-sistema-de-memoria.md
  reason: Aplica relevância e contexto à cobertura de históricos.
  source: git:2e5f3ed0e3bfcc873f2044df1a3fe80e3097be97:BRAIN/40-CONHECIMENTO/IA/Brain-como-sistema-de-memoria.md
- type: derived_from
  target: BRAIN/40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git.md
  reason: Mantém evidência bruta fora da camada cognitiva e do Git.
  source: git:2e5f3ed0e3bfcc873f2044df1a3fe80e3097be97:BRAIN/40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git.md
---

# Cobertura, conexões e arquivo semântico

## Objetivo e limites

Preservar conhecimento útil antes de retirar históricos do disco da VPS. Esta rotina complementa as consolidações diária, semanal e mensal; um resumo periódico não demonstra, por si só, que todas as fontes foram examinadas.

O pedido de 2026-09-21 autoriza a cobertura e a exclusão posterior dos arquivos elegíveis. O usuário escolheu manter os originais na VPS até concluir a cobertura. O usuário também confirmou que o Mac é transitório: depois da cobertura e da verificação de dependências, as cópias brutas elegíveis podem ser excluídas sem manter um arquivo integral permanente. Esta publicação ainda não executa exclusões de históricos.

## Três provas independentes

1. **Integridade durante a revisão:** cada arquivo foi copiado temporariamente e comparado por tamanho e SHA-256. A cópia permite conferir a fonte enquanto a revisão está aberta; não constitui obrigação de arquivo permanente após o descarte autorizado.
2. **Cobertura:** cada unidade de conteúdo recebeu disposição rastreável: já representada, incorporada, registro histórico sem aprendizado novo, duplicata exata, pendente ou contraditória. Uma decisão útil precisa apontar a nota que a preserva. Arquivo copiado, modelo vetorial e pontuação de similaridade não encerram essa revisão.
3. **Elegibilidade operacional:** não há dependência de sessão/retomada, arquivo aberto relevante, alteração posterior ou erro de leitura. Conferir novamente na VPS imediatamente antes da exclusão. Sessão registrada não significa sessão executando, mas continua sendo uma dependência a reconciliar.

A autorização de descarte exige as três provas, o escopo aprovado e um manifesto explícito. Ausência de textos extraídos não significa ausência de conteúdo útil. Não apagar metadados, compactions, bancos, caches ou plugins apenas por nome ou idade.

## Como conectar as memórias

- Recuperar notas por texto e significado; a pontuação serve para ordenar candidatos.
- Ler as duas fontes e distinguir equivalência, complemento, derivação e contradição.
- Preferir atualizar uma nota existente quando o aprendizado já está representado.
- Registrar relação dirigida com `type`, `target`, `reason` e `source`, usando o vocabulário aprovado.
- Transformar relações já declaradas em links navegáveis; não criar hubs genéricos para melhorar métricas.
- Usar `references` para complemento. Usar `supersedes` apenas quando existir decisão explícita de substituição, com data e evidência; similaridade não significa sucessão.
- Manter fatos antigos datados. Um PASS histórico, instrução citada, plano ou fala de outro agente não é autorização atual nem comprovação independente da execução.

## Pesquisa e arquivo

As notas Markdown, relações justificadas e recibos mínimos ficam no Brain/Git. Transcrições, SQLite, embeddings, modelos e arquivos comprimidos não são conteúdo cognitivo do repositório.

A habilidade `brain-semantic-search` foi instalada na VPS em 2026-09-21. Ela usa um único modelo multilíngue local e um índice derivado fora do Git, em `/data/.openclaw/local/brain-semantic`. A pasta compartilhada de habilidades está em `/data/.openclaw/skills`; os perfis separados de Kowalski e Darth Vader apontam para a mesma habilidade. A descoberta foi conferida pelos catálogos dos agentes e a pesquisa foi executada diretamente. Isso comprova disponibilidade, não que todas as sessões já tenham invocado a habilidade.

Por padrão, a pesquisa privilegia conhecimento permanente; `--scope all` inclui diários, estados e propostas, que exigem interpretação temporal. Resultados mostram caminho, hash, data, relações estruturadas e links explicitamente escritos na nota. Um link declarado é apresentado como tal, sem inferir tipo de relação pelo modelo. Similaridade recupera candidatos; não prova equivalência, autorização ou cobertura. O índice é atualizado por demanda quando os hashes do Brain mudam, reaproveitando notas inalteradas. São mantidas no máximo duas gerações. Toda inferência de embeddings é local, sem API externa.

A habilidade é uma ferramenta explícita, distinta do `memory_search` nativo; a configuração deste último não foi alterada. Código, dependências fixadas e instruções ficam versionados, enquanto o modelo e índice permanecem na VPS. As rotinas periódicas ainda não ganham recibos automáticos apenas por esta instalação.

O arquivo de históricos, seu índice de revisão e o modelo temporário do Mac são descartáveis ao fim desta operação. A eliminação exige encerramento rastreável das unidades úteis, confirmação de publicação e leitura do conhecimento no Brain e nova checagem das dependências dos arquivos. Quando uma duplicata estiver coberta somente por outra fonte bruta, essa fonte continua protegida até que a informação útil seja consolidada ou classificada explicitamente como não durável. Não encadear exclusões apoiadas em cópias que também serão eliminadas.

Após o descarte autorizado não haverá recuperação literal das conversas removidas. Decisões úteis, restrições, aprendizados e relações ficam preservados no Brain. Recibos mínimos com hashes, posições e justificativas documentam a revisão sem publicar transcrições ou credenciais. A proteção de credenciais nos resultados é adicional, não garantia de anonimização.

## Integração às rotinas existentes

- Diária: examinar fontes novas e disposições pendentes; registrar recibos de cobertura por fonte. A agenda sozinha não substitui recibo.
- Semanal: reconciliar repetição, conflito e vínculos; promover padrões revisados a notas permanentes.
- Mensal: verificar continuidade temporal, pendências e retenção do conhecimento e dos arquivos operacionais ainda necessários.

Esta especificação não altera os quatro agendamentos existentes nem o script legado de sincronização. A implementação dos recibos automáticos continua pendente. Nunca apresentar procedimento documentado como automação já ativa.

## Medição honesta

Separar integridade dos links, alcance no grafo, validade dos schemas, validade formal das relações, revisão do significado e cobertura das fontes. Reportar denominadores e itens não medidos. O gate legado fixa duas taxas em 1; seu resultado não comprova qualidade semântica. Usar a validação específica do lote e manter as limitações visíveis.

## Fontes e conexões

- [[40-CONHECIMENTO/IA/Brain-como-sistema-de-memoria|Brain como sistema de memória]] — utilidade futura e contexto.
- [[40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git|Artefatos fora do Git]] — separação de conhecimento e evidência.
- [[99-SISTEMA/brain-v2/governance/README|Governança Brain v2]] — taxonomia, schemas e aprovação.
- [[99-SISTEMA/brain-v2/health/knowledge-health|Knowledge Health]] — métricas e seus limites.
