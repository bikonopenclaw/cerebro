# Darth Vader

```yaml
categoria: agente_operacional
fonte: sessões operacionais visíveis, configuração de skills em 2026-06-17 e snapshot versionado em 2026-07-11
confiabilidade: alta
ultima_revisao: 2026-07-11
tags: [agente, financeiro, faturamento, nfse, boleto, remessa, cresol-api]
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

## Relações

- `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- `BRAIN/70-AUTOMACOES/boletos-malote/README.md`
- `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
