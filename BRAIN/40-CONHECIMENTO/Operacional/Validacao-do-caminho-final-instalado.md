---
id: brain-f819c078460db8166730
type: knowledge
title: Validacao do caminho final instalado
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T21:16:57.672344Z'
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Deploy-atomico-de-skills-com-hash-canonico.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado.md#relações
- type: references
  target: BRAIN/01-DIARIO/Semanal/2026-W31.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado.md#relações
---

# Validacao do caminho final instalado

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W31
confiabilidade: alta
ultima_revisao: 2026-08-02
tags: [instalacao, launcher, black-box, dre, runtime, validacao]
```

## Principio

Teste em clean root, pre-install ou commit preservado nao comprova que a ferramenta instalada funciona. O caminho final usado pelo operador precisa ser validado em black-box.

## Gate minimo

1. Instalar no caminho final esperado.
2. Executar o binario ou launcher pelo mesmo comando que o usuario usara.
3. Confirmar que caminhos internos sao relocatable ou calculados a partir do local correto.
4. Validar saida, exit code, logs e ausencia de dependencia acidental do diretorio de build.
5. Reverter a instalacao se o caminho final resolver artefato incorreto.

## Exemplo conectado

Na semana 2026-W31, o OpenClaw DRE v1 tinha commit preservado, `75/75` testes pre-install e `git fsck` PASS, mas a instalacao foi revertida porque `/usr/local/bin/openclaw-dre` resolvia incorretamente `/usr/local/src/dre.py`. O estado correto ficou como nao instalado.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao|Validação do runtime pós-migração]]
- [[40-CONHECIMENTO/Operacional/Deploy-atomico-de-skills-com-hash-canonico|Deploy atômico de skills com hash canônico]]
- [[01-DIARIO/Semanal/2026-W31|Semana 2026-W31, cobertura parcial]]

## Complementos reconciliados — lote 6 de 2026-09-21

Na validação histórica do DRE, uma fixture que deveria provocar erro interno 7 retornou legitimamente TRANSACTION_NOT_FOUND 5; em outra tentativa, exit esperado 2 disparou trap ERR antes da asserção. O harness precisa distinguir saída esperada do domínio de falha do próprio teste, exercitar a rota instalada real e congelar fixtures válidas. Um teste mal especificado não prova defeito de produção nem autoriza repetir ordem encerrada. Fonte: unidades 33946, 33985.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 7 de 2026-09-21

A aceitação histórica do Shadow Mode rejeitou uma suíte verde porque não havia call site no fluxo real. Também separou exceção de comparador, timeout com thread ainda viva e classificação C0 sem LLM. Validar integração efetiva e terminalidade de falhas, não somente testes da biblioteca. Fonte: unidades 34544.

Uma revisão encontrou controller criando automaticamente `.prov213-shadow-root` em qualquer root recebido pela CLI. Isso transforma rótulo em autorização e invalida isolamento: aceitar somente root de teste previamente preparado pela rota explícita e validar que ambiente produtivo continua rejeitado. Testes verdes não substituem esse controle negativo. Fonte: unidades 37175.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 9 de 2026-09-21

Na validaçãoGoldenBaselineProv213, PROTECTED_SURFACE_HASHES.csv usava surface,sha256, enquanto o checker esperava path,size e falhou comKeyError. Validar schema e semântica do manifesto: hash de superfície contratual e inventário de arquivos são provas diferentes. Corrigir checker e repetir a leitura do mesmo pacote antes do veredito; aprovação do indexer staged não prova execução de1003objetos, e falhaOAuth não demonstra defeito do indexer. Fonte: unidades 9873.

No contrato históricoPortal213Stage1A.2, a aplicação precisava validar config no próprio masterGunicorn antes de aceitar conexão; ExecStartPre separado não bastava. Loaderreal validava arquivo regular/não symlink, owner/group/mode antes de ler e ficava inalcançável no canário sintético. Validar origin estruturalmente (semuserinfo,portaalternativa,query,fragmento,lookalike), limitar logs a camposallowlisted semrawpath/query/token e provar ausência de sentinelas emstdout/stderr/journal. Release único mínimo, hashes/permissões porpath, rollback pelo estado capturado e isolamento loopback/semcredenciais reais pertenciam ao gateoffline; não autorizavamStage1B/1C. Teste de string da configuração não comprova enforcement do processo em execução. Fonte: unidades 29316.

Na revisãoODPDay3, executor aceito chamava psql direto em0000/0001/0002 e não chamava o runner externo. OsSQL criavamapplied_migrations mas não inseriam oledger; corrigir apenascandidate/runner não corrigia a rota produtiva. O caminho efetivamente invocado precisa exercitar ledger/atomicidade/checksum; aprovação da instalação não prova comportamento de migração. Não usarhashSQL autorreferente como atalho nem alterar executor congelado fora do escopo. DossierV2/testes prévios ainda exigiam inspeção do callsite real, seminferir promoção. Fonte: unidades 9648.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch9-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 10 de 2026-09-21

No gate DRE, harness/contrato esperavam PACKAGE_OR_PREFLIGHT_FAILURE e ATTESTATION_VERIFICATION_FAILURE, mas fonte/testes congelados emitiam PACKAGE_OR_PREFLIGHT_IO_FAILURE e ATTESTATION_INVALID. Concordar em exitcode não basta quando classificação exata faz parte do contrato; reconciliar artefatos autorizados e hashes, sem alias silencioso. Fixture com path onde o contrato exige relative_path era inválida, não defeito do validador. Separar raiz única de evidência de múltiplas state roots ao avaliar o critério, sem declarar equivalência não acordada. Fonte: unidades 9801.

Na validação EDC, validator local e8testes passaram enquanto Draft2020-12 independente rejeitava propriedades adicionais em cinco documentos canônicos. Validar bindings documento→schema congelado e required/const/additionalProperties, sem afrouxar schema para aprovar saída. O chmod0644 não ampliava execução, mas contradizia proibição e declaração de zerochmod: efeito técnico pequeno não torna recibo inexato aceitável. Reconciliação deve registrar desvio e evidência independente da versão corrigida; processo internoPASS não comprova ativação. Fonte: unidades 8823.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 12 de 2026-09-21

Na aceitaçãoDRE histórica, fixtureusou path onde contrato exigia relative_path; campo ausente virou stringvazia e produziu UNSAFE_PATH. Corrigir fixture, não afrouxar validador. Exitcodeinterno7 não era reproduzível pela rota públicaque retornava TRANSACTION_NOT_FOUND: separar provas de suíte/revisão e black-box, sem fabricar rota para satisfazer teste. Relato terminou antes da aceitaçãofinal, depois tratada em outraetapa. Fonte: unidades 33967.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch12-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 13 de 2026-09-21

No DRE v1 de 01/08, launcher relocatable e 91 testes pós-instalação passaram, mas black-box de pacote inexistente devolveu exit 7 quando o contrato exigia 2. A falha ocorreu antes de renderizar e bloqueou aceite; o rollback foi solicitado apenas para os dois alvos instalados, condicionado a hashes esperados. Separar sucesso de instalação, contrato de erro e aceite black-box. O screenshot posterior sem texto extraído neste trecho não comprova que rollback ocorreu; confirmação requer recibo/estado posterior, não inferência da autorização. Fonte: unidades 32802.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch13-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 15 de 2026-09-21

Na validação histórica cleanroots, dois outputs concordantes ainda podiam divergir do perfil autorizado; em seguida, a identidade do manifesto também precisou ser reconciliada. Validar a cadeia perfil → manifesto → geração → outputs, incluindo a convenção de bytes e normalização exigida pelo contrato. Não substituir hash bruto por hash de texto normalizado silenciosamente. O PASS posterior de 8927 supera esses bloqueios históricos, sem dispensar a ligação de origem para futuras gerações. Fonte: unidades 8903.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 16 de 2026-09-21

Na revisão Shadow R4 de 25/07, validate_target() aprovava o primário enquanto <primary>.lock era symlink; a primeira escrita falhava e deixava o destino vazio. Validar os mesmos recursos e tipos usados no caminho real, incluindo lock e companion, sem seguir links ou bloquear em FIFO. Um companion inválido não deve inutilizar silenciosamente um destino primário saudável. Na leitura de relatório, primário UTF-8 inválido e fallback válido produziram rc 2, report_complete=false e os registros válidos preservados; isso é parcial explícito, não PASS completo. O primeiro timeout de FIFO não se reproduziu, portanto não foi elevado a defeito confirmado. Snapshot/testes antigos não dispensam revalidação após mudança do diff. Fonte: unidades 41427.

Na validação histórica EP-02, null na raiz é um valor JSON materializado válido; usar None como sentinela de ausência fez o teste confundir a mutação válida com falha de materialização. Separadamente, converter tuple para list antes de verificar o perfil permitia entrada não JSON que deveria ser rejeitada: esse era defeito de implementação. Usar sentinela distinta e validar tipos antes de normalizações destrutivas. Contar casos apenas na seção correspondente e calcular agregado com o wrapper definido pela versão do contrato. A correção documental CTM teve PASS_DOCUMENTATION_ONLY; o estado homologado posterior com 23/23 testes supera os bloqueios desse checkpoint. Fonte: unidades 8858.

No EP-02A, run1 e run2 byte-idênticos, contagens corretas e hashes reproduzíveis não bastavam quando o commitment usava preimage diferente da ADR congelada. A regra do preimage deve ser ligada ao hash e à versão da fonte normativa, evitando misturar revisões posteriores. Pacote anunciado como congelado que muda durante a revisão exige nova submissão coerente. Correções já verificadas de LEFT/RIGHT e inclusão de semantic_commitment não permanecem como bloqueadores; os checkpoints posteriores do projeto substituem os FAIL intermediários. Fonte: unidades 9755.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch16-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 20 de 2026-09-21

No DRE v1 de 01/08, duas árvores idênticas e 75 testes não bastaram para o commit: a regra bin/ do .gitignore excluía o launcher, deixando somente 11 dos 12 paths no stage simulado. Comparar inventário físico autorizado, regras de ignore e conteúdo efetivamente commitado antes de empacotar. A nova tentativa autorizou force-add apenas do launcher, sem alterar a política global; o commit de 12 paths ainda precisava de instalação e teste pela rota real, que depois revelou outro problema. Não confundir autorização de force-add restrito com liberação de arquivos ignorados em geral. Fonte: unidades 33089.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch20-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 21 de 2026-09-21

No DRE v1 de 01/08, a execução passou gates 1–9, mas antecipou testes de attestation inválida e transação inexistente antes dos gates obrigatórios de resume entre processos e entre turnos; terminou FAIL_CLOSED_ROUTE_DEVIATION. Uma tentativa posterior foi fechada antes do Gate 1 por conflito de start/controller, com zero gates executados. Conjunto de testes úteis não substitui sequência contratada, e interrupção de orquestração não é evidência de novo defeito no DRE. Rollback solicitado não significa rollback executado; a instalação/aceitação posterior pertence a outro checkpoint. Fonte: unidades 32824.

Na aceitação histórica DRE de 01/08, preflight, run sintético, determinismo, publicação e journal passaram, mas o executor antecipou testes de attestation inválida/transação inexistente antes dos gates obrigatórios de resume e fronteira de turno. O resultado foi FAIL_CLOSED_ROUTE_DEVIATION, não aprovação parcial da instalação. Quando o contrato congela sequência, sucesso isolado dos testes não substitui percurso autorizado e estado terminal. A solicitação de rollback e preparação posterior de reinstalação são etapas distintas, sem prova automática da execução pelo texto da ordem. Fonte: unidades 32822.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch21-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 22 de 2026-09-21

No Harness DRE v3 histórico, o Gate 04 falhou com PACKAGE_OR_PREFLIGHT_IO_FAILURE porque --package recebeu o diretório da fixture, embora o contrato exigisse o arquivo manifest.json. O preflight direto com o arquivo passou e os 12 caminhos congelados permaneciam equivalentes. A correção v4 autorizada separava FIXTURE_ROOT de FIXTURE_MANIFEST, exigia validação dos bytes do harness/instalador e wrapper que somente declarasse PASS após preflights reais, com rollback em divergência. A preparação e o PASS local não autorizavam instalação nem execução do novo harness; houve parada obrigatória no gate root. Esse checkpoint antecede a instalação posterior e não indica defeito atual. Fonte: unidades 30780.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch22-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 23 de 2026-09-21

Na revisão pós-commit EP-02, o parecer PASS foi sustentado por 23 testes e reprodução independente do relatório normalizado, sem ler como entrada o relatório fornecido pelo executor. O JSON compacto usava ordem fixa, UTF-8 e nenhum newline final; já o manifesto de caminhos exigia ordem da Seção 12 e newline final. Aplicar a convenção de bytes de cada artefato, sem uma normalização genérica. Esse aceite homologava o kernel técnico; a discussão seguinte ainda apontava ausência de perfil e fluxo de negócio concretos, anterior ao Business Completion posterior. Fonte: unidades 8864.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch23-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 25 de 2026-09-21

Na revisão histórica do Shadow Mode, o candidato inicial falhou por timeout permissivo, duplicação entre primário/fallback e relatório sem deduplicação. O commit d217f53c0c76f461d5f3058dfab4e3bdf5f28043 corrigiu os probes finais: validar escrita, leitura regular segura e lock antes do handoff; companion inválido não deve impedir primário saudável; JSON completo sem newline continua válido. Persistência usava lock interprocesso e busca integral limitada pelo deadline, não apenas tail fixo; mesmo execution_id com conteúdo conflitante abortava relatório, duplicata equivalente podia colapsar. Entrada inválida preservava resultado parcial explicitamente incompleto, rc 2. Os alertas finais eram de versões intermediárias e não se reproduziram no SHA entregue. A quinta revisão integral estava apenas iniciada; probes finais pontuais não comprovam todos os gates dessa nova rodada nem estado atual. Fonte: unidades 41428.

Nas revisões históricas EP-02A, contagens e duas gerações byte idênticas passaram enquanto o FIM usava mutações genéricas em /payload/value para defeitos de outros campos. Depois persistiram casos LEFT/RIGHT indistintos e colisões esperadas antes de recompor commitments, que na verdade acionavam primeiro DATA_HASH_MISMATCH. Um caso negativo deve atingir a condição nomeada, distinguir os lados e satisfazer precondições dos gates anteriores; determinismo não prova adequação semântica. A leitura seguinte confirmou correções LEFT/RIGHT e ausência de no-op, e o freeze final posterior passou. Arquivo anunciado congelado que muda durante a revisão exige nova submissão coerente, sem reutilizar hashes ou stdout antigos. Fonte: unidades 9740, 9743.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch25-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 26 de 2026-09-21

A pré-validação DRE v2 reconciliou exatamente Gates 03 e 12 com o código congelado: PACKAGE_OR_PREFLIGHT_IO_FAILURE/exit 2 e ATTESTATION_INVALID/exit 6. Manteve 13 gates, ordem, comandos e códigos esperados, preservou artefatos antigos e passou revisão independente. Exit 7 continuava falha interna, não aceitação pública; raiz-mãe única de evidência não significa uma única state-root para todos os gates. A revisão v3 seguinte examinou capture_expected_exit para 2/5/6 sem desativar ERR trap para falha inesperada; o checkpoint ainda não executou harness nem instalou DRE. Reconciliar pré-validação, execução e instalação como provas distintas. Fonte: unidades 9803.

O defeito histórico CPIW de autoautorizar root foi posteriormente fechado em 07/08: setup explícito, binding anti-cópia/tamper, rejeição imutável de root arbitrário/canônico/produtivo, 179 testes e ciclo shadow de 311 operações com rollback e idempotência. Kowalski validou staging e cópia limpa após promoção de quatro caminhos pelo coordenador; não promoveu nem escreveu AIR/ICD produtivo. Baseline de staging, cópia limpa e caminho canônico tinham identidades distintas e não eram intercambiáveis. A próxima superfície AUTHORITATIVE_PRODUCTION iniciada na cauda era autorização/validação separada. Isto supera o bloqueio antigo sem provar estado produtivo atual. Fonte: unidades 9817.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch26-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
