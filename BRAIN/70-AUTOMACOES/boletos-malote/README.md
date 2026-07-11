# Boletos e malote bancário

Backup e documentação da futura habilidade do Darth Vader para gerar remessa/malote bancário de boletos da Bikon.

Espelho operacional:
`/data/.openclaw/workspace-darth-vader/boletos`

## Estado em 2026-07-11

- Banco identificado nos modelos: Cresol, código 133.
- Há modelo de boleto e template CSV em `modelos/`.
- Há exemplos de remessa em `remessas/exemplos/`.
- A remessa `exemplo-malote-20260614-015740.rem` funciona como referência positiva inicial: header tipo `0`, detalhe tipo `1` e trailer tipo `9`.
- A remessa `exemplo-malote-20260614-0223-133_CNAB400_1008_27846.rem` funciona como referência negativa: possui duas linhas tipo `0`, não possui detalhe nem trailer e deve ser rejeitada por validações futuras.
- Há documentação sanitizada de retorno Cresol CNAB400 em `boletos/retornos/`, sincronizada no snapshot versionado da Darth Vader sem o arquivo `.ret` bruto.
- O retorno analisado confirma estrutura de 3 linhas de 400 posições, registros `0/1/9` e ocorrência `06` como liquidação, servindo apenas para parser/conciliação.
- Revisão pré-produção de 2026-06-30 confirmou que boleto/remessa podem ser preparados em produção assistida, mas não como esteira automática sem validação humana.
- Remessa de produção deve ser validada localmente antes de upload: linhas de 400 posições, CRLF, header `0`, detalhes `1`, trailer `9`, banco `133`, literal `REMESSA`, serviço `COBRANCA`, quantidade e valor total compatíveis com o lote.
- API Cresol entrou como camada futura complementar ao CNAB: homologação validada para autenticação, consultas e criação controlada de título de teste com autorização explícita; produção segue bloqueada.
- Artefatos de homologação da API, como payloads, respostas e PDFs oficiais baixados, devem ficar no workspace operacional da Darth Vader e não no Git do Brain.
- Em 2026-07-09, foi gerado pacote local de homologação Cresol com remessa CNAB400 validada e boleto PDF renderizado/conferido após correção do renderizador; nada foi enviado ao portal, por e-mail ou a cliente.
- Diretórios locais de homologação e ambientes virtuais (`homologacao-*`, `.venv-*`) foram classificados como artefatos de execução e excluídos dos snapshots versionados do Brain.
- Em 2026-07-10/11, o renderizador HTML do boleto Cresol recebeu ajuste específico para impedir corte do quinto bloco da linha digitável no Chromium, preservando o conteúdo calculado e reduzindo apenas fonte/largura quando necessário.
- Foi criada camada BI consultável sobre o SQLite financeiro da Darth Vader, com views de boletos, contas a receber, KPI mensal, clientes, remessas e retornos. Exports CSV continuam tratados como artefatos/dados derivados e não entram no Brain/Git.
- Kowalski tem acesso somente leitura à base financeira gerencial para relatórios e conferências; escrita, importação de retorno, baixa, NFS-e, boleto e remessa continuam sob responsabilidade da Darth Vader.

## Pendências antes de uso real

Confirmar com o banco/contrato:

1. layout oficial CNAB 240 ou CNAB 400;
2. convênio/código beneficiário definitivo;
3. regra do nosso número;
4. sequencial da remessa;
5. carteira/modalidade;
6. instruções aceitas pelo banco;
7. validação homologada antes de qualquer envio operacional;
8. controle aprovado de `seq_remessa`, `numero_documento` e `nosso_numero` antes de gerar arquivo de produção.
9. mapeamento final de juros/multa para API Cresol em produção, preservando a regra Bikon de multa de 2,00% e juros de 1% ao mês proporcional ao dia.
10. aprovação explícita do Hebert antes de upload no portal Cresol, envio ao banco, produção, baixa por API ou comunicação externa.
11. importar retornos Cresol no SQLite financeiro somente pela Darth Vader, com validação controlada antes de qualquer baixa operacional.

## Guardrail

Não usar os modelos para envio bancário real até concluir homologação com a Cresol e validar os campos obrigatórios do layout oficial.

Retorno `.ret` é referência de conciliação/liquidação, não de geração de remessa `.rem`; não usar retorno para inferir próximo nosso número, número de documento, sequencial de remessa ou regras de emissão.

Upload/envio no portal Cresol exige confirmação explícita do Hebert após validação local da remessa.

API Cresol em produção exige nova confirmação explícita do Hebert. Baixa por API permanece bloqueada até haver procedimento próprio, rollback e autorização específica.
