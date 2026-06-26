# CHANGELOG.md

## 2026-06-12

- Criada estrutura Brain Enterprise v1.0.
- Criadas subpastas oficiais.
- Criados arquivos obrigatórios em `99-SISTEMA`.
- Registrada regra operacional em `CONFIG.md`.

## 2026-06-12, decisão arquitetural

- Confirmado que o Brain não será agente.
- Brain definido como repositório vivo de conhecimento.
- Puppet Master permanece responsável pela administração do Brain.
- Criada rotina diária de consolidação silenciosa.
- Criado dashboard inicial de status do Brain.

## 2026-06-12, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-12.md`.
- Registrada automação `BRAIN/70-AUTOMACOES/CONSOLIDACAO-DIARIA-SILENCIOSA.md`.
- Atualizados indicadores de saúde após criação da rotina e dashboard inicial.

## 2026-06-12, filosofia cognitiva

- Criado `BRAIN/99-SISTEMA/FILOSOFIA.md`.
- Registrados princípios: memória maior que armazenamento, contexto maior que fato, conhecimento conectado, relevância conquistada e esquecimento saudável.
- Criada pasta `BRAIN/99-ARQUIVO` para redução de prioridade sem apagar conhecimento.
- Atualizados `CONFIG.md`, `INDEX.md`, `ROTINA-CONSOLIDACAO.md` e `HEALTH.md`.

## 2026-06-12, sync GitHub 4x ao dia

- Criado script `scripts/sync-github.sh`.
- Script faz commit apenas quando há mudanças locais.
- Script envia `main` para `origin/main`.
- Automação programada para 06:00, 12:00, 18:00 e 23:00 BRT.

## 2026-06-12, skill Notaas NFS-e

- Auditada skill Notaas NFS-e v2.0.
- Corrigidos problemas de instalação, dry-run e frontmatter.
- Instalada skill em `/data/.openclaw/workspace/skills/notaas-nfse` e `/data/.openclaw/skills/notaas-nfse`.
- Registrados guardrails para impedir emissão/cancelamento fiscal sem confirmação explícita.
## 2026-06-12, configuração Notaas Bikon

- Configurada skill Notaas NFS-e para Bikon Tecnologia da Informação Ltda Me.
- Registrados apenas dados não sensíveis no Brain.
- API key mantida fora do Git, em arquivos locais com permissão 600.
- Validação realizada em modo dry-run, sem chamada real para API.
## 2026-06-12, exclusividade Notaas NFS-e

- Skill `notaas-nfse` restringida para uso exclusivo da Darth Vader.
- Removida dos diretórios globais/main.
- Mantida em `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse`.
- Validado que main e Kowalski não enxergam a skill, e Darth Vader enxerga.

## 2026-06-13, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-13.md`.
- Revisado contexto recente disponível; nenhuma sessão recente visível nem memória recuperável com conhecimento novo relevante.
- Mantidos registros permanentes sem novos arquivos para evitar ruído e duplicidade.

## 2026-06-14, consolidação semanal

- Criado resumo semanal `BRAIN/01-DIARIO/Semanal/2026-W24.md` cobrindo daily notes disponíveis de 2026-06-08 a 2026-06-14.
- Identificados padrões recorrentes: Brain como sistema de memória, consolidação silenciosa sem ruído e criação de notas apenas com utilidade futura.
- Elevados aprendizados para notas permanentes em `BRAIN/40-CONHECIMENTO/IA/Brain-como-sistema-de-memoria.md`, `BRAIN/40-CONHECIMENTO/Operacional/Consolidacao-silenciosa-sem-ruido.md` e `BRAIN/50-PROJETOS/Em-Andamento/Brain-Enterprise.md`.
- Nenhum arquivamento realizado; registros existentes permanecem recentes, conectados e relevantes.

## 2026-06-16, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-16.md`.
- Criado registro central `BRAIN/20-EMPRESAS/BIKON/README.md` para conectar informações já existentes da BIKON sem fragmentação.
- Atualizado `BRAIN/70-AUTOMACOES/boletos-malote/README.md` com estado, pendências de homologação Cresol e guardrail de não uso real sem validação.
- Atualizados `INDEX.md`, `HEALTH.md` e `STATUS-BRAIN.md` para refletir BIKON, boletos/malote e limitação temporária da busca semântica de memória.

