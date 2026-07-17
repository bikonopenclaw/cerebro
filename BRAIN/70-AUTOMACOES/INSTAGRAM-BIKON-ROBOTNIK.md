# Instagram Bikon, Robotnik

```yaml
nome: Instagram Bikon Robotnik
status: implantacao_controlada
responsavel: Robotnik sob coordenação do Puppet Master
ultima_revisao: 2026-07-17
fonte: conversa Hebert/Puppet Master e workspace Robotnik
tags: [instagram, meta, robotnik, marketing, bikon]
```

## Objetivo

Planejar, gerar, compor, revisar e publicar conteúdo do Instagram Bikon com portões humanos, rastreabilidade e um único escritor do estado de publicação.

## Decisão técnica atual

Usar a seguinte divisão de responsabilidade:

- Robotnik: pesquisa, pauta, copy, roteiro e direção criativa.
- Puppet Master: coordenação, portões e consolidação.
- Kling CLI: geração de mídia bruta.
- Creatomate: composição determinística de logo, texto, CTA, tipografia e avisos.
- Buffer: único sistema autorizado a criar rascunho, agendar ou publicar.
- Hebert: aprovação de gasto e ação externa.

A integração Meta Graph API validada em 2026-07-09 permanece como histórico técnico e contingência não autorizada. Ela não é mais a rota produtiva de publicação.

Não usar:

- login/senha do Instagram em script
- automação de navegador para postar
- scraping
- extensões ou serviços não autorizados
- Meta Graph API, Instagram direto ou BlackTwist como publicador paralelo ao Buffer

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

Em 2026-07-17, a arquitetura de produção foi consolidada:

- skill `instagram-brand-director` implantada;
- Kling CLI 0.1.3 contratada somente para `text_to_image`;
- adapter corrigido para o prompt posicional real, com nove testes aprovados;
- nenhuma geração enviada e nenhum crédito consumido;
- brand pack oficial validado com Space Grotesk, logos oficiais e paleta Bikon;
- conta Creatomate criada;
- template `BIKON-FEED-4X5-V1`, ID `f3539d0c-8551-4913-b006-104f3354f0e7`, validado como PNG 1080 × 1350;
- credencial Creatomate validada sem exposição e mantida fora do Brain/Git;
- template ainda sem as camadas produtivas na última validação;
- Buffer ainda sem perfil e credencial configurados.

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
- preparar prompt, referências, manifesto e parâmetros de geração

Robotnik não pode:

- publicar sem aprovação explícita
- receber senha ou token por chat
- expor token em relatório
- responder cliente externo sem aprovação
- submeter geração Kling sem aprovação dos parâmetros exatos
- renderizar no Creatomate sem aprovação do portão de composição
- criar rascunho, agendar, publicar, editar ou excluir no Buffer sem a autorização específica da operação

## Portões de produção

1. Briefing: objetivo, público, oferta, formato, KPI, prazo e restrições.
2. Estratégia e rota: pilar, ângulo, hook, copy, fontes e direção visual.
3. Geração: comando Kling, modelo, prompt, referências, quantidade, custo e hash exatos.
4. Composição e render: mídia aprovada, template, textos, logo, CTA, avisos, áudio, legendas e hash do render.
5. Publicação: canal, legenda, data, operação exata e versão final.

Uma aprovação vale somente para o portão, os parâmetros e o hash apresentados. Nova variante exige nova aprovação. Criar rascunho não autoriza agendar; agendar não autoriza publicar, editar ou excluir.

## Rotina editorial relacionada

Em 2026-07-09, foram criados crons do Robotnik para cadência editorial:

- diário, segunda a sexta às 07:30 America/Sao_Paulo: pesquisar fontes externas, propor 3 pautas e preparar material em rascunho;
- semanal, sexta às 16:00 America/Sao_Paulo: propor 5 pautas para a semana seguinte;
- entrega esperada no Telegram: arte/carrossel anexado, copy, legenda e pedido de aprovação;
- publicação, agendamento ou envio externo continuam bloqueados até aprovação explícita do Hebert/Puppet Master.

Em 2026-07-10, foi observado rascunho editorial local para tema KEV/PME. A peça não representa publicação, agendamento ou aprovação; artefatos gerados de draft permanecem fora do Brain/Git.

## Próximos passos

1. Concluir as camadas dinâmicas do master Creatomate e preencher o `template-map`.
2. Validar a credencial no contexto efetivo do runtime e executar preflight sem render.
3. Configurar o perfil Bikon no Buffer como único publicador.
4. Executar piloto controlado de cibersegurança com uma imagem, passando por todos os portões.
5. Manter fontes externas como entrada principal de pesquisa e usar métricas somente como evidência editorial.
