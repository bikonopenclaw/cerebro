---
id: brain-f819c078460db8166730
type: knowledge
title: Validacao do caminho final instalado
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T20:06:54.602140Z'
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
