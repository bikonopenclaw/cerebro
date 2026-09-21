---
id: brain-8e9ec44fd0edd87d039d
type: state
title: Prov213 — Business Completion Addendum v1 histórico
created: '2026-09-21T19:43:12.426265Z'
updated: '2026-09-21T20:46:44.672892Z'
schema_version: '1.0'
created_semantics: Registro de proposta histórica; não data de aceite ou implementação.
relationships:
- type: references
  target: BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md
  reason: O contrato histórico pertence ao projeto Prov213.
  source: BRAIN/50-PROJETOS/Historico/Prov213-Business-Completion-Addendum-v1.md#contexto-e-escopo
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo.md
  reason: A proposta depende de identidade exata e consumo único.
  source: BRAIN/50-PROJETOS/Historico/Prov213-Business-Completion-Addendum-v1.md#evidência-hash-e-retenção-do-contrato-histórico
---

# Prov213 — Business Completion Addendum v1 histórico

Estado histórico reconciliado: proposta inicial8931, correção de schema e READY_FOR_FIRST_OPERATIONAL_IMPLEMENTATION relatados pela fonte posterior8885, em29/07/2026 às16:53UTC. Os ensaios descritos usavam fixtures não produtivas; isso não comprova teste real de serventia, implantação ou conformidade atual. As decisões se declaravam `LOCAL_OPERATIONAL_DECISION`. Este registro não valida norma jurídica nem torna limites antigos requisitos atuais. A seção do lote13 registra o estado documental posterior e a inclusão obrigatória de modified_time_utc no objeto evidence_items.

## Contexto e escopo

A unidade8931 referia o commit `d31c8b15f3ecc819d99dc11fb8aaca4d972dc779`, árvore `95ecb32fe5161b210d8459fdbe703aaee9a1e736`, para completar lacunas do controle `CTRL-P213-BACKUP-RESTORE-TEST-V1`. A revisão pedida era documental e somente leitura, com veredito READY ou FAIL_CLOSED. Referências ao Provimento213/2026 pertencem à atribuição do documento de origem; não foram revalidadas nesta recuperação. Um controle, uma ação e ciclo coleta→avaliação→finding→aprovação→ação→pós-validação→relatório eram o limite declarado.

## Aplicabilidade e avaliação propostas

- Antes da Etapa4: NOT_APPLICABLE/PHASE_NOT_REACHED. Na Etapa4 ativa ou concluída, o teste seria devido se não houvesse teste conforme anterior ou se a avaliação atingisse seis meses-calendário para classe3, doze para classes1/2. Ainda não devido: NOT_APPLICABLE/TEST_NOT_YET_DUE.
- Entrada, identidade, timestamps ou limites inválidos: INVALID_INPUT. Teste devido com evidência mínima ausente, NOT_EXECUTED ou NOT_VERIFIED: INSUFFICIENT_EVIDENCE.
- COMPLETE, integridade PASS, hashes válidos e RTO/RPO dentro dos limites: CONFORMING; caso contrário, NON_CONFORMING. As fórmulas efetivas de RTO/RPO estavam redigidas na fonte e não foram reconstruídas.
- Limite efetivo proposto: mínimo entre PCN/PRD e teto local por classe. RTO:8h classe3,24h classes1/2. RPO:4h classe3,12h classe2,24h classe1. Estes são valores do contrato histórico, não confirmação de regra CNJ vigente.
- Finding de INSUFFICIENT_EVIDENCE ou NON_CONFORMING teria severidade local ALTA, sem inferir incidente crítico. Sua identidade seria determinística por controle, execução, serventia e decisão.

## Única ação proposta

`ACT-B04-CREATE-VERIFY-RESTORE-SET-V1`: com aprovação humana exata, criar um conjunto completo novo para escopo selado, registrar integridade, restaurar integralmente em ambiente isolado não produtivo, avaliar integridade/RTO/RPO e gerar ata/evidência final. Preservar backups anteriores. Exigir identidade de serventia/ambiente/fonte/manifesto, capacidade isolada e aprovação válida não consumida de tentativa única.

Resultado esperado: reavaliação CONFORMING. Falha: ação FAILED, controle NON_CONFORMING, alerta/chamado, aprovação consumida e nenhum retry automático. A fronteira de rollback era aditiva: isolar/quarentenar novo conjunto e ambiente de teste, preservando evidências. Alterar produção, sobrescrever ou excluir backup anterior seria OUT_OF_SCOPE. Esta nota não autoriza executar a ação.

## Estrutura de dados inicialmente proposta — corrigida posteriormente

Schema fechado (`additionalProperties=false`), todos os campos presentes, inclusive os anuláveis:

- `schema_version` fixo `CTRL-P213-BACKUP-RESTORE-TEST-V1+BCA-v1`; `execution_id` UUID; `serventia_id` CNS; `serventia_class`1/2/3; `operational_phase` BEFORE_ETAPA_4 ou ETAPA_4_ACTIVE_OR_COMPLETED; `assessment_at_utc` RFC3339 UTC Z.
- `last_conforming_test_completed_at_utc` timestamp UTC ou null; `pcn_prd_rto_seconds` e `pcn_prd_rpo_seconds` inteiros positivos.
- `backup_set_id` string/null; timestamps/null `backup_created_at_utc`, `recovery_reference_at_utc`, `last_integral_data_at_utc`, `restore_started_at_utc`, `restore_completed_at_utc`.
- `restoration_result`: NOT_EXECUTED, COMPLETE, PARTIAL ou FAILED; `integrity_result`: NOT_VERIFIED, PASS ou FAIL; `restored_scope` array.
- `evidence_items`: array de objetos exatos com `drive_file_id`, `mime_type`, `byte_length`, `sha256`.
- `action_target_id` string/null; `action_approval` objeto/null. Aprovação com `approval_id`, `approving_human`, `issue_at_utc`, `expires_at_utc`, `action_id`, `target_id`, `environment`, `serventia_id`, `action_manifest_sha256`, `permitted_attempts` fixo1 e `consumption_state` GRANTED/CONSUMED/REVOKED.

