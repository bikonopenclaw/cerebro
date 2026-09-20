# Validacao tecnica nao substitui aceite humano

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W33; consolidacao semanal 2026-W37; lote 365 Control em 2026-09-14; consolidacao semanal 2026-W38
confiabilidade: alta
ultima_revisao: 2026-09-20
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

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Commit-de-estado-nao-e-aceitacao-operacional|Commit de estado nao e aceitacao operacional]]
- [[40-CONHECIMENTO/Operacional/Contagem-nao-e-percentual-de-conclusao|Contagem nao e percentual de conclusao]]
- [[01-DIARIO/Semanal/2026-W33|Semana 2026-W33]]
- [[01-DIARIO/Semanal/2026-W37|Semana 2026-W37]]
