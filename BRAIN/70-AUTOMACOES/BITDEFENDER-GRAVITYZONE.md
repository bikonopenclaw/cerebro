---
id: brain-7a6103874c8018f1606c
type: state
title: Bitdefender GravityZone - integração Bikon
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T21:59:38.438442Z'
relationships:
- type: references
  target: BRAIN/20-EMPRESAS/BIKON/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md#relações
---

# Bitdefender GravityZone - integração Bikon

```yaml
categoria: automacao_seguranca
fonte: conversa com Hebert em 2026-06-18/19, documentação pública Bitdefender consultada na sessão, relatório executivo gerado em 2026-06-19 e relatórios operacionais read-only até 2026-08-12
confiabilidade: media
ultima_revisao: 2026-08-13
tags: [bikon, bitdefender, gravityzone, seguranca, inventario, endpoints, relatorios, ninjaone, tickets]
```

## Finalidade

Registrar o desenho inicial para integração da Bikon com a Public API do Bitdefender GravityZone, visando inventário, saúde de endpoints, incidentes e relatórios por cliente.

## Escopo inicial recomendado

- Inventário de empresas/clientes no GravityZone.
- Lista de endpoints por cliente.
- Status do agente Bitdefender.
- Identificação de máquinas sem proteção, offline ou com problema.
- Consulta de incidentes/detecções recentes.
- Relatório mensal por cliente.
- Alertas operacionais internos.

## APIs/permissões sugeridas

Fase inicial:

- `Network API`: clientes, grupos, endpoints e status.
- `Reports API`: geração/consulta de relatórios.
- `Incidents API`: alertas e incidentes de segurança.

Fase posterior:

- `Event Push Service API`: eventos em tempo real via webhook HTTPS.
- `Quarantine API`: consulta de quarentena, se houver necessidade operacional.

## Autenticação e segredos

- GravityZone usa API Key pelo Control Center e chamadas JSON-RPC 2.0.
- A API key deve ser exclusiva para integração, com permissão mínima necessária.
- A chave aparece uma vez só no painel; deve ser copiada e armazenada com cuidado.
- Não registrar API key no Brain, Telegram, Git ou arquivos versionados.
- Sugestão de cofre local fora do repositório: `/data/.openclaw/secrets/bitdefender-gravityzone.env`.

## Guardrails

- Não executar chamadas reais sem autorização explícita do Hebert.
- Não solicitar ou receber chave de API por Telegram.
- Não commitar arquivos `.env`, tokens, respostas sensíveis ou inventário detalhado de clientes/endpoints.
- Começar por teste controlado de autenticação e leitura, sem alteração de políticas, pacotes ou configurações.
- Ações de remediação, alteração de política, isolamento ou quarentena exigem aprovação explícita e registro operacional.
- Tickets NinjaOne podem ser criados apenas para critérios aprovados; não abrir ticket para máquina inativa, validação manual sem data ou item sem evidência acionável.
- Auto-fechamento só pode ocorrer quando nova coleta confirmar resolução; sem remediação automática no Bitdefender.

## Relatório executivo 2026-06-19

Artefatos gerados no workspace do Kowalski:

- Markdown: `/data/.openclaw/workspace-kowalski/relatorios/bitdefender/relatorio-executivo-licencas-bitdefender-2026-06-19.md`
- PDF: `/data/.openclaw/workspace-kowalski/relatorios/bitdefender/relatorio-executivo-licencas-bitdefender-2026-06-19.pdf`

Resumo agregado:

- 21 clientes.
- 785 licenças.
- 651 slots usados.
- 759 dispositivos.
- 647 dispositivos gerenciados.
- 112 dispositivos não gerenciados.

Observação: manter apenas métricas agregadas no Brain; não registrar API keys, respostas sensíveis ou inventário detalhado de clientes/endpoints.


## Relatório diário de ameaças 2026-07-02

Resumo observado na rotina diária:

- 0 ameaças detectadas.
- 0 itens em quarentena.
- 0 pendências humanas reportadas.

Observação: manter no Brain apenas agregados executivos; não versionar respostas brutas, inventário detalhado ou credenciais.

## Relatório diário de ameaças 2026-07-06

Resumo observado na rotina diária:

