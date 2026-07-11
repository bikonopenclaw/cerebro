# Instagram Bikon, Robotnik

```yaml
nome: Instagram Bikon Robotnik
status: configurado_em_draft
responsavel: Robotnik sob coordenação do Puppet Master
ultima_revisao: 2026-07-11
fonte: conversa Hebert/Puppet Master e workspace Robotnik
tags: [instagram, meta, robotnik, marketing, bikon]
```

## Objetivo

Conectar o Instagram profissional da Bikon ao Robotnik para preparar posts, captions, Reels e futuramente publicar ou agendar via API oficial.

## Decisão técnica

Usar Meta Graph API oficial.

Não usar:

- login/senha do Instagram em script
- automação de navegador para postar
- scraping
- extensões ou serviços não autorizados

## Status atual

Em 2026-06-25, Hebert confirmou que:

- o Instagram da Bikon é profissional
- está ligado a uma Página do Facebook
- a verificação de segurança da Meta poderia levar até 2 dias úteis

Em 2026-06-26, a verificação de segurança da Meta foi marcada como aprovada e a integração saiu do estado de espera. A publicação real continua bloqueada até configuração segura, testes controlados e aprovação explícita.

Em 2026-07-09, foram validados via Meta/Graph:

- Página Facebook da Bikon conectada ao Instagram profissional.
- `META_PAGE_ID` e `INSTAGRAM_BUSINESS_ACCOUNT_ID` identificados e testados.
- token de longa duração gerado e salvo somente em arquivo local de segredo do Robotnik, com permissão restrita.
- permissão `instagram_content_publish` confirmada.
- `ROBOTNIK_INSTAGRAM_MODE=draft` mantido para impedir publicação automática.

O Brain não registra token nem app secret. IDs operacionais podem aparecer apenas quando necessários para reconstruir contexto técnico; segredos permanecem fora do Git.

## Estrutura criada

- Workspace: `/data/.openclaw/workspace-robotnik/instagram-bikon`
- Script: `scripts/instagram_graph.py`
- Exemplo de env: `config/instagram-bikon.env.example`
- Segredos locais: `secrets/instagram-bikon.env`, fora do Git
- Template de post: `posts/post-template.json`
- Status inicial: `status/standby-meta-verificacao-2026-06-25.md`
- Status de retomada: `status/retomada-meta-aprovada-2026-06-26.md`

## Regra operacional

Modo inicial: `draft`.

Robotnik pode:

- preparar copy
- preparar rascunho de post
- preparar payload técnico
- validar formato e campos
- gerar ou ajustar arte de rascunho usando primeiro a ferramenta embutida de imagem do Codex/ChatGPT, pela skill `imagegen`, ou geração local determinística quando bastar

Robotnik não pode:

- publicar sem aprovação explícita
- receber senha ou token por chat
- expor token em relatório
- responder cliente externo sem aprovação
- usar `image_generate`, CLI de imagem, `OPENAI_API_KEY`, API externa paga ou serviço de terceiros para gerar imagem sem aprovação explícita do Hebert

## Rotina editorial relacionada

Em 2026-07-09, foram criados crons do Robotnik para cadência editorial:

- diário, segunda a sexta às 07:30 America/Sao_Paulo: pesquisar fontes externas, propor 3 pautas e preparar material em rascunho;
- semanal, sexta às 16:00 America/Sao_Paulo: propor 5 pautas para a semana seguinte;
- entrega esperada no Telegram: arte/carrossel anexado, copy, legenda e pedido de aprovação;
- publicação, agendamento ou envio externo continuam bloqueados até aprovação explícita do Hebert/Puppet Master.

Em 2026-07-10, foi observado rascunho editorial local para tema KEV/PME. A peça não representa publicação, agendamento ou aprovação; artefatos gerados de draft permanecem fora do Brain/Git.

## Próximos passos

1. Observar as primeiras entregas dos crons e ajustar briefing se vierem genéricas, sensacionalistas ou fora do escopo Bikon.
2. Manter fontes externas/notícias/RSS como entrada principal de pauta; usar Instagram API para contexto da Bikon, métricas, hashtags pontuais e publicação controlada.
3. Reavaliar publicação via API somente depois de rotina estável em modo rascunho e aprovação explícita por post.
