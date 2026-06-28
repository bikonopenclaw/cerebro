# Separar teste, rascunho e produção em automações externas

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W26
confiabilidade: alta
ultima_revisao: 2026-06-28
tags: [guardrails, dry-run, rascunho, producao, automacoes, comunicacao-externa]
```

## Princípio

Automações que podem gerar efeito externo devem separar claramente preparação interna, teste controlado e execução real.

## Aplicação prática

- Usar `dry-run`, rascunhos, payloads e pré-visualização como padrão inicial.
- Antes de envio, publicação, emissão, cancelamento, chamada real ou alteração operacional, listar o impacto esperado e exigir confirmação quando não houver autorização prévia.
- Em testes com dados reais, usar destinatário explícito e impedir lookup automático de cadastro que possa enviar para terceiros.
- Manter logs, tokens, `.env` e artefatos sensíveis fora do Brain/Git.
- Registrar no Brain o estado operacional e os guardrails, não a execução sensível completa.

## Exemplos conectados

- Notaas NFS-e BIKON: rascunho `.eml`, SMTP validado, anexos preparados e envio externo bloqueado sem autorização.
- API WhatsApp Bikon: rotina segura com dry-run por padrão e envio real somente com confirmação explícita.
- Instagram Bikon Robotnik: modo `draft` até token/IDs seguros, testes controlados e aprovação de publicação.

## Relações

- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md`
- `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- `BRAIN/70-AUTOMACOES/API-WHATSAPP-BIKON.md`
- `BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md`