## 2026-06-17, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-17.md`.
- Revisados arquivos locais do Brain, Inbox, `git status/log` e sessões visíveis; nenhum contexto recente externo recuperável foi encontrado.
- Mantidos registros permanentes sem novos arquivos para evitar ruído e duplicidade.
- Atualizados `INDEX.md`, `HEALTH.md`, `STATUS-BRAIN.md` e a automação de consolidação diária para refletir a execução e a recorrência da limitação de `memory_search`.

## 2026-06-18, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-18.md`.
- Criado `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md` para consolidar contextos dos grupos Telegram de faturamento Bikon e FN Souza.
- Criado `BRAIN/60-AGENTES/DARTH-VADER.md` documentando o papel financeiro/fiscal do agente e guardrails de execução.
- Atualizado `BRAIN/20-EMPRESAS/BIKON/README.md` com a restrição do grupo Faturamento Bikon.
- Atualizados `INDEX.md`, `HEALTH.md`, `STATUS-BRAIN.md` e a automação de consolidação diária.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais e histórico Git.

## 2026-06-19, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-19.md`.
- Criado `BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md` com desenho inicial da integração GravityZone para Bikon, sem credenciais e sem execução externa.
- Criado `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md` para registrar a diretriz de aviso/confirmação antes de ações com impacto fora da conversa atual.
- Atualizados `BIKON/README.md`, `FATURAMENTO-TELEGRAM.md`, `MEMORY.md`, `INDEX.md`, `HEALTH.md`, `STATUS-BRAIN.md` e a automação de consolidação diária.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais e histórico Git.
## 2026-06-20, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-20.md`.
- Atualizado `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md` com padrão Bikon de tomador completo e preservação de endereço.
- Atualizados `BRAIN/20-EMPRESAS/BIKON/README.md` e `BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md` com relatório executivo agregado Bitdefender de 2026-06-19.
- Criado `BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md` para registrar a automação diária ARX Backup → tickets NinjaOne.
- Atualizados `MEMORY.md`, `INDEX.md`, `HEALTH.md` e `STATUS-BRAIN.md`.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais e histórico Git.

## 2026-06-21, consolidação semanal

- Criado resumo semanal `BRAIN/01-DIARIO/Semanal/2026-W25.md` cobrindo daily notes disponíveis de 2026-06-15 a 2026-06-21.
- Identificados padrões recorrentes: escopo de canais operacionais, confirmação antes de ações com impacto, segredos fora do Brain/Git, dados mestres completos em automações fiscais e consolidação com evidência local quando `memory_search` está indisponível.
- Elevados aprendizados para notas permanentes em `BRAIN/40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md`, `BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md` e `BRAIN/40-CONHECIMENTO/Financeiro/Dados-mestres-completos-em-automacoes-fiscais.md`.
- Reforçado `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md` como padrão semanal recorrente.
- Atualizados `INDEX.md`, `MEMORY.md`, `HEALTH.md` e `STATUS-BRAIN.md`.
- Nenhum arquivamento realizado; registros recentes permanecem conectados e relevantes.
## 2026-06-22, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-22.md`.
- Atualizado `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md` com e-mail automático Bikon, SMTP fatura validado, template HTML, anexos PDF/XML/boleto e agrupamento de múltiplas NFS-e por cliente.
- Criado `BRAIN/60-AGENTES/KOWALSKI.md` e `BRAIN/70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM.md` para registrar o grupo de relatórios operacionais e o uso restrito do Kowalski.
- Criado `BRAIN/70-AUTOMACOES/WHISPER-LOCAL.md` para registrar faster-whisper local como padrão de transcrição de áudios.
- Atualizado `BRAIN/20-EMPRESAS/BIKON/README.md` com decisões de faturamento, relatórios operacionais e guardrails de envio externo.
- Atualizados `INDEX.md`, `HEALTH.md` e `STATUS-BRAIN.md`.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em arquivos locais, memória operacional e inspeção direta.
## 2026-06-22, versionamento de agentes

