# BIKON

## Identificação

- Nome operacional: Bikon
- Razão social registrada no contexto fiscal: Bikon Tecnologia da Informação Ltda Me
- CNPJ: 34.191.026/0001-86
- Inscrição Municipal: 083712941
- Cidade/UF: Vitória/ES
- Código IBGE: 3205309

## Relações no Brain

- Automação fiscal: `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- Cadastro de clientes: `BRAIN/20-EMPRESAS/BIKON/cadastro-clientes/`
- Boletos e malote bancário: `BRAIN/70-AUTOMACOES/boletos-malote/`
- Contexto de grupos de faturamento: `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
- Integração de segurança/antivírus em desenho: `BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md`

## Histórico relevante

- 2026-06-19: desenhada oportunidade de integração Bitdefender GravityZone para inventário, status de endpoints, incidentes e relatórios por cliente; sem credenciais registradas e sem execução externa.
- 2026-06-17: grupo Telegram `Faturamento Bikon` (`telegram:-5561224828`) restringido para tratar apenas de faturamento da Bikon: NFS-e, boletos, remessa/retorno e conferência cadastral diretamente ligada ao faturamento.
- 2026-06-12: skill Notaas NFS-e configurada para Bikon, com segredos mantidos fora do Brain/Git e emissão/cancelamento real protegidos por confirmação explícita.
- 2026-06-14: criado backup operacional de cadastro de clientes e documentação inicial para futura geração de boletos/remessa bancária.

## Guardrails

- Não registrar API keys, credenciais bancárias, tokens, arquivos sensíveis sem necessidade ou dados fiscais sigilosos no Brain.
- Qualquer emissão/cancelamento fiscal real exige autorização explícita do Hebert/Puppet Master.
- Qualquer geração de remessa bancária real deve ser validada contra layout oficial do banco antes de uso operacional.
- Qualquer chamada real à API GravityZone ou armazenamento de chave exige autorização explícita do Hebert e cofre local fora do Git.
