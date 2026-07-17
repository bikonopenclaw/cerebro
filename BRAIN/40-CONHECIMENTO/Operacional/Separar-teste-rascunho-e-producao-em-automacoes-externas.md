# Separar teste, rascunho e produção em automações externas

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W26
confiabilidade: alta
ultima_revisao: 2026-07-17
tags: [guardrails, dry-run, rascunho, producao, automacoes, comunicacao-externa, aprovacao, hash]
```

## Princípio

Automações que podem gerar efeito externo devem separar claramente preparação interna, teste controlado e execução real.

## Aplicação prática

- Usar `dry-run`, rascunhos, payloads e pré-visualização como padrão inicial.
- Antes de envio, publicação, emissão, cancelamento, chamada real ou alteração operacional, listar o impacto esperado e exigir confirmação quando não houver autorização prévia.
- Em testes com dados reais, usar destinatário explícito e impedir lookup automático de cadastro que possa enviar para terceiros.
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

## Relações

- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md`
- `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- `BRAIN/70-AUTOMACOES/API-WHATSAPP-BIKON.md`
- `BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md`