- Criado `BRAIN/60-AGENTES/versionados/` para versionar snapshots seguros do Kowalski e Darth Vader dentro do Git do Brain.
- Incluídos diretórios `agents/<agente>/agent` e recortes seguros dos workspaces operacionais dos agentes.
- Criado `scripts/sync-agentes-versionados.py` para atualizar os snapshots com exclusão de sessões, caches, `.env`, tokens, segredos, relatórios finais, binários pesados e artefatos gerados.
- Configuração real da Notaas foi substituída por `empresa.example.json`; exemplos `.env.example` mantidos apenas com placeholders.
- Atualizados `INDEX.md`, `HEALTH.md` e `STATUS-BRAIN.md`.
## 2026-06-23, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-23.md`.
- Atualizado `BRAIN/70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM.md` com padrão visual para relatórios externos Bikon.
- Atualizado `BRAIN/60-AGENTES/KOWALSKI.md` com responsabilidade de acabamento premium e validação visual de PDFs externos.
- Atualizado `BRAIN/20-EMPRESAS/BIKON/README.md` com padrão de relatórios técnicos externos.
- Sincronizados snapshots versionados de Kowalski e Darth Vader antes da consolidação.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais e inspeção direta.

## 2026-06-24, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-24.md`.
- Criado `BRAIN/70-AUTOMACOES/MATRIZ-ACESSO-BIKON-AD-CLIENTES.md` para registrar a governança de usuários Bikon aprovados no Entra ID versus acessos em ADs locais de clientes.
- Atualizado `BRAIN/20-EMPRESAS/BIKON/README.md` com relação, histórico e guardrail da matriz de acesso.
- Atualizado `BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md` com execução bem-sucedida observada em 2026-06-23.
- Atualizados `INDEX.md`, `HEALTH.md` e `STATUS-BRAIN.md`.
- Sincronizados snapshots versionados de Kowalski e Darth Vader antes da consolidação.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais, histórico Git e inspeção direta.

## 2026-06-25, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-25.md`.
- Atualizado `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md` para marcar FN Souza como contexto inativo/histórico e manter apenas Faturamento Bikon como grupo ativo.
- Atualizado `BRAIN/60-AGENTES/DARTH-VADER.md` para registrar `faturamento-fn-souza` como contexto removido do conjunto ativo.
- Atualizado `BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md` com execução bem-sucedida observada em 2026-06-24.
- Atualizados `INDEX.md`, `HEALTH.md` e `STATUS-BRAIN.md`.
- Sincronizados snapshots versionados de Kowalski e Darth Vader antes da consolidação; o snapshot refletiu a remoção da skill `faturamento-fn-souza` da Darth Vader.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais e inspeção direta.

## 2026-06-25, Robotnik e Provimento 213 no Brain/cron

- Criado `BRAIN/60-AGENTES/ROBOTNIK.md` documentando o novo agente interno de marketing, guardrails e status da integração Instagram.
- Criado `BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md` para registrar a integração via Meta Graph API, em stand by até aprovação de segurança da Meta.
- Criado `BRAIN/70-AUTOMACOES/PROVIMENTO-213-2026-KOWALSKI.md` para registrar a skill do Kowalski e o fluxo operacional de diagnóstico técnico de cartórios.
- Atualizado `scripts/sync-agentes-versionados.py` para incluir Robotnik nos snapshots seguros e reforçar exclusão de segredos/auth.
- Atualizado cron `Brain, consolidação diária silenciosa` para considerar Kowalski, Darth Vader e Robotnik nos snapshots versionados.
- Criado backup sanitizado `BRAIN/99-SISTEMA/openclaw-config-agentes-backup-2026-06-25.md` com os quatro agentes e allowlist agent-to-agent.
- Atualizados `INDEX.md`, `HEALTH.md`, `KOWALSKI.md` e `CONSOLIDACAO-DIARIA-SILENCIOSA.md`.

## 2026-06-26, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-26.md`.
- Atualizado `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md` com aprendizado operacional sobre `groupAllowFrom` e separação entre grupo permitido e remetente permitido.
- Atualizado `BRAIN/70-AUTOMACOES/boletos-malote/README.md` com retorno Cresol CNAB400 como referência sanitizada de parser/conciliação, sem autorizar uso como remessa.
- Atualizado `BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md` com execução bem-sucedida observada em 2026-06-25.
- Atualizados `INDEX.md`, `HEALTH.md`, `STATUS-BRAIN.md` e a automação de consolidação diária.
- Sincronizados snapshots versionados de Kowalski, Darth Vader e Robotnik antes da consolidação; o snapshot da Darth Vader passou a incluir documentação sanitizada de retornos Cresol, sem o `.ret` bruto.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais e inspeção direta.
