# Instagram Bikon, Robotnik

```yaml
nome: Instagram Bikon Robotnik
status: retomada_aprovada_meta
responsavel: Robotnik sob coordenação do Puppet Master
ultima_revisao: 2026-06-27
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

Robotnik não pode:

- publicar sem aprovação explícita
- receber senha ou token por chat
- expor token em relatório
- responder cliente externo sem aprovação

## Próximos passos pós-aprovação Meta

1. Gerar token Meta seguro de longa duração.
2. Salvar o token somente em `/data/.openclaw/workspace-robotnik/instagram-bikon/secrets/instagram-bikon.env`.
3. Rodar testes seguros:
   - `python3 scripts/instagram_graph.py me`
   - `python3 scripts/instagram_graph.py pages`
4. Identificar e preencher no arquivo local de segredos:
   - `META_PAGE_ID`
   - `INSTAGRAM_BUSINESS_ACCOUNT_ID`
5. Manter `ROBOTNIK_INSTAGRAM_MODE=draft` e publicação travada até teste validado e aprovação explícita.

## Cron relacionado

Existe lembrete one-shot para retomar a integração:

- Nome: `Retomar integração Instagram Bikon Robotnik`
- Data: 2026-06-29 09:00 BRT
- Objetivo: verificar com Hebert se a Meta aprovou a verificação.
