---
id: brain-d03ba676ba34b20e7863
type: knowledge
title: Menor privilégio em monitoramento
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:32:09.804705Z'
relationships:
- type: references
  target: BRAIN/60-AGENTES/SENTINEL.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md#relações
- type: references
  target: BRAIN/60-AGENTES/versionados/workspaces/sentinel/access_control/REVOGACAO.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md#relações
---

# Menor privilégio em monitoramento

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W29
confiabilidade: alta
ultima_revisao: 2026-07-17
tags: [monitoramento, menor-privilegio, read-only, allowlist, auditoria, revogacao]
```

## Princípio

Monitorar não exige poder de remediar. Agentes de observabilidade devem receber somente a leitura necessária, por clientes tipados e allowlists verificáveis, com saída sanitizada e revogação testável.

## Requisitos

- Fonte e operação explicitamente autorizadas.
- Cliente read-only sem URL, método, comando ou caminho arbitrário.
- Segredo fora do Brain/Git e permissão local restrita.
- Saída mínima, sem resposta bruta, credencial ou dado pessoal desnecessário.
- Auditoria append-only com ator, fonte, operação, horário UTC, resultado, correlação e hash do cliente.
- Falha de auditoria bloqueia a consulta.
- Revogação no provedor seguida de prova pela mesma rota aprovada.

## Limite de credencial compartilhada

Um wrapper read-only reduz risco operacional, mas não transforma uma credencial ampla em credencial de privilégio mínimo. Quando o provedor permitir, a solução correta é criar identidade exclusiva com escopo somente leitura. Até lá, a limitação deve permanecer documentada e revisada.

## Relações

- [[60-AGENTES/SENTINEL|SENTINEL, Controller de Operações e SNOC]]
- [[60-AGENTES/versionados/workspaces/sentinel/access_control/REVOGACAO|Procedimento de revogacao]]
- [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|Ausência de evidência não é status operacional]]

## Conhecimento recuperado dos históricos — revisão 2026-09-21

Em 01/07/2026, no contexto de dashboard do controle financeiro familiar, Hebert pediu restringir acesso ao IP fixo da empresa. Registrar como requisito de acesso daquele projeto, sujeito a confirmação do endereço e teste efetivo da restrição; a conversa não comprova firewall ou autenticação implementados. Não generalizar o IP observado no servidor como endereço autorizado da empresa. Fonte: unidades 29965.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.

## Complementos reconciliados — lote 5 de 2026-09-21

Na preparação praxis-gws em 18/06/2026, o pacote incluía e-mails/relatórios de outra operação e scopes amplos. A instalação foi relatada sem autenticação nem envio, com revisão do conteúdo e scripts antes de usar. Dependência instalada não concede autoridade operacional; reduzir dados herdados e scopes ao necessário antes de integrar conta real. Fonte: unidades 34663, 34666.

No teste praxis-gws de 18/06/2026, gmail.send permitiu envio, mas consulta de perfil pediu permissão que não estava concedida. O diagnóstico deve distinguir operação fora do scope de falha de autenticação, sem ampliar permissão só para passar um teste. Drive.file e calendar.events foram depois adicionados para funções específicas, com criação/exclusão de objetos de teste; esse registro histórico não comprova scopes atuais nem autoriza novas operações. Fonte: unidades 34684, 34690, 34693, 34696, 34699.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch5-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 7 de 2026-09-21

No desenho de acesso ao painel por terceiro, compartilhar o dispositivo Tailscale e autorizar só o serviço/porta desejado foram considerados controles distintos. Validar alcance efetivo de ACL e autenticação da aplicação; não supor que convite ao nó concede somente o painel. Proposta histórica não comprova ACL aplicada e não autoriza tornar serviço público. Fonte: unidades 39543.

No cliente ARX do Sentinel, status foi limitado a contagens/classificações agregadas e referência de auditoria após append-only bem-sucedido; payload bruto, contas/ativos/settings não deveriam sair do comando agregado. Consulta bem-sucedida com atenção agregada não identifica cliente nem autoriza nova leitura/ticket/remediação. Separar observabilidade sanitizada de acesso detalhado e manter correlação com a coleta autenticada. Fonte: unidades 36765.

No acesso remoto histórico, ativar Tailscale no host não expunha automaticamente serviços presos a loopback. Serve foi relatado como proxy tailnet-only para o dashboard OpenClaw; publicar Claw3D na mesma raiz substituiria esse destino. Exposição de novo serviço precisa de rota/porta e ACL próprias, sem trocar silenciosamente o dashboard existente; tailnet-only não equivale a Internet pública, e endereço antigo não prova serviço atual. Fonte: unidades 37435, 37432, 35440.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
