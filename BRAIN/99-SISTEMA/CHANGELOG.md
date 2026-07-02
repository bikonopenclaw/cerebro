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

## 2026-06-26, API WhatsApp Bikon validada
- Criado workspace operacional `/data/.openclaw/workspace/api-bikon-whatsapp` para integração com `https://api.bikon.tech`.
- Swagger v2 enviado por Hebert salvo e indexado; client CLI local criado para canal, status, envio de texto/mídia, contatos, atendimentos e templates.
- Token do canal capturado via Google Drive temporário, salvo apenas em `secrets/.env`; documento temporário apagado após captura.
- Corrigido bloqueio Cloudflare 1010 adicionando User-Agent de navegador ao client.
- Canal validado: `Atendimento Bikon`, número `+55 (27) 3022-0499`, status `REGISTERED`.
- Template oficial WhatsApp Cloud `retomar_solicitacao (pt_BR)` validado com envio recebido por Hebert.
- Criada rotina segura `envio_seguro_template.py`, dry-run por padrão e envio real somente com `--confirm ENVIAR`.
- Snapshot sanitizado versionado em `BRAIN/70-AUTOMACOES/api-bikon-whatsapp/`, sem tokens, logs ou caches.

## 2026-06-27, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-27.md`.
- Atualizado `BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md` e `BRAIN/60-AGENTES/ROBOTNIK.md` com retomada pós-aprovação da verificação de segurança da Meta, mantendo token/IDs fora do Brain/Git e publicação bloqueada até aprovação explícita.
- Atualizado `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md` e `BRAIN/20-EMPRESAS/BIKON/README.md` com regra de cópia para `financeiro@bikon.com.br` em e-mails de NFS-e/boleto.
- Atualizado `BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md` com execução bem-sucedida observada em 2026-06-26.
- Atualizados `INDEX.md`, `HEALTH.md` e `STATUS-BRAIN.md`.
- Sincronizados snapshots versionados de Kowalski, Darth Vader e Robotnik antes da consolidação; o snapshot do Robotnik passou a incluir o status de retomada Instagram, e a configuração de e-mail da Darth Vader refletiu a cópia financeira padrão.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais, diffs Git e inspeção direta.
## 2026-06-28, consolidação semanal

- Criado resumo semanal `BRAIN/01-DIARIO/Semanal/2026-W26.md` cobrindo daily notes disponíveis de 2026-06-22 a 2026-06-28.
- Identificados padrões recorrentes: confirmação antes de impacto, segredos fora do Brain/Git, separação entre teste/rascunho/produção, governança antes de automação de identidade, retorno bancário não valida remessa, validação visual de relatórios externos e separação entre grupo permitido/remetente autorizado.
- Elevados aprendizados para notas permanentes em `BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md`, `BRAIN/40-CONHECIMENTO/Operacional/Governanca-antes-de-automacao-de-identidade.md`, `BRAIN/40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa.md`, `BRAIN/40-CONHECIMENTO/Operacional/Validacao-visual-de-relatorios-externos.md` e `BRAIN/40-CONHECIMENTO/Operacional/Canais-com-escopo-e-remetente-autorizados.md`.
- Reforçados os guardrails permanentes de confirmação antes de ações com impacto, segredos fora do Brain/Git e escopo de canais operacionais.
- Atualizados `INDEX.md`, `MEMORY.md` e `HEALTH.md`.
- Nenhum arquivamento realizado; registros recentes permanecem conectados e relevantes.

## 2026-06-30, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-30.md`.
- Atualizado `BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md` com execução bem-sucedida observada em 2026-06-29: 10 backups verificados, 3 ocorrências, 1 ticket criado, 2 tickets existentes reaproveitados e 0 erros.
- Atualizados `HEALTH.md` e `STATUS-BRAIN.md` para refletir a consolidação diária e a última execução ARX observada.
- Sincronizados snapshots versionados de Kowalski, Darth Vader e Robotnik antes da consolidação; o manifesto foi atualizado para 2026-06-30.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais, histórico Git e inspeção direta.

## 2026-07-01, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-07-01.md`.
- Sincronizados snapshots versionados de Kowalski, Darth Vader e Robotnik antes da consolidação; manifesto atualizado para 2026-07-01 e novo snapshot sanitizado da revisão pré-produção NFS-e/boleto/remessa da Darth Vader incluído.
- Atualizado `BRAIN/60-AGENTES/KOWALSKI.md` com regras de autoria/solicitante e padrão NinjaOne/EOL por máquina, separando cotação de hardware de ações internas de software.
- Atualizados `BRAIN/60-AGENTES/DARTH-VADER.md`, `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md` e `BRAIN/70-AUTOMACOES/boletos-malote/README.md` com revisão pré-produção: produção assistida, etapas cadenciadas, validação de cadastro/sequenciais/anexos e confirmação explícita antes de impactos fiscais, bancários ou comunicação externa.
- Atualizado `BRAIN/60-AGENTES/ROBOTNIK.md` para refletir o esclarecimento via Puppet Master quando brief vier incompleto.
- Atualizados `HEALTH.md` e `STATUS-BRAIN.md` para refletir a consolidação diária e os novos guardrails.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais, diffs Git e inspeção direta.

