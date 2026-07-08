# INDEX.md

Mapa geral do Brain.

## Estrutura

- `00-INBOX`: entrada temporária de conhecimento.
- `01-DIARIO`: consolidação cronológica.
- `20-EMPRESAS`: conhecimento organizacional.
- `30-PESSOAS`: conhecimento relacional.
- `40-CONHECIMENTO`: biblioteca institucional.
- `50-PROJETOS`: iniciativas e projetos.
- `60-AGENTES`: documentação de agentes.
- `70-AUTOMACOES`: workflows e integrações.
- `80-DASHBOARDS`: indicadores consolidados.
- `99-SISTEMA`: regras, memória, índice, saúde e changelog.

## Registros ativos

- `01-DIARIO/2026/2026-06-12.md`: primeira consolidação diária do Brain.
- `01-DIARIO/2026/2026-06-13.md`: consolidação diária silenciosa sem novos registros permanentes.
- `01-DIARIO/2026/2026-06-16.md`: consolidação diária com centralização dos registros da BIKON e limitação de memória semântica registrada.
- `01-DIARIO/2026/2026-06-17.md`: consolidação diária sem novos registros permanentes, com limitação recorrente de memória semântica registrada.
- `01-DIARIO/2026/2026-06-18.md`: consolidação diária com registros dos contextos de faturamento Bikon/FN Souza e skill inicial FN Souza para Darth Vader.
- `01-DIARIO/2026/2026-06-19.md`: consolidação diária com diretriz de confirmação antes de ações com impacto e desenho inicial da integração GravityZone para Bikon.
- `01-DIARIO/2026/2026-06-20.md`: consolidação diária com padrão Bikon de tomador completo em NFS-e, relatório executivo Bitdefender e automação ARX Backup → NinjaOne.
- `01-DIARIO/2026/2026-06-22.md`: consolidação diária com e-mail automático NFS-e Bikon, SMTP fatura validado, agrupamento de notas por cliente, grupo Relatórios Operacionais/Kowalski e Whisper local como padrão.
- `01-DIARIO/2026/2026-06-23.md`: consolidação diária com padrão visual premium Bikon para relatórios técnicos externos e sincronização de snapshots versionados.
- `01-DIARIO/2026/2026-06-24.md`: consolidação diária com matriz de acesso Bikon ↔ AD local de clientes, execução ARX Backup → NinjaOne e sincronização de snapshots versionados.
- `01-DIARIO/2026/2026-06-25.md`: consolidação diária com remoção do contexto ativo FN Souza, execução ARX Backup → NinjaOne e sincronização de snapshots versionados.
- `01-DIARIO/2026/2026-06-26.md`: consolidação diária com correção operacional da rota Faturamento Bikon, retorno Cresol CNAB400 para parser/conciliação, execução ARX Backup → NinjaOne e sincronização de snapshots versionados.
- `01-DIARIO/2026/2026-06-27.md`: consolidação diária com API WhatsApp Bikon validada, retomada Instagram Robotnik pós-aprovação Meta, regra de cópia financeira em NFS-e/boleto e sincronização de snapshots versionados.
- `01-DIARIO/Semanal/2026-W24.md`: primeira consolidação semanal do Brain.
- `01-DIARIO/Semanal/2026-W25.md`: consolidação semanal com padrões de escopo de canais, confirmação antes de impacto, segredos fora do Brain/Git e dados mestres completos em automações fiscais.
- `01-DIARIO/Semanal/2026-W26.md`: consolidação semanal com padrões de segurança operacional antes de escala, teste/rascunho/produção, governança de identidade, retorno bancário versus remessa, relatórios externos e canais com remetente autorizado.
- `01-DIARIO/2026/2026-07-03.md`: consolidação diária com snapshots versionados, KPIs WhatsApp/Bitdefender, limitação de tickets NinjaOne, falhas por limite de uso e saneamento de PDFs/artefatos no Git.
- `01-DIARIO/2026/2026-07-08.md`: consolidação diária com limpeza pré-migração da VPS, riscos operacionais BIKON de 06/07/2026, atualização de snapshots e pendência de `memory_search`.
- `01-DIARIO/Mensal/2026-06.md`: consolidação mensal de junho/2026 com aprendizados consolidados, padrões de longo prazo, decisões e critério de não arquivamento por recência/conexão.
- `20-EMPRESAS/BIKON/README.md`: registro central da BIKON e conexões com automações fiscal, cadastro de clientes e boletos/malote.
- `20-EMPRESAS/BIKON/cadastro-clientes/README.md`: backup operacional de cadastro de clientes da BIKON.
- `40-CONHECIMENTO/IA/Brain-como-sistema-de-memoria.md`: princípio permanente de memória útil.
- `40-CONHECIMENTO/Operacional/Consolidacao-silenciosa-sem-ruido.md`: regra operacional para consolidar sem interrupção e sem ruído.
- `40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`: guardrail para avisar/confirmar antes de envios, alterações, criações ou execuções com impacto fora da conversa atual.
- `40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md`: aprendizado permanente sobre separar canais por finalidade, escopo, roteamento e guardrails.
- `40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md`: guardrail permanente para manter credenciais, tokens e dados sensíveis fora do Brain/Git.
- `40-CONHECIMENTO/Financeiro/Dados-mestres-completos-em-automacoes-fiscais.md`: princípio fiscal para preservar dados completos do cadastro mestre em payloads de NFS-e.
- `40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa.md`: princípio financeiro para não usar retorno CNAB400 como validação de remessa, nosso número ou sequencial.
- `40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md`: guardrail para separar preparo interno, dry-run e execução real.
- `40-CONHECIMENTO/Operacional/Governanca-antes-de-automacao-de-identidade.md`: aprendizado permanente para iniciar automações de identidade por matriz, auditoria e aprovação.
- `40-CONHECIMENTO/Operacional/Validacao-visual-de-relatorios-externos.md`: padrão de revisão visual para PDFs e pareceres externos.
- `40-CONHECIMENTO/Operacional/Canais-com-escopo-e-remetente-autorizados.md`: aprendizado sobre separar grupo/canal permitido de remetente autorizado.
- `50-PROJETOS/Em-Andamento/Brain-Enterprise.md`: registro permanente do projeto Brain Enterprise.
- `50-PROJETOS/Planejamento/Migracao-Hostinger-VPS-OpenClaw.md`: projeto de migração OpenClaw para VPS Hostinger com ambiente limpo, usuário `openclaw`, validação e rollback.
- `60-AGENTES/DARTH-VADER.md`: papel financeiro/fiscal do agente Darth Vader e skills relacionadas.
- `60-AGENTES/KOWALSKI.md`: papel de dados/relatórios do agente Kowalski, incluindo skill Provimento 213/2026, e uso controlado no grupo Relatórios Operacionais.
- `60-AGENTES/ROBOTNIK.md`: papel de marketing do agente Robotnik, status interno, guardrails e integração Instagram em retomada pós-aprovação Meta.
- `60-AGENTES/versionados/`: snapshots seguros de código, skills e documentação operacional do Kowalski, Darth Vader e Robotnik, com exclusão de segredos e artefatos gerados.
- `70-AUTOMACOES/CONSOLIDACAO-DIARIA-SILENCIOSA.md`: rotina diária silenciosa de consolidação.
- `70-AUTOMACOES/SYNC-GITHUB.md`: sincronização automática do Brain com GitHub 4x ao dia.
- `70-AUTOMACOES/NOTAAS-NFSE.md`: registro da skill Notaas NFS-e exclusiva da Darth Vader, com guardrails fiscais.
- `70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`: contexto ativo do grupo Telegram de faturamento Bikon e histórico inativo FN Souza, com roteamento para Darth Vader e guardrails.
- `70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM.md`: contexto do grupo Telegram de relatórios operacionais, com roteamento restrito para Kowalski.
- `70-AUTOMACOES/WHISPER-LOCAL.md`: instância local faster-whisper definida como padrão para transcrição de áudios.
- `70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md`: desenho inicial da integração GravityZone para segurança, inventário e relatórios da Bikon.
- `70-AUTOMACOES/MATRIZ-ACESSO-BIKON-AD-CLIENTES.md`: matriz mestre para governança e auditoria de usuários Bikon aprovados no Entra ID versus acessos em ADs locais de clientes.
- `70-AUTOMACOES/ARX-BACKUP-NINJAONE.md`: automação diária de monitoramento ARX Backup com deduplicação/criação de tickets NinjaOne.
- `70-AUTOMACOES/PROVIMENTO-213-2026-KOWALSKI.md`: skill e fluxo do Kowalski para diagnósticos técnicos de cartórios no Provimento CNJ 213/2026.
- `70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md`: integração Instagram Bikon com Robotnik via Meta Graph API, em retomada pós-aprovação de segurança da Meta.
- `70-AUTOMACOES/boletos-malote/README.md`: documentação da futura automação de boletos/remessa bancária da BIKON, com pendências de homologação Cresol.
- `70-AUTOMACOES/API-WHATSAPP-BIKON.md`: integração do canal oficial WhatsApp Bikon via api.bikon.tech, template `retomar_solicitacao`, rotina segura com dry-run e confirmação explícita.
- `70-AUTOMACOES/api-bikon-whatsapp/`: snapshot sanitizado do client local, Swagger, documentação e rotina segura, sem tokens.

## Arquivos de sistema

- `CONFIG.md`: regras operacionais do Brain.
- `FILOSOFIA.md`: princípios cognitivos e filosofia de funcionamento.
- `ROTINA-CONSOLIDACAO.md`: rotina diária de consolidação.
- `MEMORY.md`: memória institucional consolidada.
- `CHANGELOG.md`: histórico de alterações.
- `HEALTH.md`: saúde e métricas do Brain.

## Arquivo

- `99-ARQUIVO`: notas antigas, sem links fortes ou com baixa prioridade. Não é lixeira, é redução de visibilidade.
