---
id: brain-43f6df5f2e3dc092a33a
type: knowledge
title: Validacao tecnica nao substitui aceite humano
created: '2026-09-21T19:35:12.394147Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Validacao-visual-de-relatorios-externos.md
  reason: O caso comercial distingue premissas da oferta, parecer visual e aceite humano.
  source: BRAIN/99-SISTEMA/brain-v2/reports/coverage-2026-09-26-daily.json#K2-K215
- type: derived_from
  target: BRAIN/01-DIARIO/Semanal/2026-W39.md
  reason: A semana reforça que uma correção humana não valida dimensões não testadas.
  source: BRAIN/99-SISTEMA/brain-v2/reports/coverage-2026-09-27-weekly.json#daily-25-26
updated: '2026-10-04T06:00:00Z'
---

# Validacao tecnica nao substitui aceite humano

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W33; consolidacao semanal 2026-W37; lote 365 Control em 2026-09-14; consolidacao semanal 2026-W38
confiabilidade: alta
ultima_revisao: 2026-10-04
tags: [aceite, validacao, fail-closed, provimento-213, fip, kowalski, versao, artefato, entrega]
```

## Principio

Teste automatizado, hash, manifesto, rota `200`, Kowalski `PASS` ou suite completa provam somente a dimensao tecnica que foi exercitada. Quando o gate definido e visual, humano, semantico, financeiro ou de verdade canonica, a aceitacao continua bloqueada ate a evidencia propria desse gate existir.

Validacao tecnica reduz risco, mas nao muda o criterio de aceite.

## Aplicacao pratica

- Declarar qual dimensao cada gate valida: tecnica, visual, semantica, financeira, canonica ou humana.
- Manter `FAIL_CLOSED` quando a suite passa, mas o gate humano/visual ainda nao foi executado.
- Separar "pronto tecnicamente" de "aceito operacionalmente".
- Registrar quem ou qual evidencia autoriza a promocao final.
- Nao substituir reteste em dispositivo real, revisao de PDF, reconciliacao de corpus ou aceite de Project Owner por resumo tecnico.
- Vincular o parecer ao hash/versao revisado. Mudanca de copy, composicao, acabamento ou bytes invalida a heranca de aceite e exige nova revisao no gate aplicavel.
- Distinguir aceite do transporte de aceite humano: upload concluido, ACK do gateway ou entrega Telegram nao comprovam visualizacao, aprovacao artistica nem autoridade de publicacao.
- Preservar a superficie exata de cada QA: validacao de MP4 integral pelo produtor nao amplia um parecer do revisor sobre frames/capa, e revisao visual nao prova encode, audio, duracao ou sincronismo que nao foram exercitados.
- Separar validade do produto, suficiencia factual e aceite de negocio. Um PDF bem formado e visualmente aprovado ainda pode falhar ao objetivo se a fonte nao provar o periodo, a populacao ou a pergunta do proprietario.

## Exemplo conectado

Na semana 2026-W33, o Mini App e a composicao visual do Provimento 213 passaram em testes, rotas, Kowalski e pureza read-only, mas permaneceram bloqueados ate reteste real do iPhone do Project Owner. O PDF Alzira tambem exigiu aceite semantico apos corrigir o falso `100%`.

Na semana 2026-W37, os rascunhos A/B da Bikon foram revisados e entregues sem aceite humano, o canario R3 permaneceu `REQUIRES_CHANGES` e a opcao C V6 do 365 Control nao herdou o parecer tecnico da V3. Cada versao conservou seu proprio estado e nenhuma recebeu autoridade de publicacao por inferencia.

Em 2026-09-14, carrossel e Reel 365 Control chegaram a `APPROVED_FOR_TECHNICAL_DELIVERY` e foram entregues privadamente, mas permaneceram com `approval=null`, `publication=null` e `publication_authority=false`. No Reel, Robotnik validou o MP4 integral enquanto Kowalski cobriu apenas o pacote visual; as duas evidencias foram mantidas separadas.

Em 2026-W38, o primeiro PDF ARX do cliente 2111 passou pipeline e QA, mas foi rejeitado porque a fonte nao comprovava os backups realizados. O predecessor preservou o sucesso tecnico e o aceite negativo; nova apresentacao ou nova coleta nao poderia apagar nenhum desses fatos.

## Reconciliação de escopo do aceite — semana 2026-W39

O caso Business Gestão de 24/09, consolidado no [[01-DIARIO/2026/2026-09-26|diário de 26/09]], acrescenta um limite comercial ao padrão: PASS técnico/visual declarado não comprova quantidade atual, composição do pacote, preço, suporte ou SLA. Corrigir a oferta exige reconciliar as premissas fornecidas pelo proprietário e a versão do documento; não basta melhorar o acabamento. O caso permanece detalhado em [[40-CONHECIMENTO/Operacional/Validacao-visual-de-relatorios-externos|validação visual e premissas comerciais]], sem transformar condições de um cliente em política geral nem atestar aceite final.

O inverso também importa: a confirmação humana de que o grupo voltou a responder, registrada em [[01-DIARIO/2026/2026-09-25|25/09]], comprova o retorno observado, não homologação financeira, auditoria de canais ou aprovação de outras operações. Parecer técnico e confirmação humana precisam ambos declarar objeto, versão quando aplicável e dimensão efetivamente verificada. Fontes e limites da reconciliação: [[01-DIARIO/Semanal/2026-W39|semana 2026-W39]].

## Observação natural não se encerra apenas pelo relógio — 28/09/2026

O checkpoint de qualificação natural registrou a janela original de 24 horas encerrada, mas `0/3` tarefas naturais elegíveis, exposição insuficiente das propriedades alteradas e `ready_for_review=false`. A lição é separar tempo decorrido, exposição efetiva por propriedade, representatividade da amostra e inspeção do produto. Uma extensão passiva da observação não é aprovação; tarefas artificiais ou repetição de efeitos não preenchem legitimamente uma quota de uso natural.

Fonte: chamadas de checkpoint e espera da sessão main `ca07a16c-ab62-48e4-8bd5-9e06138d0e31`, linhas 16 e 18, em 28/09. Este registro preserva o estado declarado naquele corte, sem verificar novamente o observador nem antecipar o resultado de uma revisão posterior. Identidades e limites no recibo `BRAIN/99-SISTEMA/brain-v2/reports/coverage-2026-09-29-daily.json`.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Commit-de-estado-nao-e-aceitacao-operacional|Commit de estado nao e aceitacao operacional]]
- [[40-CONHECIMENTO/Operacional/Contagem-nao-e-percentual-de-conclusao|Contagem nao e percentual de conclusao]]
- [[01-DIARIO/Semanal/2026-W33|Semana 2026-W33]]
- [[01-DIARIO/Semanal/2026-W37|Semana 2026-W37]]

## Complementos reconciliados — lote 9 de 2026-09-21

No dashboard Prov213 multi-CNS, PASS local foi reaberto: Tailscale removia prefixo /prov213, então rotas gerais davam404 externamente embora individuais funcionassem; o renderer tratava objetos ICDV4 como strings. Adaptar view model e validar HTTPS real, GET repetido sem mutação e hashes antes/depois. Teste de traversal com cliente normalizando ../ não demonstra bloqueio: enviar caminho literal. Fila aceita de validação não é PASS; aguardar retorno independente do mesmo artefato. Fonte: unidades 33186.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch9-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 15 de 2026-09-21

Em 08/08, após a revisão que detectara escrita por GET, o gate multi-CNS relatou PASS em oito rotas HTTPS reais, export pelo registro do CNS, zero mutações em GET repetido e ausência de Chromium tratada como 503. A igualdade do conteúdo PDF foi avaliada também com normalização de metadados dinâmicos de geração. Declarar se a prova é equivalência semântica normalizada ou identidade exata de bytes; uma não substitui a outra em manifesto selado. PASS staged não basta para o endereço externo, e este gate de exportação não equivale a aceite posterior do Mini App pelo usuário. Fonte: unidades 9591.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 19 de 2026-09-21

Em 17/07/2026, o Chromium fixado produziu PDF com metadados compatíveis, mas o teste visual perdeu logo e deslocou cabeçalho. Depois da adaptação com brand pack, o agente anunciou DOCX/PDF validados; Hebert rejeitou a configuração do DOCX e o timbrado/padrão do PDF e pediu para não continuar naquele momento. Preservar o aceite negativo como desfecho: paginação e metadados corretos não comprovam fidelidade visual entre formatos. Não reabrir a tarefa nem reinstalar a versão antiga por esta memória. Fonte: unidades 36688, 36691.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch19-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 22 de 2026-09-21

No Portal 213 de 21/08, build versionado, HTML loopback/HTTPS idêntico, probes assinados e Chromium renderizado coexistiram com os dois botões reais falhando no Telegram/iOS do usuário. O aceite precisava reabrir e localizar a quebra entre tap, WebView, HTTPS/build, initData e render, sem pedir repetição antes de hipótese/build corrigidos. A afirmação inicial de unit inexistente foi contradita pelo journal do user manager com loop de restart; healthz nomeando serviço também não prova ownership. Registrar restart loop como evidência operacional e hipótese causal naquele checkpoint, sem afirmar causa conclusiva ou estado atual. Fonte: unidades 30217.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch22-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Evidência incremental não transfere aceite — semana 2026-W40

A campanha revisada em 01/10 e o retorno documental incorporado em 03/10 mostram por que cada prova deve declarar **objeto/hash, dimensão, autor e momento**. Hash/extração relatados pelo destinatário acrescentam integridade de transporte; não se tornam inspeção independente do ZIP, aceite criativo ou autorização de publicação. A rejeição anterior continua na cronologia da versão correspondente, sem impor por inferência o mesmo resultado a bytes não examinados.

O mesmo limite aparece nos relatórios e na qualificação natural do diário de 29/09: PASS técnico limitado, ocorrência natural e amostra suficiente respondem a perguntas diferentes. Registrar o gate que falta, em vez de promover evidência de outra dimensão a conclusão geral. Síntese e fontes em [[01-DIARIO/Semanal/2026-W40|W40]]. PGL/Golden e gates de negócio não foram alterados; a revisão foi documental, sem teste ou envio novo.