## 2026-07-01, consolidação mensal de junho/2026

- Criado resumo mensal `BRAIN/01-DIARIO/Mensal/2026-06.md` a partir dos resumos semanais `2026-W24`, `2026-W25`, `2026-W26` e do fechamento diário de 2026-06-30.
- Consolidados aprendizados de junho: Brain como memória, consolidação silenciosa, confirmação antes de impacto, segredos fora do Brain/Git, escopo de canais, dados mestres fiscais, separação teste/rascunho/produção, governança de identidade, retorno bancário versus remessa e validação visual de relatórios externos.
- Identificados padrões de longo prazo: Bikon como domínio operacional central, human-in-the-loop para impacto real, segurança por desenho, evidência local quando `memory_search` falha e elevação de conhecimento por recorrência.
- Atualizados `INDEX.md`, `MEMORY.md`, `HEALTH.md` e `STATUS-BRAIN.md` com a consolidação mensal e métricas.
- Nenhuma nota arquivada; registros de junho seguem recentes, conectados ou com valor de evidência.

## 2026-07-02, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-07-02.md`.
- Sincronizados snapshots versionados de Kowalski, Darth Vader e Robotnik antes da consolidação; manifesto atualizado para 2026-07-02.
- Atualizado `scripts/sync-agentes-versionados.py` para excluir diretórios temporários `tmp`, `tmp-*`, `tmp_*` e `temp` dos snapshots, evitando versionamento de artefatos de validação gerados.
- Atualizado `BRAIN/60-AGENTES/KOWALSKI.md` com guardrail para gerar PDFs externos sem cabeçalho/rodapé automático do Chromium/navegador e sem caminhos locais.
- Registrados no diário os aprendizados recentes sobre Notaas NFS-e/lote Remessa 092, relatórios externos e pacote Controle Financeiro Familiar, sem versionar dados brutos ou artefatos sensíveis.
- Registrada novamente a indisponibilidade de `memory_search` por quota insuficiente; revisão baseada em sessões visíveis, arquivos locais, diffs Git e inspeção direta.

## 2026-07-02, saneamento de skills e governança dos agentes

- Movido material `serpro-integra-parcelamentos` para standby no workspace do Darth Vader e refletido no snapshot seguro versionado.
- Removidos caches Python das skills vivas fora do Git, com backup pré-limpeza; Notaas NFS-e foi preservada estruturalmente por ser fluxo produtivo principal.
- Registrada correção de governança: Puppet Master coordena Kowalski, Darth Vader e Robotnik como agentes plenos, com interação agente-a-agente quando a tarefa cruzar escopos.
- Atualizado `scripts/sync-agentes-versionados.py` para excluir arquivos com `segredo/Segredo/SEGREDO` no nome, além de tokens, senhas, secrets e credenciais.

## 2026-07-02, skill padrão de relatórios Bikon e modelo EOL

- Criada a skill `padrao-relatorios-bikon` para o Kowalski, com checklist e validador de relatório Bikon.
- Atualizada a skill `ninjaone-relatorios` para usar obrigatoriamente o modelo EOL aprovado em relatórios de End of Life, fim de vida, substituição, obsolescência e cotação por parque.
- Registrado o PDF EOL corrigido do João Neiva, baseado no HTML/CSS real do Ferreira Rocha, como referência visual oficial no workspace do Kowalski.
- Mantida a regra de snapshot seguro: modelos binários aprovados ficam no workspace operacional e não entram no Brain Git quando cobertos por exclusão de `modelos-aprovados`.

## 2026-07-02, profundidade operacional nos agentes especialistas

- Atualizados Kowalski, Darth Vader e Robotnik para operar com Extreme Ownership, Anti-Sycophancy, Input Raso -> Deep Output, raciocínio estruturado sem CoT bruto e obsessão pelo objetivo.
- Kowalski passou a reforçar evidência, fonte, padrão Bikon e recomendação acionável.
- Darth Vader passou a reforçar segurança fiscal/financeira/bancária/técnica, validação, rollback e separação teste/produção.
- Robotnik passou a reforçar posicionamento, prova, CTA, recusa de marketês, promessa exagerada e exposição indevida.