- 2 detecções/ameaças ativas encontradas na leitura.
- 2 endpoints afetados: `NOTE-271 | 11 - Unus` e `SCFR01 | 16 - Cartório Ferreira Rocha`.
- 0 bloqueios/quarentenas confirmados pela API para os itens retornados.
- 54 endpoints vistos em 30 dias com assinatura/produto desatualizado.

Próxima ação: revisar os endpoints com `malwareStatus` positivo diretamente no console GravityZone antes de qualquer remediação, isolamento, alteração de política ou comunicação externa.

Observação: manter apenas agregados e nomes operacionais necessários; não versionar respostas brutas, API keys ou inventário detalhado.

## Bitdefender -> tickets NinjaOne, 2026-07-13

Evolução aprovada para Fase 1:

- Dry-run inicial classificou 191 itens acionáveis, mas a validação separou alta confiança de ruído provável.
- Critério ajustado: `endpoint_sem_protecao` só conta se o endpoint foi visto há menos de 30 dias; endpoints mais antigos são tratados como inativos, sem ticket.
- Produção autorizada apenas para 39 itens de alta confiança após validação.
- Itens sem data ou que exigem validação manual permanecem fora da automação de tickets.
- Cron de produção foi aprovado com auto-fechamento quando uma nova coleta confirmar resolução.
- Travas mantidas: sem remediação no Bitdefender, sem alteração de política, sem comunicação externa e sem ticket para máquina inativa.

Estado operacional: Kowalski é responsável por preparar/operar o fluxo Bitdefender -> Ninja dentro dos critérios acima; Puppet Master mantém governança sobre autorização, escala e mudanças de escopo.

## Relatório diário de ameaças 2026-08-07

Resumo agregado observado na rotina diária read-only:

- 2 registros confirmados no dia, ambos como novas entradas em quarentena, sem incidentes.
- 2 endpoints afetados: `NOTE-168 | 11 - Unus` e `11-000303 | 11 - Unus`, ambos `Atc4.Detection`.
- Estado atual indicou 2 endpoints com `malwareStatus` positivo: `SCFR01 | 16 - Cartório Ferreira Rocha` e `11-000303 | 11 - Unus`.
- Janela de licenciamento de 30 dias: 448 dispositivos vistos, 416 licenciados, 22 explicitamente sem licença, 10 sem confirmação técnica e 60 com produto/assinatura desatualizado.
- Coleta concluída sem falhas nas consultas previstas.

Próxima ação: validar no GravityZone os endpoints com `malwareStatus` positivo e confirmar se há remediação pendente antes de qualquer remediação, alteração de política, isolamento, ticket manual ou comunicação externa.

Observação: manter apenas agregados e identificadores operacionais mínimos; não versionar resposta bruta, API keys ou inventário detalhado.

## Relatorio diario de ameacas 2026-08-12

Resumo agregado observado na rotina diaria read-only referente a 2026-08-11 BRT:

- 3 registros confirmados no dia, todos novas entradas em quarentena, sem incidentes.
- 3 endpoints afetados no Grupo Unus: `NOTE-168`, `PC-02` e `11-000303`, todos `Atc4.Detection`.
- Estado atual indicou 2 endpoints com `malwareStatus` positivo: `SCFR01 | 16 - Cartorio Ferreira Rocha` e `11-000303 | 11 - Unus`.
- Janela de licenciamento de 30 dias: 447 dispositivos vistos, 416 licenciados, 21 explicitamente sem licenca, 10 sem confirmacao tecnica e 63 com produto/assinatura desatualizado.
- Coleta concluiu sem falhas nas consultas previstas.

Proxima acao: validar no GravityZone os endpoints com `malwareStatus` positivo e confirmar remediacao pendente antes de qualquer isolamento, alteracao de politica, remediacao, ticket manual ou comunicacao externa.

Observacao: manter apenas agregados e identificadores operacionais minimos; nao versionar resposta bruta, API keys ou inventario detalhado.

## Relações

- Empresa: [[20-EMPRESAS/BIKON/README|BIKON]]
- Diretriz operacional: [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]
- Separação teste/produção: [[40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas|Separar teste, rascunho e produção em automações externas]]

## Complementos reconciliados — lote 7 de 2026-09-21

