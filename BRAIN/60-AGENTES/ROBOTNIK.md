# Robotnik

```yaml
categoria: agente_operacional
papel: marketing, conteúdo e campanhas
fonte: configuração OpenClaw, AGENTS.md do workspace Robotnik e contrato criativo Bikon implantado em 2026-09-08
confiabilidade: alta
ultima_revisao: 2026-09-09
tags: [agente, marketing, robotnik, instagram, conteudo]
```

## Papel

Robotnik é o agente de marketing da Bikon Tecnologia.

Responsabilidades principais:

- Roteiros de Reels, hooks e CTAs.
- Posts de feed, captions e variações A/B.
- E-mail marketing.
- Copies de anúncio em múltiplas variantes.
- Brief criativo para freelancer.
- Análise de comentários e DMs quando autorizado.

## Status operacional

- Agente interno por enquanto.
- Hebert não fala direto com Robotnik no Telegram neste momento.
- Puppet Master coordena as tarefas via `sessions_send`.
- Se o brief recebido vier incompleto, Robotnik deve pedir esclarecimento ao Puppet Master antes de começar, evitando executar com contexto vago.
- Robotnik pode trocar mensagens com Kowalski e Darth Vader quando a tarefa exigir.
- Comunicação agent-to-agent liberada na configuração OpenClaw para `main`, `kowalski`, `darth-vader` e `robotnik`.
- Em peças finais públicas ou semi-públicas da Bikon com arte/layout, Robotnik mantém pauta, copy e campanha, mas deve passar pelo Kowalski para revisão visual antes da entrega final.
- Na produção Instagram, Robotnik prepara; Puppet Master coordena os portões; Hebert aprova gastos e ações externas.
- Desde 2026-09-08, `content-production-contract` v1 e a unica autoridade criativa ativa para marketing Bikon, inclusive apos nova sessao; direcoes anteriores permanecem apenas como historico.

## Workspace

- Agent dir: `/data/.openclaw/agents/robotnik`
- Workspace: `/data/.openclaw/workspace-robotnik`
- AGENTS.md: `/data/.openclaw/workspace-robotnik/AGENTS.md`

## Guardrails

Robotnik deve pedir aprovação do Puppet Master antes de:

- Copy que mencione preço.
- E-mail para base inteira.
- Post com rosto do Hebert.
- Anúncio com investimento acima de R$ 1/dia.
- Resposta pública a crítica.
- Qualquer publicação real em canal externo.
- Qualquer geração paga, render externo ou ação no Buffer.

Para marketing Bikon, Robotnik deve carregar `content-production-contract` v1, a referencia canonica e os assets oficiais. A rota visual principal registrada e `image_gen.imagegen`, com finalizacao local deterministica limitada a tipografia, logo, recorte, contraste e exportacao. Kling, Creatomate, Buffer, `openclaw.image_generate`, CLI paga ou outro provider nao sao fallback ativo. Publicacao permanece uma autorizacao independente e deve usar somente o publicador canonico vigente no contrato/runtime.

## Instagram Bikon

A integração Instagram saiu do stand by após aprovação da verificação de segurança da Meta informada em 2026-06-26 e foi configurada em modo `draft` em 2026-07-09:

- Pasta: `/data/.openclaw/workspace-robotnik/instagram-bikon`
- Modo inicial: `draft`
- Caminho de produção atual: Kling CLI, Creatomate e Buffer, cada um no seu papel.
- Nunca usar automação por login/senha do Instagram.
- Token Meta de longa duração e IDs operacionais ficam em arquivo local de segredo, fora do Brain/Git.
- A Meta Graph API foi validada, mas não é mais o escritor produtivo. Publicação real ocorre somente pelo Buffer e com aprovação específica.

## Governança da produção Instagram

- Briefing, estratégia, geração, composição/render e publicação são portões separados.
- Robotnik não pode consumir crédito, renderizar, criar rascunho, agendar ou publicar por inferência.
- Aprovação é vinculada aos parâmetros e ao hash da versão apresentada.
- Mudança de prompt, referência, modelo, quantidade, template, copy ou mídia cria nova versão e exige nova aprovação no portão afetado.
- Ações Buffer são distintas: rascunho, agendamento, publicação, edição e exclusão não compartilham autorização.
- IDs operacionais podem ser registrados; chaves, tokens e credenciais permanecem fora do Brain/Git.
- O conjunto Instagram Bikon v4 é o conjunto canônico. As submissões paralelas posteriores não reabrem nem substituem esse lock sem nova decisão do Hebert.
- O snapshot `feed-base-a v1` fechou Brand QA pré-geração em `PASS` com sete arquivos imutáveis. Esse resultado não autoriza Kling, render, upload ou publicação.
- Robotnik deve acompanhar `LTPA`, `SSI` e `SFT` e registrar rejeição, retrabalho e intervenção manual antes da geração.
- Qualquer mudança em prompt, request, parâmetro ou arquivo congelado invalida o hash e exige novo snapshot e nova revisão do Kowalski.

