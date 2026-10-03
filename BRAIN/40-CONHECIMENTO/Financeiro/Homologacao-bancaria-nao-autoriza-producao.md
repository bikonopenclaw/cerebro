---
id: brain-3a02cbeee41af13e0836
type: knowledge
title: Homologação bancária não autoriza produção
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-10-03T02:00:00Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/boletos-malote/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Homologacao-bancaria-nao-autoriza-producao.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Homologacao-bancaria-nao-autoriza-producao.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Homologacao-bancaria-nao-autoriza-producao.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Homologacao-bancaria-nao-autoriza-producao.md#relações
---

# Homologação bancária não autoriza produção

```yaml
categoria: financeiro
tipo: guardrail
fonte: consolidação semanal 2026-W28
confiabilidade: alta
ultima_revisao: 2026-10-03
tags: [cresol, homologacao, boletos, remessa, baixa, producao]
```

## Regra

Homologação técnica, pacote local validado, API funcional ou boleto renderizado corretamente não autorizam uso em produção, upload bancário, baixa financeira ou envio externo.

## Aplicação prática

- Manter produção bloqueada por padrão até autorização explícita.
- Separar criação/consulta de título de teste de operações produtivas.
- Exigir procedimento próprio para baixa por API, com validação, rollback e aprovação.
- Registrar no Brain apenas estado, guardrails e evidência sanitizada; payloads, respostas e PDFs oficiais de homologação ficam fora do Git.
- Antes de upload, validar localmente remessa, totais, sequenciais, contrato, carteira, nosso número e documentação oficial.

## Exemplo conectado

Na semana 2026-W28, a API Cresol avançou em homologação, a remessa CNAB400 local foi validada e o boleto PDF foi conferido, mas nenhum upload no portal, envio bancário, baixa por API ou comunicação externa foi autorizado.

## Checkpoint Cresol — 26/27 de setembro de 2026

As memórias main de 26 e 27/09 registram o broker `cresol-preflight-broker` 0.1.2 instalado no runtime dedicado do Darth Vader e preflight `PASS_METADATA_ONLY`, sem leitura do segredo nem rede nessa etapa. Na tentativa autenticada posterior, OAuth respondeu HTTP 502 / `temporarily_unavailable`, antes das consultas bancárias; o checkpoint de 27/09 registra um POST OAuth nessa tentativa, sem retry automático. Isso não equivale a POST de criação de título, homologação concluída ou acesso produtivo.

A orientação registrada é preservar o pacote e o snapshot, aguardar a resposta oficial da Cresol e retomar do checkpoint, sem reinstalar, fazer rollback ou repetir testes live em loop por mera falha remota. Alterações de contrato, plugin, credencial ou rota continuam dependentes de aprovação explícita. O limite é importante: validação local, visibilidade do segredo por metadados, autenticação remota e operação bancária são provas separadas; indisponibilidade de OAuth não invalida automaticamente a integridade do pacote.

Fontes: `memory/2026-09-26.md` e primeira seção de `memory/2026-09-27.md`, lidas integralmente; hashes/posições no recibo `BRAIN/99-SISTEMA/brain-v2/reports/coverage-2026-09-29-daily.json`. São checkpoints documentados, não revalidação do runtime ou do provedor nesta consolidação. Evidência técnica referenciada, não auditada aqui: `artifacts/cresol-api-homologation-isolated-20260923/CRESOL_OAUTH_PROVIDER_RESPONSE_CHECKPOINT_20260926T2142Z.json`.

## Reteste solicitado em 01/10/2026 — bloqueio antes da API

Hebert solicitou novo teste de comunicação no grupo Faturamento Bikon. Isso acrescenta autorização pontual ao histórico de espera pela Cresol; não autoriza produção, operação financeira, mudança de credencial/rota ou reparo do runtime. A nova solicitação não transforma o HTTP 502 de setembro em resultado atual.

