# Instagram Bikon, Robotnik

```yaml
nome: Instagram Bikon Robotnik
status: stand_by
responsavel: Robotnik sob coordenação do Puppet Master
ultima_revisao: 2026-06-25
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
- a verificação de segurança da Meta pode levar até 2 dias úteis

Integração ficou em stand by até aprovação da verificação.

## Estrutura criada

- Workspace: `/data/.openclaw/workspace-robotnik/instagram-bikon`
- Script: `scripts/instagram_graph.py`
- Exemplo de env: `config/instagram-bikon.env.example`
- Segredos locais: `secrets/instagram-bikon.env`, fora do Git
- Template de post: `posts/post-template.json`
- Status: `status/standby-meta-verificacao-2026-06-25.md`

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

## Próximo passo quando a Meta aprovar

1. Acessar Meta Developers.
2. Criar/configurar app da Bikon.
3. Liberar permissões necessárias, incluindo `instagram_basic`, `instagram_content_publish`, `pages_show_list` e permissões correlatas exigidas pela Meta.
4. Gerar token seguro de longa duração.
5. Salvar em `/data/.openclaw/workspace-robotnik/instagram-bikon/secrets/instagram-bikon.env`.
6. Rodar teste de listagem de páginas e conta Instagram:
   - `/data/.openclaw/workspace-robotnik/instagram-bikon/scripts/instagram_graph.py pages`
7. Manter publicação travada até teste validado e aprovação explícita.

## Cron relacionado

Existe lembrete one-shot para retomar a integração:

- Nome: `Retomar integração Instagram Bikon Robotnik`
- Data: 2026-06-29 09:00 BRT
- Objetivo: verificar com Hebert se a Meta aprovou a verificação.
