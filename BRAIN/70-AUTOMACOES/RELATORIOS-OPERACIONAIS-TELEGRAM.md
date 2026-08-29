# Relatórios Operacionais Telegram

```yaml
categoria: canal_operacional
fonte: decisão do Hebert em 2026-06-22, ajuste operacional de crons em 2026-08-03, reparo de rota em 2026-08-17, alias-router em 2026-08-19, checkpoint de crons em 2026-08-24, autoridade controlada de Felipe em 2026-08-26 e incidente P1 em 2026-08-27/29
confiabilidade: alta
ultima_revisao: 2026-08-29
tags: [telegram, relatorios, kowalski, ninjaone, eol, operacao, gateway, identidade-visual]
```

## Finalidade

Registrar o canal Telegram `relatórios operacionais` como grupo de consulta e produção de relatórios do dia a dia da Bikon.

## Grupo

- Nome: `relatórios operacionais`
- Chat observado: `telegram:-5165906669`
- Agente responsável: Kowalski
- Tipo de uso: consulta, relatório e análise operacional.

## Roteamento Telegram em 2026-07-09

Hebert autorizou a evolução do grupo para canal isolado do Kowalski:

- Bot Kowalski: `@mattedi_02_bot`.
- Gateway dedicado: `openclaw-gateway-kowalski.service`.
- Porta dedicada: `18810`.
- Puppet Master continua no grupo, mas com `requireMention=true`.
- Kowalski fica com resposta direta para mensagens comuns dentro do escopo de relatórios operacionais.
- A coordenação agente-a-agente e decisões com impacto continuam sob Puppet Master.

Token, auth store e configuração sensível ficam fora do Brain/Git.

## Escopo permitido

- Relatórios operacionais para clientes.
- Consulta a dados NinjaOne quando houver acesso/fonte disponível.
- Relatórios por dispositivo, alertas, inventário, disponibilidade, backup e evidências técnicas.
- Pareceres técnicos em linguagem Bikon quando aprovados pelo fluxo.

## Autoridade controlada de Felipe Nogueira, 2026-08-26

No grupo Relatorios Operacionais, Felipe pode solicitar e autorizar somente:

- abertura, atualizacao e fechamento de ticket operacional no NinjaOne;
- execucao de script NinjaOne ja existente e previamente aprovado, limitada ao escopo e aos parametros informados no pedido;
- alteracao de layout de relatorio operacional;
- pesquisa read-only em API ja liberada para a Bikon.

Roteamento: ticket, script e pesquisa em fonte operacional ficam com Sentinel; layout e documento ficam com Kowalski.

Essa autoridade nao inclui API ou endpoint novo, ampliacao de credencial/permissao, criacao ou alteracao de script, cron, configuracao, integracao, mudanca de rota, fallback, acao em massa, alteracao de backup, comunicacao externa, financeiro, fiscal ou gasto. Esses dominios continuam dependentes de autorizacao do Hebert.

## Fora de escopo

- Alterar estrutura operacional do Kowalski.
- Alterar skills, arquivos, configurações ou processos do Kowalski a partir do grupo.
- Acionar Puppet Master/main de forma independente pelo grupo.
- Acionar Darth Vader ou outro agente sem coordenação de Puppet Master.
- Comunicação externa para cliente sem aprovação explícita.
- Mudança em produção, faturamento, cobrança, site, checkout ou integração.

## Regra de identidade no grupo

Com bot próprio validado, mensagens comuns do grupo devem ser tratadas pelo Kowalski quando forem de relatório operacional. Puppet Master só deve responder quando mencionado nominalmente ou quando houver coordenação, mudança estrutural, produção, gasto, comunicação externa ou decisão estratégica.

## Roteamento FIP/Darth em 2026-08-17

Após falha real de rota em pedido de cenário financeiro, o grupo foi ajustado para evitar resposta direta de workers quando a execução envolver Darth/Kowalski e FIP:

- runtime isolado do Kowalski (`openclaw-gateway-kowalski.service`, porta `18810`) passou a registrar o agente canonico `darth-vader`;
- o grupo `telegram:-5165906669` passou a rotear para Puppet Master como owner externo quando houver fluxo com workers;
- `darth-vader` e `kowalski` ficaram cobertos pelo guard `relatorios-operacionais-workers-no-external-outbound`, bloqueando tool `message` externo para workers;
- o perfil isolado do Kowalski foi corrigido para modelo ChatGPT/OAuth `openai/gpt-5.5`, com fallback `openai/gpt-5.5`/`openai/gpt-5.4`, sem introduzir API key/billing;
- prova real do fluxo: Puppet respondeu uma vez no grupo, Darth e Kowalski tiveram resposta externa direta `0`, FIP actuals e porta `9213` nao sofreram mutacao.

O pedido de cenário Grupo Unus ficou validado como consulta gerencial read-only: a reducao para R$ 24.000,00 substitui os R$ 42.942,42 canonicos do grupo dentro do cenario; Simples usa perfil/recorrencia canonica, nao chute percentual.

## Alias-router em 2026-08-19

Apos evidencia de `REPLY_SKIP` em consulta Corpus/NinjaOne, o grupo manteve Puppet Master como owner externo e recebeu reparo de contrato de alias no main profile:

- rota externa do grupo `telegram:-5165906669`: Telegram default account -> `main`;
- Kowalski nao foi restaurado como owner externo; `enabled=false`, `groupPolicy=disabled`, `requireMention=true` no perfil isolado;
- `requireMention=false` do main no grupo ja nao era o bloqueio; o defeito era contrato semantico de alias/resposta visivel;
- alias-router adicionado para inicio de mensagem: `Puppet`, `Puppet Master`, `Kowalski`, `Darth` e `Darth Vader`;
- match incidental fora do inicio da frase deve retornar `none`;
- alias `Kowalski` deve usar `sessions_send` para `agent:kowalski:main`; alias `Darth`/`Darth Vader` deve usar `sessions_send` para `agent:darth-vader:main`;
- resposta visivel em grupo deve sair pelo Puppet via `message(action=send)`;
- guard `relatorios-operacionais-workers-no-external-outbound` continua bloqueando `message` externo de Kowalski/Darth quando a source for o grupo Relatorios;
- falha/timeout de worker deve gerar resposta unica sanitizada, sem stack trace, shell, SQLite, paths, provider, payloads, credenciais ou erro bruto.

Validacoes locais do reparo:

- aliases Puppet/Kowalski/Darth/Darth Vader: `PASS`;
- unaddressed routing de clientes Corpus/NinjaOne para Kowalski: `PASS`;
- unaddressed routing de caixa/recebiveis para Darth: `PASS`;
- worker external send bloqueado para Kowalski/Darth e permitido para Puppet;
- `RAW_INTERNAL_ERROR_DISCLOSURE_COUNT=0`;
- FIP, FCOC, card interview, porta `8787` e porta `9213`: mutacao `0`.

Reload do gateway principal foi solicitado via SIGUSR1 sem sudo; o reload de canal ficou `deferred` enquanto a propria execucao estava ativa. Retry real ainda necessario: `Kowalski, vc sabe quais sao os clientes da corpus no ninjaone?`, esperando Puppet externo `1`, Kowalski externo `0` e silencio `0`.

## Agenda automática diária

Atualização 2026-08-03:

- Relatórios diários ter-sex no grupo `Relatórios Operacionais`: WhatsApp 07:45, ARX Backup 07:46, NinjaOne 07:47 e Bitdefender 07:48, timezone `America/Sao_Paulo`.
- Instrução diária do Kowalski no grupo `Suporte Bikon`: 07:59, timezone `America/Sao_Paulo`.
- Antes/depois do ajuste foi usada a verificação local de sobreposição de crons; não reativar nem recriar arquitetura antiga.
- Regra prática: segunda-feira usa fechamento semanal coletado no sábado; não forçar job diário de segunda quando não houver cache diário correspondente.

Checkpoint 2026-08-24:

- Janela canonica de entrega solicitada por Hebert: `07:45-07:48 America/Sao_Paulo`.
- Relatorios diarios de NinjaOne estavam habilitados sob Kowalski no cron `5cee835c-67c0-4761-ad54-e5ddd6175150`, expressao `47 7 * * 2-5`.
- Relatorio semanal NinjaOne estava habilitado sob Kowalski no cron `b1c0fdbf-69ad-4b27-978e-10590ce3dbac`, expressao `47 7 * * 1`.
- Nao voltar ao padrao antigo de segunda `08:00-08:03`; semanais devem respeitar a mesma janela operacional.
- Ticketing ARX -> NinjaOne e relatorios operacionais sao responsabilidades distintas: o primeiro pode criar/fechar tickets apenas quando reautorizado e validado; o segundo entrega resumo na janela acordada.

## Incidente P1 de entrega, 2026-08-27/28

Evidencia real confirmou indisponibilidade dos resumos diarios WhatsApp Bikon, ARX Backup, NinjaOne Tickets e Bitdefender, alem de `OPERATIONAL_TOWER_DELIVERY=NOT_DELIVERED`.

Estado consolidado:

- incidente `P1` aberto para restaurar a cadeia completa schedule -> coleta Sentinel -> estado/input canonico -> consumo Kowalski -> artefato -> entrega Telegram;
- a mensagem generica `coleta Sentinel/Kowalski nao gerou arquivo` e sintoma, nao causa raiz comprovada;
- o executor P1 morreu antes do workload, sem diagnostico completo, patch, artefato ou catch-up;
- admissao `f3c9c0bf-07f9-4c53-8257-92c810249e29` permaneceu `DEFERRED` com `--wait` vivo; nao abrir retry concorrente;
- retomada depende do reparo B1 do lifecycle RSE e do deploy B2 autorizado, sempre pela rota canonica;
- ao retomar, reconciliar Sentinel `bd15e995-81f5-4c24-97e2-a67168ec9ce2` e Kowalski `3c4ae1da-0ded-42a8-8333-188ad3e75f2e`, autenticando cada transicao ate terminalidade;
- catch-up so pode ocorrer exatamente uma vez, no grupo correto, com dados validos/frescos e prova de idempotencia.

Tentativa posterior de retomada em 2026-08-28 tambem terminou antes do workload: o isolamento recebeu perfil de aproximadamente 5,77 GB, enquanto o RSE liberava aproximadamente 4,47 GB. Houve zero spawn, zero bootstrap, zero execucao do P1 e zero entrega; a admissao dessa tentativa foi cancelada sem orfao. O incidente permanece aberto e nao deve receber novo retry concorrente enquanto o reparo M2 nao fechar, for congelado e atravessar seu boundary de implantacao proprio.

Ownership preservado: Sentinel coleta e mantem dados operacionais; Kowalski produz e entrega relatorios internos; Puppet Master governa orquestracao, autoridade e comunicacao externa. Identidade visivel do bot no Telegram nao prova ownership de schedule, execucao, relatorio ou entrega.

## Padrão visual para relatórios externos

Em 2026-06-23, após revisão da versão premium do parecer do Cartório Capixaba, ficou registrado como padrão operacional para PDFs externos da Bikon:

- Usar identidade visual Bikon com acabamento corporativo e leitura séria.
- Evitar aparência de HTML impresso.
- Remover cabeçalhos e rodapés automáticos de navegador/documento, incluindo data técnica, caminho, URL, título repetido e paginação visualmente pobre.
- Manter apenas elementos institucionais quando fizerem parte natural do layout.
- Preservar conteúdo técnico, conclusões e estrutura quando a solicitação for apenas ajuste visual.
- Conferir visualmente o PDF renderizado antes de enviar ao Hebert ou ao grupo.

## Guardião visual Bikon

Em 2026-07-09, a responsabilidade visual do Kowalski foi ampliada para além de relatórios:

- revisar post, carrossel, PDF, apresentação, proposta, landing page, template e material público ou semi-público com logo/paleta/layout da Bikon;
- devolver veredito, três ajustes prioritários e risco visual principal;
- manter Robotnik como responsável por pauta, copy e campanha;
- evitar que estética hacker/cyberpunk, SaaS genérico, excesso de texto ou promessa exagerada chegue à peça final;
- não publicar, enviar, agendar ou aplicar mudança externa sem aprovação explícita.

## Guardrails

- Se o NinjaOne ou outra fonte não tiver histórico granular de CPU, RAM, disco ou eventos, registrar a limitação sem inventar métrica.
- Não incluir caminho interno de arquivo em relatório final para cliente.
- Relatório externo deve sair limpo, profissional e sem comentário operacional.
- Usuários adicionados por Hebert podem consultar dentro do grupo, mas não ganham permissão para acionar outros agentes.
- Workers internos nao devem responder externamente quando a rota tiver owner Puppet; retorno de Darth/Kowalski deve voltar ao Puppet para resposta unica ao grupo.
- Alias de especialista no grupo so deve valer no inicio da mensagem; mencao incidental a Kowalski/Darth no meio de frase nao deve desviar owner nem acionar worker.

## Caso de uso inicial

Em 2026-06-22, o grupo foi usado para solicitar parecer técnico do Cartório Capixaba:

- Incluir embasamento no Provimento CNJ 213/2026.
- Remover referência a local/caminho de arquivo no relatório.
- Tentar usar dados históricos por dispositivo.
- Evidenciar CPU, memória, disco, alertas e gargalos quando auditáveis.
- Gerar PDF para cliente externo.

Resultado: Kowalski gerou e enviou PDF no grupo, com ressalva explícita sobre limitações de histórico granular quando a fonte não retornou séries contínuas.


## Ajuste visual ARX em 2026-07-02

Um PDF enviado no grupo precisou ser refeito com o conteúdo recebido encaixado dentro do layout ARX/Bikon. O caso reforça o padrão:

- preservar conteúdo técnico aprovado;
- aplicar identidade visual Bikon/ARX quando o pedido for formatação externa;
- remover vestígios de caminho local, metadados de impressão, nome de agente ou comentário operacional;
- validar o arquivo final antes do envio.

## Lista de clientes NinjaOne em 2026-07-07

Solicitação no grupo pediu lista simples de clientes cadastrados no NinjaOne. O registro relevante para o Brain é o padrão operacional: quando o pedido for apenas listagem em texto, responder de forma simples no próprio chat e evitar gerar artefato, PDF ou relatório final desnecessário.

## Modelo de Relatório EOL Bikon, 2026-07-13

Hebert aprovou como padrão oficial para próximos relatórios de EOL o `Modelo de Relatório EOL Bikon`.

Regras consolidadas:

- não nomear o modelo por cliente;
- usar PDF com identidade Bikon, capa limpa, cards de KPI, tabela com cabeçalho escuro e legendas/badges condensados;
- manter a lógica: software EOL vira ação interna Bikon; compra física entra apenas quando houver hardware classificado para substituição;
- validar capa, paginação, legenda em uma linha, ausência de termos internos e exportação final em PDF antes de enviar;
- manter PDFs finais e lotes gerados fora do Brain/Git.

## Correção do dossiê técnico em 2026-07-22

- A última saída correta do grupo foi identificada como o dossiê técnico Bikon originalmente publicado na mensagem `657` do grupo.
- O PDF foi regenerado do mesmo HTML sem cabeçalho e rodapé automáticos do navegador, preservando três páginas A4 e o miolo textual.
- O envio corrigido e válido para o usuário é a mensagem `9396`.
- A identificação e o envio anteriores do EOL do 1º Ofício de Presidente Kennedy foram tratados como erro e não devem ser usados como referência desta entrega.
- Regra reforçada: antes de refazer a “última saída”, resolver a última mensagem com anexo no histórico real do grupo e validar identidade, data e arquivo antes da geração e do envio.

## Relações

- Agente Kowalski: `BRAIN/60-AGENTES/KOWALSKI.md`
- Escopo de canais operacionais: `BRAIN/40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md`
- Bikon: `BRAIN/20-EMPRESAS/BIKON/README.md`
