# BIKON

## Identificação

- Nome operacional: Bikon
- Razão social registrada no contexto fiscal: Bikon Tecnologia da Informação Ltda Me
- CNPJ: 34.191.026/0001-86
- Inscrição Municipal: não usar como campo obrigatório na automação Notaas enquanto a API aceitar sem esse dado
- Cidade/UF: Vitória/ES
- Código IBGE: 3205309

## Relações no Brain

- Automação fiscal: `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- Cadastro de clientes: `BRAIN/20-EMPRESAS/BIKON/cadastro-clientes/`
- Boletos e malote bancário: `BRAIN/70-AUTOMACOES/boletos-malote/`
- Contexto de grupos de faturamento: `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
- Grupo relatórios operacionais: `BRAIN/70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM.md`
- Integração de segurança/antivírus em desenho: `BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md`

## Histórico relevante

- 2026-06-23: reforçado padrão visual premium Bikon para relatórios técnicos externos, com fundo suave dentro da paleta, sem cabeçalhos/rodapés automáticos e sem metadados de impressão/navegador.
- 2026-06-22: validado envio de e-mail NFS-e via `fatura@bikontecnologia.com.br`, template HTML padrão Bikon e agrupamento de duas ou mais NFS-e por cliente em um único e-mail com todos os PDFs/XMLs e boletos.
- 2026-06-22: criado grupo Telegram `relatórios operacionais` para consultas e relatórios do Kowalski, sem bot separado e sem alteração de estrutura operacional do agente.
- 2026-06-20: definido padrão operacional de NFS-e com tomador completo; quando o cadastro mestre tiver endereço, o payload Notaas deve incluir endereço completo e não apenas documento, nome e e-mail.
- 2026-06-19: gerado relatório executivo Bitdefender com 21 clientes, 785 licenças, 651 slots usados, 759 dispositivos, 647 gerenciados e 112 não gerenciados; caminhos registrados sem segredos.
- 2026-06-19: desenhada oportunidade de integração Bitdefender GravityZone para inventário, status de endpoints, incidentes e relatórios por cliente; sem credenciais registradas e sem execução externa.
- 2026-06-17: grupo Telegram `Faturamento Bikon` (`telegram:-5561224828`) restringido para tratar apenas de faturamento da Bikon: NFS-e, boletos, remessa/retorno e conferência cadastral diretamente ligada ao faturamento.
- 2026-06-12: skill Notaas NFS-e configurada para Bikon, com segredos mantidos fora do Brain/Git e emissão/cancelamento real protegidos por confirmação explícita.
- 2026-06-14: criado backup operacional de cadastro de clientes e documentação inicial para futura geração de boletos/remessa bancária.

## Guardrails

- Não registrar API keys, credenciais bancárias, tokens, arquivos sensíveis sem necessidade ou dados fiscais sigilosos no Brain.
- Qualquer emissão/cancelamento fiscal real exige autorização explícita do Hebert/Puppet Master.
- Qualquer envio externo de NFS-e, boleto ou e-mail financeiro para cliente exige aprovação explícita.
- NFS-e da Bikon deve usar dados completos do tomador quando disponíveis no cadastro mestre, incluindo endereço completo.
- Qualquer geração de remessa bancária real deve ser validada contra layout oficial do banco antes de uso operacional.
- Qualquer chamada real à API GravityZone ou armazenamento de chave exige autorização explícita do Hebert e cofre local fora do Git.

- Relatórios técnicos externos devem sair com acabamento visual premium Bikon, sem caminhos internos, metadados automáticos, paginação feia ou aparência de HTML impresso.
