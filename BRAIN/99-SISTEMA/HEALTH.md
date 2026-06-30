# HEALTH.md

Health Score: 95/100

## Status atual

- Estrutura principal criada.
- Arquivos obrigatórios criados.
- Sem registros duplicados identificados.
- Sem projetos abandonados identificados.
- Rotina de consolidação diária registrada e executada em 2026-06-13, 2026-06-16, 2026-06-17, 2026-06-18, 2026-06-19, 2026-06-20, 2026-06-22, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26, 2026-06-27 e 2026-06-30.
- Consolidações semanais executadas em 2026-06-14 (`01-DIARIO/Semanal/2026-W24.md`), 2026-06-21 (`01-DIARIO/Semanal/2026-W25.md`) e 2026-06-28 (`01-DIARIO/Semanal/2026-W26.md`).
- Aprendizados elevados para notas permanentes conectadas em `40-CONHECIMENTO` e `50-PROJETOS`, incluindo escopo de canais, segredos fora do Brain/Git, dados mestres completos em automações fiscais, separação teste/rascunho/produção, governança de identidade, retorno bancário versus remessa e validação visual de relatórios externos.
- Registro central da BIKON criado e conectado a Notaas NFS-e, cadastro de clientes e boletos/malote.
- Dashboard inicial atualizado.
- Automações registradas: consolidação diária silenciosa, sync GitHub, Notaas NFS-e exclusiva da Darth Vader, documentação inicial de boletos/malote da BIKON com retorno Cresol CNAB400 para parser/conciliação, contexto ativo do grupo Telegram de faturamento Bikon, histórico inativo FN Souza, desenho inicial GravityZone para Bikon, matriz de acesso Bikon ↔ AD local de clientes, ARX Backup diário para tickets NinjaOne, Provimento 213/2026 Kowalski, Instagram Bikon Robotnik em retomada pós-aprovação Meta e API WhatsApp Bikon validada.
- Contexto do grupo Telegram de faturamento Bikon registrado com escopo, roteamento e guardrails; contexto FN Souza mantido apenas como histórico inativo desde 2026-06-25.
- Agente Darth Vader documentado como executor financeiro/fiscal relacionado a NFS-e, boletos e remessas.
- Diretriz operacional registrada para confirmação antes de ações com impacto fora da conversa atual.
- Guardrail permanente registrado para manter segredos, tokens e inventários sensíveis fora do Brain/Git.
- Princípio financeiro/fiscal registrado para preservar dados mestres completos nos payloads de NFS-e.
- Fluxo de e-mail NFS-e Bikon registrado com SMTP validado, template HTML, anexos obrigatórios e agrupamento por cliente.
- Agente Kowalski, grupo Relatórios Operacionais e skill Provimento 213/2026 documentados.
- Whisper local documentado como padrão de transcrição.
- Padrão visual premium Bikon para relatórios técnicos externos registrado.
- Governança inicial de acessos Bikon ↔ AD local de clientes registrada com fase 1 restrita a auditoria.
- Agentes Kowalski, Darth Vader e Robotnik documentados.
- Snapshots versionados dos agentes Kowalski, Darth Vader e Robotnik criados em `60-AGENTES/versionados/`, com política de exclusão de segredos e artefatos.

## Pendências

- Manter cobertura diária consistente; há lacunas de diário em 2026-06-14/15, apesar da consolidação semanal de 2026-06-14.
- Restaurar ou trocar o provedor de embeddings: `memory_search` falhou em 2026-06-16, 2026-06-17, 2026-06-18, 2026-06-19, 2026-06-20, 2026-06-22, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26, 2026-06-27 e 2026-06-30 por quota insuficiente.
- Homologar layout Cresol antes de qualquer uso real da automação de boletos/malote; retorno `.ret` validado deve permanecer restrito a parser/conciliação.
- Concluir configuração segura da integração Instagram Bikon Robotnik: token Meta de longa duração, IDs da Página/Instagram Business Account e testes `me`/`pages`, mantendo publicação bloqueada até aprovação explícita.
- Expandir dashboards conforme surgirem projetos, empresas, pessoas e automações reais.

## Filosofia cognitiva

- Filosofia oficial registrada em `FILOSOFIA.md`.
- Métricas de saúde definidas.
- Esquecimento saudável definido via `99-ARQUIVO`.
- Rotinas diária, semanal e mensal especificadas.
- API WhatsApp Bikon validada com canal oficial Meta/WhatsApp Cloud, template `retomar_solicitacao` e rotina segura com confirmação explícita. Consolidação semanal 2026-W26 concluída sem arquivamento por baixa relevância.
