---
id: brain-ee4e9b868c7dc6d3dbd0
type: knowledge
title: Separar teste, rascunho e produção em automações externas
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:18:32.790773Z'
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/API-WHATSAPP-BIKON.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md#relações
---

# Separar teste, rascunho e produção em automações externas

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W26 e FIP Document Intake Gateway 2026-08-19
confiabilidade: alta
ultima_revisao: 2026-08-19
tags: [guardrails, dry-run, rascunho, producao, automacoes, comunicacao-externa, aprovacao, hash]
```

## Princípio

Automações que podem gerar efeito externo devem separar claramente preparação interna, teste controlado e execução real.

## Aplicação prática

- Usar `dry-run`, rascunhos, payloads e pré-visualização como padrão inicial.
- Antes de envio, publicação, emissão, cancelamento, chamada real ou alteração operacional, listar o impacto esperado e exigir confirmação quando não houver autorização prévia.
- Em testes com dados reais, usar destinatário explícito e impedir lookup automático de cadastro que possa enviar para terceiros.
- Fixture sintetica nao deve ser executada contra producao; se isso ocorrer por erro, neutralizar no proprio dominio com estado explicito, rollback logico, delta verificado e trilha append-only.
- Manter logs, tokens, `.env` e artefatos sensíveis fora do Brain/Git.
- Registrar no Brain o estado operacional e os guardrails, não a execução sensível completa.

## Aprovação por etapa e por hash

- Separar aprovações de briefing, estratégia, geração paga, composição/render e publicação.
- Vincular a aprovação à operação, versão, parâmetros e hash apresentados.
- Tratar aprovação como uso único quando a operação puder consumir crédito ou alterar estado externo.
- Qualquer mudança de prompt, modelo, referência, quantidade, template, mídia, copy, canal ou data invalida a aprovação do portão afetado.
- Não herdar autorização entre operações. Rascunho não autoriza agendamento; agendamento não autoriza publicação; publicação não autoriza edição ou exclusão.
- Antes de repetir, consultar o ID da operação e seu resultado. Polling ou consulta de status nunca deve virar nova submissão.
- Registrar aprovador, horário UTC, evidência, ressalvas e correlação, sem copiar segredo.

## Exemplos conectados

- Notaas NFS-e BIKON: rascunho `.eml`, SMTP validado, anexos preparados e envio externo bloqueado sem autorização.
- API WhatsApp Bikon: rotina segura com dry-run por padrão e envio real somente com confirmação explícita.
- Instagram Bikon Robotnik: portões separados, Kling para mídia, Creatomate para composição e Buffer como único publicador.
- FIP Document Intake Gateway: source real ja ingerido pode validar idempotencia; fixture sintetica em producao precisa ser rejeitada ou neutralizada com auditoria.

## Relações

- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]
- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]
- [[70-AUTOMACOES/NOTAAS-NFSE|Skill Notaas NFS-e]]
- [[70-AUTOMACOES/API-WHATSAPP-BIKON|API WhatsApp Bikon]]
- [[70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK|Instagram Bikon, Robotnik]]

## Efeitos indiretos do payload

O escopo autorizado também alcança efeitos indiretos, como comunicação que possa ser disparada pelo provedor a partir dos campos enviados. Antes de executar, verificar esses efeitos junto com destinatários e configurações; omitir um campo não é prova suficiente de que o provedor não enviará uma mensagem.

O relato de 2026-06-26 sobre emissão de NFS-e sem e-mail externo registrou a intenção de omitir o e-mail do payload e parar se a API o exigisse. Esse episódio ilustra a necessidade de validar o efeito, sem comprovar o comportamento atual da API nem substituir uma política explícita de destinatários. Fonte: trecho 3554 no recibo `BRAIN/99-SISTEMA/brain-v2/reports/coverage-round2-20260921.json`.

## Complementos reconciliados — lote 6 de 2026-09-21

No episódio Notaas, o cliente local conservava rótulo interno homologation enquanto a configuração/destino e os documentos indicavam efeitos produtivos. Um rótulo de log, modo ou nome de diretório não prova sandbox: validar endpoint, credencial, contrato do ambiente e evidência do resultado antes de chamar uma ação de homologação. Não usar o episódio como autorização para emitir novamente. Fonte: unidades 35061, 36498.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