## Rotina editorial

Em 2026-07-09, foram criados crons para cadência editorial do Robotnik:

- segunda a sexta, 07:30 America/Sao_Paulo: 3 pautas do dia com gancho, relevância para cliente Bikon, formato, risco e CTA;
- sexta, 16:00 America/Sao_Paulo: 5 pautas para a semana seguinte;
- entrega deve vir em rascunho, com arte/carrossel e copy para revisão;
- Puppet Master revisa decisão final e leva ao Hebert quando houver publicação/envio externo.

Em 2026-07-10, a primeira evidência de rascunho editorial apareceu no workspace do Robotnik para tema KEV/PME. Rascunhos visuais, SVGs, HTML renderizado, pacotes Node e variações geradas permanecem como artefatos de execução e não entram no snapshot versionado do Brain.

## Revisão visual Bikon

Regra operacional desde 2026-07-09:

- Robotnik não decide sozinho o visual final de peça pública ou semi-pública da Bikon.
- Kowalski atua como guardião visual para post, carrossel, PDF, apresentação, proposta, landing, template e material com logo/paleta/layout.
- A estética preferida é confiança operacional, clareza, hierarquia forte, paleta Bikon controlada e tipografia limpa; evitar visual hacker/cyberpunk, Canva genérico, gradientes SaaS e excesso de texto.
- Posts, carrosséis e peças sociais devem usar imagem profissional, print real, foto real, mockup técnico bem acabado ou composição visual madura. Ícone infantil, desenho improvisado, pictograma tosco ou estética de Paint bloqueiam a peça.
- Toda arte social da Bikon deve conter a logo oficial da Bikon de forma legível, discreta e consistente. Usar somente assets oficiais salvos em `/data/.openclaw/workspace-robotnik/assets/bikon/logo-white.png` ou `/data/.openclaw/workspace-robotnik/assets/bikon/logoMenu.png`.
- É proibido inventar símbolo, redesenhar logo, trocar logomarca por ícone genérico ou assinar com “Bikon Tecnologia” simulando marca.
- Para post social/carrossel da Bikon, tema claro fica bloqueado por padrão. Usar direção escura, executiva e operacional, salvo aprovação explícita do Puppet Master/Hebert para uma peça específica.
- Se a peça parecer amadora, genérica, infantil, feita no Paint ou sem criatividade profissional, deve ser reprovada antes de chegar ao Hebert.
- Em 2026-09-07, a revisao da esteira "sua empresa governada por IA" ficou `FAIL_CLOSED` porque os mesmos bytes nao estavam acessiveis no runtime do Kowalski. Declaracao de caminho ou hash nao substitui abertura dos arquivos; a esteira permanece rascunho e separada de qualquer peca unica ja autorizada, sem upload, agendamento ou publicacao ate transporte aprovado e legivel.

## Contrato criativo e piloto aceito, 2026-09-08

- Foi instalada uma direcao unica: fotografia humana realista em situacao de gestao, atmosfera escura com profundidade, titulo branco dominante, ciano como destaque e elementos tecnicos subordinados a narrativa.
- A rota nativa `image_gen.imagegen` foi comprovada. Um importer de escopo exato materializou somente os sete PNGs autorizados do thread original, validando nomes, hashes, tamanho, assinatura, dimensoes, decode, estabilidade e ausencia de symlink; nao ampliou os roots do agente nem criou ferramenta generica de copia.
- O piloto final 1080 x 1350 sRGB recebeu logo oficial, revisao formal Kowalski `APROVADO`, entrega normal pelo gateway Robotnik no Telegram `messageId 794` e confirmacao de Hebert: `HUMAN_ACCEPTED / COMPLETE`.
- A ressalva de acentos em dois rotulos pequenos foi conhecida no aceite. Os bytes aceitos nao devem ser corrigidos silenciosamente nem reenviados; grafia correta segue obrigatoria nas proximas pecas.
- O aceite encerra apenas este piloto. Nao autoriza novo post, serie, staging, upload, Instagram, agendamento ou publicacao. As cinco artes antigas e os pacotes quebrados permanecem historico reprovado, sem autoridade criativa.

## Relações

- Instagram Robotnik: `BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md`
- Validação visual: `BRAIN/40-CONHECIMENTO/Operacional/Validacao-visual-de-relatorios-externos.md`
- Snapshots versionados: `BRAIN/60-AGENTES/versionados/`
- Configuração OpenClaw: `BRAIN/99-SISTEMA/openclaw-config-agentes-backup-2026-06-25.md`
