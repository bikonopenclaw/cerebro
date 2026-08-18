# Darth Vader

```yaml
categoria: agente_operacional
fonte: sessões operacionais visíveis, configuração de skills em 2026-06-17 e snapshot versionado em 2026-07-11
confiabilidade: alta
ultima_revisao: 2026-08-18
tags: [agente, financeiro, faturamento, nfse, boleto, remessa, cresol-api, fip]
```

## Papel

Agente operacional financeiro usado para tarefas de faturamento, NFS-e, boletos, remessas e conferências cadastrais quando a execução exigir especialização financeira/fiscal.

## Skills e contextos relevantes

- `notaas-nfse`: uso exclusivo da Darth Vader para NFS-e da Bikon, com segredos fora do Brain/Git.
- `emitir-nfse-boleto-remessa`: skill geral relacionada a NFS-e, boletos, remessas e API Cresol.
- `boletos-cresol`: skill técnica relacionada a boletos Cresol.

## Contextos removidos / históricos

- `faturamento-fn-souza`: estrutura inicial criada em 2026-06-17 para o fluxo de faturamento FN Souza, removida do conjunto ativo em 2026-06-25. Não deve ser acionada como skill ativa sem nova autorização explícita e novo escopo operacional.

## Guardrails

- Não emitir NFS-e real sem aprovação explícita.
- Não emitir boleto real sem aprovação explícita.
- Não gerar remessa de produção sem validação e aprovação explícita.
- Não usar API Cresol em produção sem aprovação explícita.
- Não executar baixa automática via API Cresol enquanto não houver procedimento próprio aprovado.
- Não enviar comunicação externa em nome da Bikon sem aprovação explícita.
- Pode preparar rascunhos, estrutura de arquivos, conferências e lista de pendências internas.
- Para NFS-e + boleto + remessa em lote, manter produção assistida e cadenciada: dry-run, conferência humana, aprovação explícita, emissão, conferência XML/PDF, depois boleto/remessa e só então comunicação externa.
- Não operar a esteira completa de NFS-e + boleto + remessa + e-mail como fluxo único sem pausas de validação.

## Revisão pré-produção 2026-06-30

Darth Vader registrou revisão segura do fluxo NFS-e + boleto + remessa antes de novo lote em produção. Veredito consolidado: não liberar automação direta da esteira completa; permitir apenas produção assistida, com travas por etapa.

Pontos críticos: cadastro do tomador deve usar identificador único quando houver ambiguidade; `seq_remessa`, `numero_documento` e `nosso_numero` não devem ser inferidos; e-mail externo depende de anexos conferidos e aprovação; upload no portal Cresol exige validação local da remessa e confirmação do Hebert.

## Cresol API, 2026-07-08/09

A skill `emitir-nfse-boleto-remessa` passou a prever a API de boletos Cresol como camada futura para registro de títulos oficiais, PDF oficial, consulta de status, alteração de vencimento e ocorrências.

Estado consolidado:

- Fase 1 documentada com guardrails, mantendo CNAB/remessa como fallback e auditoria.
- Fase 2 criou cliente CLI de homologação, com produção bloqueada por padrão e escrita exigindo `--allow-write`.
- Credenciais ficam somente em arquivo secreto local, fora do Brain/Git/snapshot.
- Testes de homologação validaram autenticação, parâmetros da conta, espécies, listagem de títulos, pagadores e sequenciais.
- Um título controlado de homologação foi criado com autorização explícita do Hebert; o PDF oficial foi baixado para conferência, mas payloads/respostas/PDFs permanecem fora do Git por serem artefatos de execução.

Pendências:

- Consultar evolução de status do título de homologação antes de usar ocorrências/conciliação.
- Confirmar mapeamento definitivo de juros/multa no payload produtivo: Bikon usa multa de 2,00% após vencimento e juros de 1% ao mês proporcional ao dia.

### Rodada homologacao 2026-08-11

Nova rodada Cresol API em homologacao criou o titulo `22394650` para teste BIKON:

- nosso numero: `09/00000000357-6`;
- valor: R$ 1,00;
- vencimento: 2026-08-18;
- status consultado: `EM_PROCESSAMENTO`;
- PDF oficial baixado via API, SHA-256 `7bb77b5480623ac7b0505a5fefbd0b977a0fb311b1e45ff21de7f8e99b309066`;
- remessa CNAB400 local `cb110857-titulo-22394650-homologacao.rem`, sequencial `2394650`, 3 linhas de 400 posicoes, tipos `0/1/9`, valor total R$ 1,00, validacao estrutural OK e SHA-256 `5602b5efeec58a1e033d2a77cee36644901d15b394ddcdf328848227c76ac2e8`;
- nenhum uso de producao, upload de remessa, baixa ou envio a cliente.

## BI financeiro Bikon, 2026-07-10/11

A workspace da Darth Vader passou a manter camada BI sobre o SQLite financeiro de boletos/NFS-e da Bikon, com views para:

- boletos;
- contas a receber;
- KPIs mensais;
- clientes;
- remessas;
- retornos.

Essa camada serve para consulta gerencial, relatório e conferência. Exports CSV gerados a partir dessas views são dados derivados/sensíveis e não devem ser versionados no Brain/Git.

Kowalski pode consultar a base em modo somente leitura para relatórios. Escrita, alteração de schema, importação de retorno, baixa, pagamento, NFS-e, boleto e remessa continuam exclusivamente com Darth Vader.

