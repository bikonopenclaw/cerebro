---
id: brain-ad90ba8266d344cdf7d3
type: state
title: Cobertura, conexões e arquivo semântico
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: false
updated: '2026-09-21T17:53:52Z'
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

O pedido de 2026-09-21 autoriza a cobertura e a exclusão posterior dos arquivos elegíveis. O usuário escolheu manter os originais na VPS até concluir a cobertura. Este lote não autoriza nem executa exclusão.

## Três provas independentes

1. **Preservação:** cada arquivo foi copiado para armazenamento externo e comparado por tamanho e SHA-256. Isso comprova os bytes disponíveis para recuperação.
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

As notas Markdown e as relações justificadas ficam no Brain/Git. Transcrições, SQLite, embeddings, modelos, arquivos comprimidos e manifestações completas de sessões ficam no arquivo privado externo.

A ferramenta local `scripts/brain-semantic-search.py` pesquisa as notas por embeddings multilíngues. Com `--archive`, recupera até 100 candidatos pelo índice textual e os reordena semanticamente. Esse modo é híbrido; não equivale a uma busca vetorial exaustiva de todos os históricos. Por padrão a pesquisa privilegia conhecimento permanente; `--scope all` inclui diários, estados e propostas, que exigem interpretação temporal.

Resultados mostram origem e status de evidência histórica. O filtro de credenciais é uma proteção adicional, não uma garantia de anonimização. Não publicar resultados brutos. Toda indexação é local, sem transmitir conteúdo para API de embeddings. Reconstruir o índice quando hashes das notas mudarem; registrar modelo, versão, fragmentação e testes de recuperação.

O catálogo no Git registra identificador do arquivo, hash, quantidades, estado de cobertura e referências mínimas. O manifesto privado permite reconstruir arquivo, hash e linha sem carregar milhares de logs no repositório. O pacote local não passa a ser acessível aos agentes da VPS automaticamente: a consulta foi instalada no Mac, e integração ao runtime exige uma etapa própria.

## Integração às rotinas existentes

- Diária: examinar fontes novas e disposições pendentes; registrar recibos de cobertura por fonte. A agenda sozinha não substitui recibo.
- Semanal: reconciliar repetição, conflito e vínculos; promover padrões revisados a notas permanentes.
- Mensal: verificar continuidade temporal, pendências, recuperação externa e retenção.

Esta especificação não altera os quatro agendamentos existentes nem o script legado de sincronização. A implementação dos recibos automáticos continua pendente. Nunca apresentar procedimento documentado como automação já ativa.

## Medição honesta

Separar integridade dos links, alcance no grafo, validade dos schemas, validade formal das relações, revisão do significado e cobertura das fontes. Reportar denominadores e itens não medidos. O gate legado fixa duas taxas em 1; seu resultado não comprova qualidade semântica. Usar a validação específica do lote e manter as limitações visíveis.

## Fontes e conexões

- [[40-CONHECIMENTO/IA/Brain-como-sistema-de-memoria|Brain como sistema de memória]] — utilidade futura e contexto.
- [[40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git|Artefatos fora do Git]] — separação de conhecimento e evidência.
- [[99-SISTEMA/brain-v2/governance/README|Governança Brain v2]] — taxonomia, schemas e aprovação.
- [[99-SISTEMA/brain-v2/health/knowledge-health|Knowledge Health]] — métricas e seus limites.
