# Bikon Durable Work Orchestration

```yaml
categoria: automacao_operacional
fonte: contrato canonico e requests duraveis observados em 2026-09-16/19
confiabilidade: alta
ultima_revisao: 2026-09-19
tags: [bikon, durable-work, relatorios, documentos, sentinel, kowalski, lifecycle, idempotencia]
```

## Finalidade

Preservar pedidos assíncronos de relatórios e documentos além do turno conversacional, com admissão, handoff, execução, evidência, artefato, QA, recuperação e entrega registrados sob uma única identidade durável.

## Contrato operacional

- Puppet Master é owner do pedido; Sentinel coleta; Kowalski analisa, produz, renderiza e faz QA visual.
- A autoridade de negócio é o SQLite canônico de requests e o controller existente. Não criar ledger paralelo nem despachar fases duráveis diretamente por `sessions_send` ou `sessions_spawn`.
- Somente receipt com `WORK_DURABLY_ADMITTED=true`, `request_id` estável e `durably_admitted_at` permite alegar que o trabalho foi aceito.
- ACK, runId, fila de sessão ou mensagem aceita não comprovam por si só admissão, progresso de negócio nem conclusão.
- Status é observacional; não admite, redespacha, aprova, troca executor nem cria sucessor.
- Handoff, input hash, runtime/gateway aceito, artefatos e terminalidade são persistidos antes de avançar.
- Recovery reaproveita outputs comprometidos e faz retries causais limitados na mesma identidade; não usa replay cego.
- Rework preserva bytes e QA históricos do predecessor e admite no máximo um sucessor autenticado.
- Falha depois de `ACK_DURABLE` nao autoriza repetir o mesmo input. Recuperacao exige causa identificada e mudanca autenticada de codigo, contrato, evidencia ou autoridade, preservando barreiras e tentativas anteriores.
- Revisoes de apresentacao permanecem na mesma request, com artefatos imutaveis por versao, single-writer, hash proprio e entrega idempotente; nao refazem coleta nem alteram a verdade de negocio.

## Regras de relatório

- `ARTIFACT_TECHNICAL_QA` não substitui `BUSINESS_SEMANTIC_ACCEPTANCE`.
- Empty history não prova zero execuções; artefato de disponibilidade não satisfaz intenção de performance de backup.
- Pedido explícito por “dados disponíveis” ativa `AVAILABLE_AUTHENTICATED_DATA_V1` somente para aquela request: usar observações autenticadas com datas reais e limitações declaradas, sem exigir que a falta de cobertura vire falha ou zero atividade.
- Entrega ao proprietário privado exige reconhecimento do transporte. Cliente, grupo ou outra rota externa nunca são inferidos.
- Resultado ambíguo de envio bloqueia resend cego.

## Evidência observada

- O pedido documental Bruna Reffatti terminou `COMPLETED`: dois PDFs comprometidos, QA textual/visual `PASS` e retorno interno pronto.
- Requests ARX para Alfredo Chaves, Cartório Capixaba, Cartório Camburi e Cartório Vila Velha terminaram `SUCCESS`, com PDF autenticado, QA `PASS`, delivery `ACKNOWLEDGED`, `customer_delivery=false` e `provider_mutation=false`.
- A request de Alfredo Chaves usou `31` sessões autenticadas retidas com cobertura parcial explicitada. Capixaba e Camburi usaram `190` registros autenticados cada; Vila Velha usou `134` registros, incluindo `122` execuções, `121` sucessos, `1` com erro e `12` skips. Esses números permanecem vinculados às datas/cobertura dos recibos e não devem ser generalizados para o mês inteiro.
- A request Alzira posterior usou `192` execucoes autenticadas (`191` sucessos e `1` falha), terminou `SUCCESS` e teve entrega privada reconhecida apos uma recuperacao causal de QA visual.
- A request Capixaba posterior preservou `190` execucoes com sucesso no recorte e chegou a uma apresentacao revisada por cinco recuperacoes causais limitadas. Versoes/recibos anteriores foram mantidos, provider nao foi reconsultado e o aceite de negocio continuou separado do terminal tecnico.

## Relações

- [[70-AUTOMACOES/ARX-BACKUP-NINJAONE|ARX Backup NinjaOne]]
- [[70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM|Relatorios Operacionais Telegram]]
- [[60-AGENTES/SENTINEL|Sentinel]]
- [[60-AGENTES/KOWALSKI|Kowalski]]
- [[40-CONHECIMENTO/Operacional/Estado-terminal-requer-convergencia-do-lifecycle|Estado terminal requer convergencia do lifecycle]]