Null representava ausência de teste/ação; não autorizava omitir o campo. O documento não fornece aqui um schema JSON executável completo nem comprova implementação.

## Evidência, hash e retenção do contrato histórico

Aquele primeiro ciclo admitia apenas arquivos Drive não nativos com bytes estáveis, obtidos por File ID exato sem conversão. Registrar ID, tamanho, modifiedTime e SHA-256 minúsculo dos bytes. Arquivos Google nativos ou sem bytes estáveis eram inadmissíveis naquele escopo.

Manifesto em JSON UTF-8, chaves ordenadas lexicograficamente, separadores sem espaços e uma quebra LF final; hash vinculava aprovação e pacote final. Aprovação por Hebert ou humano explicitamente delegado, identidade exata de ação/alvo/ambiente/serventia/manifesto, emissão/expiração e consumo na tentativa. Resultado desconhecido bloqueava retry. O contrato propunha evidência final assinada do AnexoV e retenção por cinco anos; isso não impõe retenção permanente de transcrições desta operação de limpeza.

## Relações e proveniência

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|Projeto Prov213]] — contexto do controle e evolução posterior a consultar.
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorização exata]] — identidade e consumo não se renovam por retomada textual.
- [[50-PROJETOS/README|Projetos]] — classificação histórica.

Fonte: unidade8931; hash e ocorrências em `BRAIN/99-SISTEMA/brain-v2/reports/business-addendum-curation-20260921.json`. Nenhum segredo, documento fiscal ou evidência operacional foi alterado.

## Complementos reconciliados — lote 12 de 2026-09-21

Na revisão registrada em29/07/2026 às15:11UTC, anterior à proposta BCA enviada às15:32UTC, PASS técnico EP02 não homologou ciclo operacional. Um addendum crítico corrigiu PASS inicial: faltavam fase/etapa e vencimento, severidade ALTA fixa sem matriz aprovada não era sustentada e teste isolado não remediava toda falha de integridade/RTO/RPO. A proposta BCA posterior tentou explicitar decisões locais, preservada acima, sem comprovação de aceite final nesta revisão. O conflito de referência B.04 exigia fonte oficial antes de orientar cliente; template vazio não comprova execução ou assinatura. Fonte: unidades 8870.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch12-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 13 de 2026-09-21

No BusinessCompletionAddendum posterior, decisões como severidadeALTA e retenção foram rotuladas LOCAL_OPERATIONAL_DECISION, sem atribuí-las aoCNJ. Schema fechado inicialmente conflitava com hashpolicy; consolidou evidence_items com drive_file_id,mime_type,byte_length,modified_time_utc(RFC3339UTCZ),sha256. Revalidação retornou READY_FOR_FIRST_OPERATIONAL_IMPLEMENTATION; ensaios equivalentes em2roots usavam fixturesnão produtivas. Conciliar comreprovação8870: origemlocalexplícita e correção decontrato não são obrigação jurídica universal nem teste real de serventia. Fonte: unidades 8885.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch13-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 15 de 2026-09-21

O resumo histórico de 29/07 às 22:59 relata PASS do Operational_Business_Completion_Addendum_v1.md, 13.488 bytes, SHA-256 f4a9afcbc88ac8d38d234e07cffdc2ec0d633ead5d41fd7698046d6020d1cb6b, além do primeiro ciclo materializado e validação RIC em dois roots (33/23/12 testes). Esse registro é posterior à proposta 8931, à crítica 8870 e ao READY com schema corrigido de 8885; o PASS deve permanecer vinculado à identidade exata desse artefato, sem promover todas as propostas anteriores ou comprovar teste real em serventia. RIC passou a exigir PROV213_REPOSITORY_STATE explícito candidate/committed, com identidade do manifesto quando committed; omissão resultava BLOCKED, e estados known-failure/partial eram terminais bloqueados. Testes em fixtures e readiness documental não são implantação produtiva. Fonte: unidades 8925.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 16 de 2026-09-21

A fonte 8910 confirma o BCA consolidado f4a9afcbc88ac8d38d234e07cffdc2ec0d633ead5d41fd7698046d6020d1cb6b, 13.488 bytes, nos dois roots v2, mas sua rodada do pacote fechou FAIL_CLOSED: o implementation manifest declarado df37ec… não correspondia aos bytes estáveis b435060aa8cdf06f41e6b5f96cb78e1e85f856e5f18d9362ad8b58360f009906. Testes 27/23/12 e igualdade entre roots não corrigiam o binding errado. Distinguir READY/PASS do documento, identidade do pacote e efeito operacional. A evidência posterior 8925 registra evolução; não perpetuar o erro intermediário como bloqueio atual nem apagar sua causa histórica. Fonte: unidades 8910.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch16-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 20 de 2026-09-21

A rechecagem histórica 8916 superou implementation_manifest_hash_mismatch: manifesto b435060a… estável, 23 paths iguais aos dois roots e PASS_BY_KOWALSKI. A materialização colocou 23 arquivos ainda untracked, sem stage/commit/push. A suíte operacional falhou quando PROV213_ADDENDUM_PATH estava ausente e passou com o caminho explícito ao addendum f4a9afcb…; falha de invocação não provava regressão do código. PASS de identidade do endpoint Kowalski era gate separado, sem validar o repositório ou autorizar alterar resolver. A nova revisão RIC começada na cauda ainda não tinha resultado nessa unidade; consultar o parecer posterior 8925. Fonte: unidades 8916.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch20-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