## Lote Bikon agosto/2026, remessa 093

Em 2026-08-03, Darth Vader executou produção assistida do lote agosto/2026:

- `27` NFS-e autorizadas em produção, com PDF/XML locais.
- `27` boletos gerados localmente e vinculados às NFS-e.
- `1` remessa CNAB400 local `remessa-093-010826-producao.rem`, SHA-256 `b4616a39ed4c89adb04bab60461c93e8df2dab33c022b4807210809592e56141`.
- Total do lote: R$ 86.357,06.
- `18` e-mails enviados, agrupados por cliente, todos com `financeiro@bikon.com.br` em cópia, status local `sent_all`.
- A remessa bancária foi preparada, mas não há registro consolidado de transmissão ao banco nesta etapa.

## Baseline FBCP, 2026-08-03

Foi concluída a Fase 0 read-only do FBCP com inventário, hashes, leitura SQLite immutable, mapa de mutações e riscos P0, sem chamada Notaas, Cresol, SMTP, remessa, emissão, boleto ou alteração operacional.

Riscos P0 que afetam a governança da Darth Vader:

- competência default fixa em partes da skill Notaas;
- valores tratados como `float` em CLI/helper/e-mail/CNAB;
- retry Notaas sem ledger idempotente;
- aprovação como flag booleana/reutilizável, sem manifest/hash de payload/anexos/destinatários;
- nosso número sem reserva transacional prévia;
- validador CNAB estrutural incompleto;
- envio SMTP sem outbox transacional/recibo forte;
- fronteira homologação/produção baseada em flags e nomes de pasta.

Próxima autorização recomendada: `AUTHORIZE_FBCP_P0_COMPETENCE_AND_MONEY_HARDENING_ONLY`.

## FIP Bikon Financial Intelligence, 2026-08-10/11

O FIP virou projeto financeiro proprio da BIKON e nao substitui a responsabilidade operacional da Darth Vader por NFS-e, boletos, remessas, baixas e comunicacao externa.

Estado consolidado:

- `FIP_PRODUCTION_GO_LIVE=PASS` em fronteira privada/controlada.
- Totais aceitos: receita canonica R$ 2.443.859,64, despesa R$ 1.418.140,88, resultado R$ 1.025.718,76; 2025 resultado R$ 812.106,17; 2026-current resultado R$ 213.612,59.
- `1438` transacoes bancarias canonicas, pendencias materiais `0`/R$ 0,00, backup/rollback `PASS`, validacao desktop/mobile `PASS`.
- App produtivo em `127.0.0.1:8787` com rota Tailscale tailnet-only, autenticacao obrigatoria e porta `9213` intocada.

Guardrail financeiro reforcado: o FIP separa caixa bruto de evento economico. Credito bancario, PIX, boleto ou cartao so entram no P&L aprovado com evidencia de natureza economica, competencia e vinculo suficiente; caso contrario ficam em clearing, settlement-only ou pendencia gerencial.

## FIP CHG-004, 2026-08-14/15

Darth Vader atuou como autoridade financeira/read-only em pontos de validacao do CHG-004. Estado consolidado:

- backend canonico 2026 aplicado no FIP com schema aditivo e sem substituir a responsabilidade operacional da Darth Vader por NFS-e, boletos, remessas, baixas e e-mails;
- fechamento estrutural `PASS`, com politica F N Souza/Felipe assumida por Bikon sob autoridade Hebert, Caju/folha/Cresol estruturados e FGTS/INSS/settlements parciais onde a fonte nao permitiu comparacao plena;
- carteira Cresol 2026 consolidada para consulta gerencial, com baixas manuais segregadas e sem caixa sintetico;
- Grupo Unus aceito por decisao humana com 8 CNPJs, sem inferencia por nome;
- cartoes pessoais Mercado Pago/Itau mantidos em quarentena privada; settlement ou prematch de reembolso nao autoriza classificacao economica automatica.

Risco residual observado: um evidence JSON de smoke registrou header de autenticacao. Isso nao altera o veredito financeiro, mas deve ser sanitizado em proxima janela aprovada.

## FIP/FCOC e Relatorios Operacionais, 2026-08-17/18

Darth Vader passou a atuar como worker interno em cenarios FIP solicitados pelo grupo Relatorios Operacionais, com Puppet Master como unico owner externo:

- active FCOC validado como `1.5.0 FROZEN`, com bootstrap/cold-start para compromissos de socios, clearing Felipe/Claude/notebook e regra de nao criar caixa sintetico;
- acesso ao backend FIP canonico `127.0.0.1:8787` validado em leitura/autenticacao, com app supervisionado por `fip-8787.service`;
- parecer do cenario Grupo Unus indicou consistencia aritmetica, sem erro material e baixo risco de dupla contagem se o valor reduzido R$ 24.000,00 substituir, e nao somar, os R$ 42.942,42 canonicos;
- em rotas do grupo, Darth nao deve usar `message` externo diretamente; resultado financeiro volta ao Puppet, que responde uma unica vez no Telegram.

## Relações

- `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- `BRAIN/70-AUTOMACOES/boletos-malote/README.md`
- `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
- `BRAIN/50-PROJETOS/Em-Andamento/FIP-Bikon-Financial-Intelligence.md`
