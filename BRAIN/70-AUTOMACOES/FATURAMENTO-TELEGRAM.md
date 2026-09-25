---
id: brain-ed9d140a3088aec50c54
type: state
title: Grupos Telegram de faturamento
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-25T02:00:00Z'
relationships:
- type: references
  target: BRAIN/20-EMPRESAS/BIKON/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/boletos-malote/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md#relações
---

# Grupos Telegram de faturamento

```yaml
categoria: automacao_operacional
fonte: sessões Telegram visíveis em 2026-06-17, correções operacionais em 2026-06-18/19/25/26, remoção FN Souza em 2026-06-25 e lote Bikon agosto/2026 em 2026-08-03
confiabilidade: alta
ultima_revisao: 2026-09-25
tags: [telegram, faturamento, bikon, fn-souza, nfse, boletos, remessa, darth-vader]
```

## Finalidade

Registrar os contextos operacionais de grupos Telegram usados para faturamento, evitando mistura de assuntos e preservando regras de segurança fiscal/financeira.

## Grupos ativos

### Faturamento Bikon

- Chat: `telegram:-5561224828`
- Contexto operacional local: `/data/.openclaw/workspace/contextos/telegram--5561224828-faturamento-bikon.md`
- Escopo: apenas faturamento da Bikon Tecnologia.
- Inclui: NFS-e, boletos, remessa/retorno bancário e conferência cadastral ligada diretamente ao faturamento da Bikon.
- Fora de escopo: faturamento de terceiros, comercial geral, marketing/conteúdo, suporte técnico, infraestrutura/site/checkout sem ligação direta com faturamento, financeiro gerencial amplo e conversa operacional aleatória.
- Roteamento: Puppet Master coordena; execução fiscal/financeira deve ser delegada ao Darth Vader quando necessário.
- Configuração operacional observada em 2026-06-25/26: o grupo permitido e o remetente permitido são dimensões separadas. `groupAllowFrom` deve conter o ID do remetente autorizado, não o ID do grupo. Após correção, foi necessário restart limpo do Gateway/Telegram para novo teste.

## Contextos inativos / históricos

### Faturamento FN Souza

- Chat: `telegram:-5435011106`
- Status: inativo desde 2026-06-25.
- Contexto anterior: criação/conferência de NFS-e, boletos e remessas da skill `faturamento-fn-souza`.
- Remoção operacional registrada: grupo removido da configuração do OpenClaw, pasta Google Drive `Faturamento FN Souza` movida para a lixeira e entrada `faturamento_fn_souza` removida do mapa local `contextos/google-drive-faturamento-pastas.json`.
- Snapshot versionado: a skill `faturamento-fn-souza` deixou de aparecer no snapshot seguro da Darth Vader após sincronização de 2026-06-25.
- Regra: não tratar FN Souza como fluxo ativo sem nova autorização explícita e novo escopo operacional.

## Guardrails

- Não emitir NFS-e real sem aprovação explícita do Hebert.
- Não emitir boleto real sem aprovação explícita do Hebert.
- Não gerar remessa de produção sem aprovação explícita do Hebert e validação do layout bancário.
- Não enviar comunicação externa ou arquivo financeiro a cliente sem aprovação explícita.
- Preparos internos, rascunhos, conferências e validações podem ser executados sem impacto externo quando houver dados suficientes.
- Se faltar dado fiscal/financeiro, pedir apenas o mínimo necessário para desbloquear.
- Antes de postar, repostar, acionar agente, alterar configuração ou disparar qualquer execução fora da conversa atual, avisar Hebert e confirmar quando o impacto não estiver previamente autorizado.

## Lote Bikon agosto/2026

Em 2026-08-03, o fluxo de faturamento Bikon operou a remessa 093 em produção assistida:

- NFS-e: `27` emitidas/autorizadas, com PDF/XML locais.
- Boletos: `27` gerados localmente.
- Remessa: `1` CNAB400 local gerada, sem transmissão bancária consolidada.
- E-mails: `18` enviados, agrupados por cliente, com cópia obrigatória para `financeiro@bikon.com.br`.
- Total do lote: R$ 86.357,06.

O caso preserva a regra de etapas: emissão fiscal, boleto/remessa, conferência, envio externo e transmissão bancária não devem virar uma única esteira automática sem gates próprios.

## Relações

- Empresa: [[20-EMPRESAS/BIKON/README|BIKON]]
- Automação fiscal: [[70-AUTOMACOES/NOTAAS-NFSE|Skill Notaas NFS-e]]
- Boletos/malote: [[70-AUTOMACOES/boletos-malote/README|Boletos e malote bancário]]
- Agente executor financeiro: Darth Vader
- Diretriz operacional: [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]

## Conhecimento recuperado dos históricos — revisão 2026-09-21

Histórico de 18/06/2026: as pastas vinculadas aos grupos de faturamento foram definidas como entrada de arquivos das notas a serem faturadas. A presença de um documento nesse espaço é insumo para preparação e conferência, não evidência de emissão concluída ou autorização automática de envio. FN Souza foi depois desativado em 25/06; esta finalidade histórica não reativa seu grupo, pasta ou fluxo. Fonte: unidades 34708.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.


## Incidente de resposta no grupo — 2026-09-24

A revisão do registro fornecido por Hebert mostra entrada de mensagem do grupo às 18:58:24 UTC e falha da mesma lane às 18:59:34 UTC com `CONTEXT_COMPACTION_FAILED`, seguida de despacho sem resposta enfileirada. A indisponibilidade estava demonstrada no processamento do contexto, não na entrega do Telegram. As hipóteses anteriores de privacidade, allowlist ou ausência de ingestão foram superadas por essa evidência; não devem ser reutilizadas como diagnóstico vigente.

O histórico relata teste temporário de `ingest=true` e rollback, sem resolução por esse caminho. Após a orientação de reset limitado à sessão do grupo, Hebert informou que voltou a responder. Essa confirmação humana sustenta a recuperação observada, mas não representa validação integral da configuração, de todos os canais ou do fluxo fiscal/financeiro. Não houve reexecução deste incidente na consolidação.

Aprendizado conectado: [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|ausência de resposta não prova ausência de entrada]]. Conferir ingresso, processamento e saída separadamente antes de atribuir causa ou propor mudanças de permissão.

Fontes: sessão main `ac87bb64-7ef3-4bfc-bae6-7a2ee976e8d0`, linha JSONL 206 (linhas internas 40, 45–46 do anexo citado), 224–225; mirror `808b6c2a-783e-41ab-9ace-f17a844f01fe`, linhas 9–30. Identidades e limites no recibo `BRAIN/99-SISTEMA/brain-v2/reports/coverage-2026-09-25-daily.json`.
