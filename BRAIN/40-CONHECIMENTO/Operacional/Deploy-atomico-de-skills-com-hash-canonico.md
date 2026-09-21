---
id: brain-3e9ac6eb255c95ad45d8
type: knowledge
title: Deploy atômico de skills com hash canônico
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T21:16:57.672344Z'
relationships:
- type: references
  target: BRAIN/01-DIARIO/2026/2026-07-20.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Deploy-atomico-de-skills-com-hash-canonico.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Deploy-atomico-de-skills-com-hash-canonico.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Deploy-atomico-de-skills-com-hash-canonico.md#relações
---

# Deploy atômico de skills com hash canônico

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: implantação Instagram Brand Director v2.1.0 em 2026-07-20
confiabilidade: alta
ultima_revisao: 2026-07-20
tags: [skills, deploy, atomicidade, hash, backup, rollback, auditoria]
```

## Princípio

Uma skill só deve ser considerada implantada quando conteúdo, algoritmo de hash, plano, backup, troca, validação e evidência formarem um único protocolo verificável. Copiar arquivos sobre a árvore ativa não oferece atomicidade nem rollback confiável.

## Plano imutável

Antes da janela, congelar um plano com:

1. caminho ativo e staging irmão no mesmo filesystem;
2. inventário e hash esperados da árvore ativa e da candidata;
3. nome e versão do algoritmo canônico de hash;
4. correlation ID único;
5. aprovação vinculada ao plano e aos hashes;
6. validators pré-corte e pós-corte;
7. caminhos de backup, evidência e rollback;
8. regra de parada no primeiro desvio.

Hash sem algoritmo nomeado é ambíguo. Ordenação, normalização de caminho e bytes incluídos devem fazer parte da convenção. Se uma evidência histórica usar outro algoritmo, preservar os dois valores e produzir manifesto de equivalência antes de pedir nova autorização.

## Sequência de corte

1. Validar candidata, inventário, permissões, ausência de symlink, bytecode e segredo.
2. Recalcular os hashes pelo algoritmo canônico no staging e imediatamente antes do corte.
3. Adquirir lock exclusivo para impedir implantação concorrente.
4. Criar e verificar backup integral da árvore ativa.
5. Executar troca atômica no mesmo filesystem, preferencialmente com `renameat2(RENAME_EXCHANGE)`.
6. Rodar todos os validators pós-corte sem reiniciar ou aplicar outra mudança na mesma janela.
7. Se qualquer gate falhar, trocar as árvores novamente e validar a restauração do hash anterior.
8. Preservar a candidata retirada, o backup e as evidências até o encerramento formal.

Sem suporte real à troca atômica, parar. Não usar overlay ou sequência de dois renames como fallback silencioso.

## Evidência e recibo

- Registrar eventos append-only com timestamp UTC, correlation ID, ator, plano, hashes antes/depois, validators, resultado e caminho de rollback.
- Encadear eventos por SHA-256 ou mecanismo equivalente para tornar adulteração detectável.
- Ancorar o hash terminal da evidência em um recibo final.
- Lifecycle administrativo e estado real da árvore são dimensões diferentes. Se a ponte nativa não existir, registrar `cut complete, lifecycle pending` sem fingir que a proposta foi aplicada pelo mecanismo administrativo.
- Nunca registrar token, senha, certificado ou segredo no recibo.

## Critério de pronto

O deploy termina somente quando a árvore ativa tem o hash planejado, todos os validators passam, o backup reproduz o hash anterior, o rollback foi comprovado ou permanece executável, a evidência append-only fecha e o lifecycle administrativo está reconciliado ou explicitamente pendente.

## Relações

- [[01-DIARIO/2026/2026-07-20|2026-07-20]]
- [[40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao|Validação do runtime pós-migração]]
- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]
- `BRAIN/60-AGENTES/versionados/`

## Registro de reconciliação (2026-07-21)

- Executada checagem de consistência entre proposta e ativo da Instagram Brand Director.
- Resultado: proposta `instagram-brand-director-20260720` permanece em `pending` e **não** se encontra ativa;
- ativo do workspace segue com hash `ed9fa5704025e7d91b3d171abdb6cc6c6ecd664cbcc41ba5774128cd3f4e68cd` (39 arquivos);
- candidato/histórico do ciclo está com hash `d2c1a74768ed37e6666ac62a14329992ccce393d994c0bf4700443e225165226`.
- Em consequência, reconciliação administrativamente continua em aberto: não houve correlação automática nem atualização de snapshot nesta janela.

## Complementos reconciliados — lote 7 de 2026-09-21

No incidente de propagação, o validador serializou JSON com ensure_ascii=True, enquanto o contrato exigia UTF-8 canônico equivalente ao jq -cS; os hashes divergiram. Identidade depende dos bytes da canonicalização acordada, não somente equivalência de objeto. Testar acentos/Unicode e comparar resultado entre produtor e consumidor antes de usar hash como binding; correção não permite reutilizar ordem terminal nem consumir aprovação falha. Fonte: unidades 34125.

Quando aprovação usa SHA-256 de JSON, congele a serialização exata: ensure_ascii=true e JSON UTF-8/jq compacto podem representar os mesmos valores e produzir hashes distintos. Comparação semântica não substitui identidade de bytes exigida pelo gate; corrigir o contrato antes de consumir autorização, sem forçar um hash discrepante. Fonte: unidades 34124.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 8 de 2026-09-21

Em validação read-only de pacote congelado, um .pyc extra altera o inventário e pode resultar da própria inspeção. Não importar ou compilar o pacote para inspecioná-lo sem controlar escrita de bytecode. Uma comparação com exclusão lógica explícita ajuda a diagnosticar, mas não apaga o arquivo, não aprova o pacote contaminado e não substitui a identidade congelada original. Fonte: unidades 8622.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch8-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 12 de 2026-09-21

Na revisãoEP02A, run1/run2 idênticos, contagens e hashes corretos não bastaram: semanticHash usava wrapperkind/version/envelope enquanto a revisão doADR então congelada descrevia preimagemdireta. Conferir preimagem contra a versão autoritativa exata; revisão normativa posterior pode mudar a regra. Não perpetuar “semwrapper” como verdade universal. AssinaturasFIM duplicadas exigiam justificar distinçãoatômica ou corrigirfixtures; maislinhas não significam cobertura maior. Fonte: unidades 9750.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch12-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 15 de 2026-09-21

No EP-02 de 29/07, FIM-0095/0104 materializavam JSON null como Python None; assertIsNotNone confundia valor válido de fixture com falha de materialização. Separadamente, FIM-0038 era defeito real: thaw transformava tuple em lista antes de validar o domínio JSON e a entrada proibida passava. Validar tipos originais antes de normalização e usar sentinela distinta para ausência de materialização. Categoria primária de erro também precisa respeitar a precedência normativa, não apenas rejeitar. A rodada posterior mostrou os três casos rejeitados conforme contrato e 23 testes passando; não perpetuar falha histórica como estado atual. Fonte: unidades 8859.

Na revisão EP-02A de 28/07, nove arquivos run1/run2 eram byte idênticos, com contagens e hashes consistentes, mas CTM-017 declarava expected_idempotency_key_match=false em contradição com a evidência de CTM-016/018. O gate falhou: determinismo reproduz também uma expectativa errada. A correção mínima proposta era true ou uma fixture diferente que realmente alterasse a chave, preservando a semântica normativa. FIM LEFT/RIGHT e semantic_commitment já haviam sido corrigidos nessa rodada; não reabrir todos os defeitos anteriores como simultaneamente ativos. A aprovação posterior do pacote é etapa distinta e não torna o FAIL intermediário inexistente. Fonte: unidades 9759.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 16 de 2026-09-21

Na homologação EDC v1.1.0 corrigida, ZIP e hashes individuais foram conferidos e 21 testes passaram; o valor corrected_baseline_hash concordava nos relatórios, mas seu método de agregação não estava documentado. Concordância entre declarações não equivale a recomputação independente do agregado. Registrar precisamente qual identidade foi calculada, qual foi apenas conferida entre fontes e a regra de serialização/inventário necessária para reproduzir o agregado. Isso não desfaz o PASS limitado nem ativa o pacote homologado. Fonte: unidades 8826.

Nos clean roots iniciais do BCA em 29/07, inventários e result.json eram iguais entre runs, mas operational.txt e ep02.txt tinham hashes diferentes, sem causa reconciliada naquele resumo. Delimitar a afirmação de determinismo aos artefatos efetivamente comparados; não declarar o pacote inteiro byte idêntico nem atribuir diferenças a timestamps sem examinar. A invocação inicial de unittest falhou por PYTHONPATH e a corrigida passou; isso distingue erro de invocador de regressão do contrato. O schema consolidado e readiness do BCA permaneceram documentais, com evolução posterior própria. Fonte: unidades 8892.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch16-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 26 de 2026-09-21

No pacote histórico DRE/Prov213 de 02/08, a reconciliação confirmou duas cópias idênticas do relatório e substituiu um hash transcrito não verificado. A autoridade foi separada em âncora machine-readable primária e bloqueante, relatório humano supporting e contexto append-only/mutável. Divergência apenas do relatório não deveria bloquear preflight se o contrato dizia que ele não era âncora; divergência da âncora primária, sim. Hash de arquivo de sessão ainda vivo não era gate permanente. Inspeção de sintaxe, modos, serialização e freeze não significava preflight real executado, e wrapper one-shot não autorizava retry automático. Preservar a função semântica do hash, além dos bytes. Fonte: unidades 8605.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch26-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