No snapshot de06/07, a consulta não disponibilizou endpoint de quarentena e apresentou zero confirmados entre itens retornados. Isso não prova zero quarentenas no universo. Informar indisponível/não verificado quando falta a fonte; se usar contagem parcial, dar denominador e cobertura. Licenças, endpoints vistos30dias, inventário total e slots do contrato são medidas distintas; não somar universos ou fechar percentuais por compensação. Fonte: unidades 32397.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 9 de 2026-09-21

Em13/07, a proposta bitdefender-ticket-operacional foi confirmada applied por inspect/list e diretório ativo após timeout anterior; pending era estado intermediário superado. A V1 humana definia Ninja com prioridade e fila padrão, assunto/cliente/evidência/impacto/urgência/ação; cotações e segredos ficavam fora. Esse histórico não amplia critérios automáticos posteriormente restringidos a evidência recente e acionável, nem comprova versão instalada atual. Fonte: unidades 8556.

No incidente18/07, GravityZone respondia mas NinjaOAuth falhava. Um precheck state_hash divergente veio de constante transcrita errada no invocador, não corrupção comprovada do arquivo. Comparar fonte e constante antes de remover guarda de integridade. Após única trocaOAuth autorizada retornar invalid_token, não houve token novo persistido nemGETorganizations; exigir fluxo fresco e persistência atômica somente após resposta completa, sem repetir código usado ou atribuir indisponibilidade ao provider errado. É lição histórica, não status atual. Fonte: unidades 8745.

Desenho histórico para tickets Bitdefender→Ninja separava coleta/relatório read-only da ação externa: alertas acionáveis, mapeamento de cliente comprovado e chave de deduplicação por cliente/endpoint/tipo/identificador. Fase inicial propunha abrir/deduplicar; fechamento automático seria fase posterior, condicionado à resolução comprovada em duas coletas. Dry-runs, horário proposto e número de ciclos não comprovam que automação foi implantada. Fonte: unidades 35308.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch9-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 13 de 2026-09-21

Em 18/07/2026, após a tentativa invalid_token, novo fluxo fresco de OAuth NinjaOne terminou em um exchange HTTP 200, token validado/persistido com modo 600 e GET /v2/organizations HTTP 200 para 34 organizações. GravityZone já respondia para 21 empresas. O teste de produção/ticket não havia sido realizado nessa etapa; autorização posterior de um ticket interno exigia dry-run limpo e rota segura existente, sem fechar ticket nem criar clientes reais. Preservar endpoint do tenant e scopes efetivamente vinculados ao contrato vigente; esse sucesso histórico não atesta token válido hoje. Não arquivar códigos, tokens ou hashes de arquivos de segredo como memória cognitiva. Fonte: unidades 8748.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch13-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 14 de 2026-09-21

Em 13/07, create bitdefender-ticket-operacional terminada em 892185b0a0 foi confirmada applied, mas o update distinto terminado em 80074a5213 continuava pending naquele snapshot. Status não se transfere entre IDs ou workspaces; inspect not found em um escopo não prova inexistência global. Regra humana de V1 mantinha fila/prioridade padrão e permitia elevar prioridade somente por ameaça ativa, usuário parado ou cliente sem proteção. Skill/proposta aplicada não comprova cron de abertura automática; separar contrato manual, automação real e critérios atuais. A evolução posterior da rotina prevalece sobre esses estados históricos. Fonte: unidades 8559.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch14-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complemento de cobertura de metadados — 2026-09-21

No resumo histórico de junho/2026 preservado em um backup de sessions.json, os 587 dispositivos com licença confirmada no detalhe eram uma métrica distinta de 647 dispositivos gerenciados e 651 slots usados; esses denominadores não deviam ser intercambiados. A descoberta daquela integração usava network/getCompaniesList, network/getEndpointsList por parentId, detalhe somente para endpoints gerenciados e licensing/getLicenseInfo por companyId, omitindo licenseKey. Esses contratos eram referências observadas naquela versão, não validação da API atual nem autorização de coleta direta por Kowalski: a rota posterior delega a fonte ao Sentinel. O mesmo resumo preservava o caso Capixaba de22/06 já consolidado em Kowalski: inventário e eventos auditáveis não autorizavam inventar histórico granular, e a norma não foi tratada como obrigação direta de trocar computadores. Contadores intermediários de máquinas, fases de substituição e paths de entrega eram checkpoints históricos; não são inventário atual nem nova autorização de contato. Fonte: unidade9103.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-metadata-summary-9103-20260921.json`.
