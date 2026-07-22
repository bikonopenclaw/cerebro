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
- Governança de acessos Bikon ↔ AD local de clientes: `BRAIN/70-AUTOMACOES/MATRIZ-ACESSO-BIKON-AD-CLIENTES.md`
- Integração Instagram Bikon Robotnik: `BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md`
- API WhatsApp Bikon: `BRAIN/70-AUTOMACOES/API-WHATSAPP-BIKON.md`
- Migração OpenClaw/Hostinger VPS: `BRAIN/50-PROJETOS/Planejamento/Migracao-Hostinger-VPS-OpenClaw.md`

## Histórico relevante

- 2026-07-20: conjunto Instagram Bikon v4 aprovado como canônico; cinco fundos Kling consumiram 10 créditos autorizados e nenhuma publicação ocorreu.
- 2026-07-20: Instagram Brand Director v2.1.0 implantada por corte atômico com backup, rollback e recibo append-only; Produção Assistida iniciada e lifecycle da proposta ainda `pending`.
- 2026-07-20: snapshot `feed-base-a v1` congelado com sete arquivos e Brand QA pré-geração `PASS`; manifesto `474e9af2…`, request `5d721862…` e payload `2be351a0…`. Render, Portão C, Kling e publicação permanecem bloqueados.
- 2026-07-20: SSI e SFT adotados como indicadores oficiais da Produção Assistida. Valores iniciais: SSI 50% e SFT 68,985 segundos.
- 2026-07-20: pacote conferido com 28 PDFs das NFS-e 191 a 218, total de R$ 88.403,87, entregue sem nova emissão ou cancelamento.
- 2026-07-17: aprovada a arquitetura de produção Instagram com Robotnik na preparação, Puppet Master na coordenação, Hebert nos portões de gasto/ação externa, Kling para mídia bruta, Creatomate para composição e Buffer como único publicador.
- 2026-07-17: contrato Kling CLI 0.1.3 limitado a `text_to_image`, adapter corrigido e nove testes aprovados sem geração ou consumo; brand pack oficial e template Creatomate 1080 × 1350 validados, com camadas produtivas e Buffer ainda pendentes.
- 2026-07-09: integração Instagram Bikon/Robotnik configurada em modo `draft` com Meta Graph API, token em segredo local, publicação bloqueada e crons editoriais criados para pautas diárias/semanais com aprovação humana.
- 2026-07-09: definido Kowalski como guardião visual de materiais públicos ou semi-públicos Bikon com arte/layout, enquanto Robotnik permanece dono de pauta, copy e campanha.
- 2026-07-09: pacote local de homologação Cresol gerado com remessa CNAB400 validada e boleto PDF conferido; nenhum upload no portal, envio ao banco ou e-mail externo foi feito.
- 2026-07-07: VPS de destino da migração OpenClaw foi limpa antes do replanejamento; manter arquitetura final com usuário `openclaw` como dono e sem resíduos de `root`, `u4s` ou gateway duplicado.
- 2026-06-26: API WhatsApp Bikon validada via `api.bikon.tech`, canal Atendimento Bikon registrado como `REGISTERED`, template `retomar_solicitacao` confirmado e rotina segura criada com token fora do Brain/Git.
- 2026-06-26: verificação de segurança da Meta aprovada para retomada da integração Instagram Bikon Robotnik; publicação real permanece bloqueada até configuração segura, testes e aprovação explícita.
- 2026-06-26: regra de faturamento atualizada para copiar `financeiro@bikon.com.br` em todo e-mail de NFS-e/boleto enviado a cliente.
- 2026-06-24: iniciada governança de acessos Bikon ↔ AD local de clientes, com matriz mestre em Google Sheets para listar usuários Bikon aprovados no Entra ID, clientes, servidores, permissões e regras de auditoria antes de qualquer automação.
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
- Todo e-mail de NFS-e/boleto enviado a cliente deve copiar `financeiro@bikon.com.br`.
- NFS-e da Bikon deve usar dados completos do tomador quando disponíveis no cadastro mestre, incluindo endereço completo.
- Qualquer geração de remessa bancária real deve ser validada contra layout oficial do banco antes de uso operacional.
- Qualquer chamada real à API GravityZone ou armazenamento de chave exige autorização explícita do Hebert e cofre local fora do Git.
- Qualquer automação sobre contas de AD local de clientes deve começar em modo auditoria; criação, desativação, remoção de grupos ou alteração de privilégio exige aprovação explícita e escopo validado.
- Relatórios técnicos externos devem sair com acabamento visual premium Bikon, sem caminhos internos, metadados automáticos, paginação feia ou aparência de HTML impresso.
- Materiais públicos ou semi-públicos com logo, paleta, layout ou identidade Bikon devem passar por revisão visual do Kowalski antes da peça final; isso não substitui aprovação explícita para publicação ou envio externo.
- No Instagram Bikon, briefing, estratégia, geração, composição/render e publicação são aprovações independentes. Buffer é o único publicador autorizado; Meta Graph API e Instagram direto não podem operar em paralelo.
- Brand QA pré-geração aprova somente o snapshot e o hash apresentados. Não autoriza Portão C, Kling, render, upload ou publicação; qualquer alteração de byte exige nova submissão.
