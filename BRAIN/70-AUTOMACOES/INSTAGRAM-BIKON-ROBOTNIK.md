# Instagram Bikon, Robotnik

```yaml
nome: Instagram Bikon Robotnik
status: contrato_criativo_v1_ativo_piloto_aceito_publicacao_bloqueada
responsavel: Robotnik sob coordenação do Puppet Master
ultima_revisao: 2026-09-09
fonte: conversa Hebert/Puppet Master e workspace Robotnik
tags: [instagram, meta, robotnik, marketing, bikon]
```

## Objetivo

Planejar, gerar, compor, revisar e publicar conteúdo do Instagram Bikon com portões humanos, rastreabilidade e um único escritor do estado de publicação.

## Decisão técnica atual

Usar a seguinte divisao de responsabilidade:

- Robotnik: pesquisa, pauta, copy, roteiro e direção criativa.
- Puppet Master: coordenação, portões e consolidação.
- `content-production-contract` v1: unica autoridade criativa Bikon.
- `image_gen.imagegen`: rota principal registrada para geracao/edicao visual na autenticacao ChatGPT ja existente.
- Finalizacao local deterministica: somente tipografia, logo oficial, recorte, contraste e exportacao; nao substitui a fotografia.
- Kowalski: revisao dos bytes reais e da referencia canonica antes da entrega.
- Hebert: aprovação de gasto e ação externa.

A arquitetura Kling/Creatomate/Buffer e a integracao Meta Graph API permanecem como historico tecnico. Nao sao direcoes ou fallbacks ativos. A skill vigente registra publicador canonico proprio, mas nenhuma publicacao, staging ou agendamento novo esta autorizado pelo aceite do piloto.

Não usar:

- login/senha do Instagram em script
- automação de navegador para postar
- scraping
- extensões ou serviços não autorizados
- Meta Graph API, Instagram direto, Buffer, BlackTwist ou outro publicador sem autorizacao especifica e contrato vigente

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

Em 2026-07-20, a operação avançou para Produção Assistida:

- o conjunto Instagram Bikon v4 foi aprovado como canônico; cinco fundos Kling consumiram os 10 créditos autorizados e nenhuma publicação ocorreu;
- a Instagram Brand Director v2.1.0 foi implantada por corte atômico validado, com backup integral, rollback e recibo append-only; o lifecycle da proposta continua `pending`;
- a campanha `bikon-operacao-sem-dependencia-20260720` iniciou o fluxo assistido;
- o snapshot `feed-base-a v1` foi congelado com sete arquivos em modo somente leitura e duas leituras integrais idênticas;
- Brand QA pré-geração e Brand Lock do snapshot fecharam em `PASS` para manifesto `474e9af2214cbe0faa25fa9aad2535bff0260bf94752a70a6b3f21352ebfc5de`, request `5d721862890d4a5c8f72e458f9a79ce59ff70a10be5d4a9a527eaf2374b8c6a3` e payload `2be351a05379c0410a3cbba53da1c536c090c853273cef4e5a82f43ea2a642c7`;
- Portão C, Approval individual, execução Kling, composição, upload e publicação permanecem bloqueados.

Esse bloco registra a arquitetura historica de julho. Em 2026-09-08, as instrucoes criativas concorrentes foram retiradas do uso ativo e substituidas pelo contrato v1 descrito abaixo.

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
- trocar a rota `image_gen.imagegen` por Kling, Creatomate, CLI paga, `openclaw.image_generate` ou outro provider por conveniencia
- criar rascunho, agendar, publicar, editar ou excluir em qualquer publicador sem a autorização específica da operação

## Portões de produção

1. Briefing: objetivo, público, oferta, formato, KPI, prazo e restrições.
2. Estratégia e rota: pilar, ângulo, hook, copy, fontes e direção visual.
3. Geração: ferramenta nativa registrada, prompt, referências, quantidade e identidade/hash da saída.
4. Finalização: mídia aprovada, textos, logo oficial, crop, contraste, formato e hash do export.
5. Publicação: canal, legenda, data, operação exata e versão final.

Uma aprovação vale somente para o portão, os parâmetros e o hash apresentados. Nova variante exige nova aprovação. Criar rascunho não autoriza agendar; agendar não autoriza publicar, editar ou excluir.

O `PASS` de Brand QA do snapshot não autoriza geração. Qualquer byte alterado em artefato congelado, prompt, request ou parâmetro invalida o snapshot e exige novo manifesto, novo hash e novo Brand QA.

## Indicadores da Produção Assistida