A execução curta do Darth Vader às 23:56 UTC informou que o catálogo expunha somente `cresol_secret_preflight`, para metadados locais do SecretRef, não uma ferramenta de teste de rede/autenticação. A ferramenta não foi executada nessa rodada por não cumprir o pedido. Plugin carregado e preflight local não comprovam conectividade, autenticação ou homologação.

O checkpoint do pai, já em 02/10 às 00:03 UTC (01/10 BRT), registrou três interrupções por `gateway_draining`, inclusive depois de `health.ok`, e reconciliou a última tentativa como leitura de duas skills antes de qualquer chamada Cresol. **Comunicação e autenticação continuavam não testadas**, sem resultado bancário novo; o bloqueio documentado é interno, não uma falha atual atribuída ao banco. A descoberta curta concluída não comprova capacidade de concluir o teste com ferramentas.

O pedido foi mantido pendente pelo mesmo responsável, com novas tentativas suspensas e próxima revisão registrada para 02/10 às 08h BRT. Este registro não agenda nem executa essa revisão. Retomar depende de evidência de resolução e reconciliação dos efeitos anteriores; autorização para testar API não autoriza reiniciar ou alterar serviços.

Fontes: sessão do grupo `056cb7b4-ab96-44b7-ab51-80559a8a32a4`, pedido linha 5 e checkpoints selecionados; sessão Darth dedicada `3b82ce3d-7ed3-43a0-bde2-2edf1571d306`, resposta linha 5. Hashes, posições e disposições em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-2026-10-02-daily.json`. Checkpoints são relatos persistidos revisados, não revalidação do executor ou da API nesta consolidação. Relaciona-se ao limite de [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|diagnóstico por etapa]].

## Relações

- [[70-AUTOMACOES/boletos-malote/README|Boletos e malote bancário]]
- [[40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa|Retorno bancário não valida remessa]]
- [[40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas|Separar teste, rascunho e produção em automações externas]]
- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]

## Complementos reconciliados — lote 10 de 2026-09-21

No teste Cresol histórico, HTTP400 informou Nosso Número já cadastrado antes da obtenção do boleto oficial. Uma colisão exige consultar estado remoto e identificar o título correspondente; não reutilizar ou avançar sequência cegamente. Recibo local/PDF e remessa preparada não comprovam importação ou aceite bancário; homologação permanece separada de produção. Fonte: unidades 3424.

Proposta histórica FBCP: integrar Cresol por adapter atrás do controlador, registrando intenção, autorização, identidade e idempotência. PDF oficial pode existir antes de aceite final e estado remoto pode continuar em processamento. Antes de repetir POST, reconciliar ledger local, referência externa, Nosso Número e estado remoto. CNAB não seria removido por um teste API; mudança de caminho exige provar consulta/ocorrências, rejeição e recuperação, mantendo homologação separada de produção. Fonte: unidades 31588.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Cancelamento posterior do reteste — 02/10/2026

Hebert pediu explicitamente encerrar a tarefa da API Cresol. A fonte registra fechamento do objetivo `CRESOL-API-COMM-RETEST-20261001T233345Z`; a inspeção terminal retornou `COMPLETED`, `next_checkin_at_ms=null`, quatro operações no histórico e nenhuma dependência ativa. Trata-se de **cancelamento do teste solicitado**, não homologação bem-sucedida nem prova de comunicação/autenticação. A espera/revisão descrita na seção de 01/10 passou a ser histórica e não é autorização de retomada.

Fonte: sessão main `a7273403-8c6d-4d1c-8cbc-4bcbba62c37c`, pedido linha 4, narrativas linhas 5/32 e resultado terminal linha 31; hashes no recibo `BRAIN/99-SISTEMA/brain-v2/reports/coverage-2026-10-03-daily.json`. A diária não chamou o banco ou o controlador.

Rastreabilidade: o recibo diário de 02/10 citado na seção anterior não foi localizado no HEAD `f399037` nem na árvore examinada em 03/10. O texto anterior está versionado, mas a referência prevista não prova cobertura por fonte; a lacuna fica preservada no recibo atual, sem inventar fechamento retroativo.