- `LTPA`, Lead Time to Production Approval: tempo do início do fluxo de aprovação até o pacote final. No fechamento do Brand QA do snapshot, estava em `2.723,846 s` e ainda aberto.
- `SSI`, Snapshot Stability Index: snapshots aprovados na primeira submissão divididos pelo total submetido ao Brand QA. Valor inicial `50%`, com um aprovado na primeira submissão de dois snapshots.
- `SFT`, Snapshot Freeze Time: tempo entre o início do congelamento e duas leituras consecutivas idênticas do manifesto. Valor inicial `68,985 s`, sete arquivos e uma tentativa.

Registrar quantidade de snapshots, rejeições, motivo, correções locais, tempo entre congelamento e aprovação e ausência ou presença de ações externas.

## Rotina editorial relacionada

Em 2026-07-09, foram criados crons do Robotnik para cadência editorial:

- diário, segunda a sexta às 07:30 America/Sao_Paulo: pesquisar fontes externas, propor 3 pautas e preparar material em rascunho;
- semanal, sexta às 16:00 America/Sao_Paulo: propor 5 pautas para a semana seguinte;
- entrega esperada no Telegram: arte/carrossel anexado, copy, legenda e pedido de aprovação;
- publicação, agendamento ou envio externo continuam bloqueados até aprovação explícita do Hebert/Puppet Master.

Em 2026-07-10, foi observado rascunho editorial local para tema KEV/PME. A peça não representa publicação, agendamento ou aprovação; artefatos gerados de draft permanecem fora do Brain/Git.

## Próximos passos

1. Tratar o piloto aceito como concluido, sem correcao silenciosa, nova geracao ou reenvio.
2. Para uma nova peca, carregar o contrato v1, a referencia canonica e os assets oficiais em sessao nova.
3. Preservar geracao, finalizacao, revisao, entrega e publicacao como portoes separados, todos vinculados a versao e hash.
4. Exigir autorizacao especifica antes de qualquer staging, upload, agendamento ou publicacao.

## Reconciliação snapshot vs implantação (20:00+)

- Fonte oficial de evidência consultada: `reports/instagram-brand-director-v2.1.0-20260720/REPORT.md`.
- Conclusão: a proposta `instagram-brand-director-20260720-5b5709ec92` está `pending` e a skill ativa permanece em `v2.0.1` com hash `ed9fa...686cd`.
- O snapshot `1ffb6a1` continua desatualizado enquanto a janela de implantação não for executada com backup/rollback conforme protocolo.
- Portão C, composição e publicação permanecem bloqueados até nova decisão explícita de corte.

## Bloqueio de integridade em 2026-07-22

- A publicação de `v4-03-quarta-sem-log.png` foi interrompida antes da chamada externa porque o hash do arquivo local divergiu do conteúdo entregue pela URL temporária.
- `instagram_graph.py` não foi executado e nenhuma publicação ocorreu.
- URL temporária não substitui evidência de integridade. Antes de publicar, o conteúdo recuperado precisa reproduzir o hash aprovado do asset congelado; divergência mantém o gate fechado e exige nova decisão sobre a origem do arquivo.

## Bloqueio de transporte para Brand QA em 2026-09-07

- A esteira "sua empresa governada por IA" nao chegou ao runtime do Kowalski por uma rota de bytes aprovada e legivel; os caminhos e o pacote declarados pelo Robotnik nao estavam montados no ambiente do revisor.
- Kowalski nao abriu PNG, prancha ou pacote e, portanto, nao validou hash, dimensoes, paleta, logo, legibilidade mobile, clipping ou artefatos.
- Estado canonico: `FAIL_CLOSED`, esteira em rascunho e aprovacao humana pendente. Esse pacote nao deve ser confundido com a peca unica ja autorizada.
- Ate os mesmos bytes estarem acessiveis por mecanismo aprovado, ficam proibidos nova tentativa pelo mesmo caminho, revisao por declaracao de hash, troca improvisada de rota, alteracao do asset, upload, agendamento e publicacao.

## Contrato criativo v1 e piloto concluido em 2026-09-08

- `content-production-contract` v1 tornou-se a unica autoridade criativa Bikon e consolidou referencia canonica, brand assets, direcao editorial, rota produtiva e criterios de QA.
- A geracao nativa produziu sete PNGs completos. A fronteira de artefato foi resolvida somente para esse conjunto por handoff autorizado, imutavel e verificado; o importer nao aceita paths livres nem autoriza exportacao futura generica.
- O piloto final `piloto-ia-sem-dono-rascunho-final.png`, SHA-256 `6c5fe3548dac700798f64cfcaf52c1d9cd353d7a4debfe727e42bd26774525a8`, foi revisado pelo Kowalski, entregue pelo gateway Robotnik como documento Telegram `messageId 794` e aceito por Hebert.
- Estado terminal: `HUMAN_ACCEPTED / COMPLETE`. Aprovacao da peca nao autoriza Instagram, staging, upload, agendamento, publicacao, nova serie ou reutilizacao das cinco artes reprovadas.
