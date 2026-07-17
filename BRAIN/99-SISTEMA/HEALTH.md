# HEALTH.md

Health Score: 94/100

## Status atual

- Estrutura principal criada.
- Arquivos obrigatórios criados.
- Sem registros duplicados identificados.
- Sem projetos abandonados identificados.
- Rotina de consolidação diária registrada e executada em 2026-06-13, 2026-06-16, 2026-06-17, 2026-06-18, 2026-06-19, 2026-06-20, 2026-06-22, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26, 2026-06-27, 2026-06-30, 2026-07-01, 2026-07-02, 2026-07-03, 2026-07-06, 2026-07-07, 2026-07-08, 2026-07-09, 2026-07-10, 2026-07-11, 2026-07-14, 2026-07-15 e 2026-07-17.
- Consolidações semanais executadas em 2026-06-14 (`01-DIARIO/Semanal/2026-W24.md`), 2026-06-21 (`01-DIARIO/Semanal/2026-W25.md`), 2026-06-28 (`01-DIARIO/Semanal/2026-W26.md`), 2026-07-12 (`01-DIARIO/Semanal/2026-W28.md`) e revisão parcial até 2026-07-17 (`01-DIARIO/Semanal/2026-W29.md`).
- Consolidação mensal executada em 2026-07-01 (`01-DIARIO/Mensal/2026-06.md`), cobrindo junho/2026.
- Aprendizados elevados para notas permanentes conectadas em `40-CONHECIMENTO` e `50-PROJETOS`, incluindo escopo de canais, segredos fora do Brain/Git, dados mestres completos em automações fiscais, separação teste/rascunho/produção, governança de identidade, retorno bancário versus remessa, validação visual de relatórios externos, artefatos gerados fora do Brain/Git, ausência de evidência em monitoramento, separação entre consulta gerencial e permissão operacional, homologação bancária sem produção automática, validação do runtime pós-migração e menor privilégio em monitoramento.
- Sentinel documentado como controller de Operações e SNOC read-only, com fontes autorizadas, allowlists, auditoria append-only, limites e revogação verificável.
- Instagram Bikon documentado com aprovações separadas por etapa e hash, Kling restrita à geração, Creatomate à composição e Buffer como único publicador.
- Registro central da BIKON criado e conectado a Notaas NFS-e, cadastro de clientes e boletos/malote.
- Dashboard inicial atualizado.
- Automações registradas: consolidação diária silenciosa, sync GitHub, Notaas NFS-e exclusiva da Darth Vader, documentação inicial de boletos/malote da BIKON com retorno Cresol CNAB400 para parser/conciliação, Cresol em homologação controlada com pacote local validado e sem envio externo, contexto ativo do grupo Telegram de faturamento Bikon, histórico inativo FN Souza, GravityZone/Bitdefender para Bikon com evolução aprovada para tickets NinjaOne sob critérios de alta confiança, matriz de acesso Bikon ↔ AD local de clientes, ARX Backup diário para tickets NinjaOne, limitações NinjaOne para backup/Hyper-V quando não há job/campo explícito, Provimento 213/2026 Kowalski, canal Telegram isolado do Kowalski para Relatórios Operacionais, Instagram Bikon Robotnik configurado em modo `draft` com crons editoriais e API WhatsApp Bikon validada; projeto de migração Hostinger VPS/OpenClaw em validação.
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
- Agentes Kowalski, Darth Vader e Robotnik documentados; Kowalski atualizado com padrão NinjaOne/EOL, autoria/solicitante, canal Telegram isolado e guardião visual Bikon; Darth Vader atualizado com revisão pré-produção de NFS-e/boleto/remessa e Cresol API em homologação; Robotnik atualizado com Instagram em `draft`, crons editoriais e revisão visual via Kowalski para peças finais.
- `Modelo de Relatório EOL Bikon` aprovado como padrão oficial para próximos relatórios EOL; PDFs finais e artefatos gerados permanecem fora do Brain/Git.
- Claw3D/OpenClaw na VPS validado em 2026-07-13 com gateway conectado e ajuste para `openclaw-ground`; pendente confirmação visual do Hebert pelo túnel SSH.
- Em 2026-07-15, a Fase 1 de saneamento liberou aproximadamente 7,1 GiB e reduziu o uso do disco para 38%; skills específicas foram reposicionadas para os workspaces ativos e o scheduler voltou a enxergar 33 jobs habilitados.
- Snapshots versionados dos agentes Kowalski, Darth Vader e Robotnik criados em `60-AGENTES/versionados/`, com política de exclusão de segredos, artefatos, diretórios temporários e dados brutos sensíveis; em 2026-07-03 o Git do Brain passou a ignorar PDFs, imagens, ZIPs, sessões, caches e artefatos binários gerados por padrão; em 2026-07-09 a rotina passou a excluir também bancos locais, WAL/SHM, estado OpenClaw e artefatos de homologação da API Cresol; em 2026-07-10 a rotina passou a excluir prefixos `.venv-*` e `homologacao-*`; em 2026-07-11 passou a excluir `exports/`, `drafts/`, `*.csv` e `*.svg`; em 2026-W28 esse padrão foi elevado para nota permanente.

## Pendências

- Manter cobertura diária consistente; há lacunas de diário em 2026-06-14/15, apesar da consolidação semanal de 2026-06-14.
- Manter explícitas as lacunas recentes de daily notes em 2026-07-12, 2026-07-13 e 2026-07-16; a semana 2026-W29 usou histórico Git apenas como evidência complementar até a criação do diário de 2026-07-17.
- Restaurar, reindexar ou trocar o provedor de embeddings: `memory_search` falhou em 2026-06-16, 2026-06-17, 2026-06-18, 2026-06-19, 2026-06-20, 2026-06-22, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26, 2026-06-27, 2026-06-30, 2026-07-01, 2026-07-02, 2026-07-03, 2026-07-07 e 2026-07-08 por quota insuficiente/billing inativo; em 2026-07-10 retornou índice sem metadata/incompatível com o provedor/modelo atual.
- Homologar layout Cresol antes de qualquer uso real da automação de boletos/malote; retorno `.ret` validado deve permanecer restrito a parser/conciliação.
- Consultar evolução do título controlado de homologação Cresol antes de avançar ocorrências/conciliação por API; produção e baixa por API seguem bloqueadas.
- Fechar camadas do master Creatomate, `template-map`, credencial ativa no runtime, Buffer e preflight antes de liberar o piloto Instagram; geração, render e publicação seguem bloqueados por portões próprios.
- Validar endpoint/permissão oficial de listagem de tickets no NinjaOne; sem isso, KPIs completos de tickets devem permanecer como indisponíveis, não estimados.
- Instrumentar no NinjaOne, quando necessário, status explícito de backup e replicação Hyper-V para servidores de clientes que não expõem esses dados por jobs, alertas, atividades ou custom fields.
- Observar o canal isolado do Kowalski no Telegram e ajustar roteamento se houver resposta fora de escopo, latência anormal ou duplicidade com Puppet Master.
- Acompanhar produção Bitdefender -> NinjaOne: confirmar que tickets reais respeitam critérios de alta confiança, recência de 30 dias, ausência de máquina inativa e auto-fechamento só por nova coleta.
- Confirmar visualmente o Claw3D/OpenClaw pelo acesso do Hebert e manter rollback documentado.
- Concluir a análise de causa-raiz dos travamentos/restarts da VPS e revalidar os 11 jobs cujo último status ficou em erro após interrupção, timeout ou aborto em 2026-07-15; manter a Fase 2 de saneamento suspensa até fechar a recuperação.
- Expandir dashboards conforme surgirem projetos, empresas, pessoas e automações reais.

## Filosofia cognitiva

- Filosofia oficial registrada em `FILOSOFIA.md`.
- Métricas de saúde definidas.
- Esquecimento saudável definido via `99-ARQUIVO`.
- Rotinas diária, semanal e mensal especificadas.
- API WhatsApp Bikon validada com canal oficial Meta/WhatsApp Cloud, template `retomar_solicitacao` e rotina segura com confirmação explícita. Consolidação semanal 2026-W26 concluída sem arquivamento por baixa relevância.
- Consolidação semanal 2026-W28 concluída sem arquivamento por baixa relevância; registros recentes permanecem conectados e operacionais.
- Consolidação parcial 2026-W29 concluída sem arquivamento; registros recentes permanecem conectados e com valor operacional ou de auditoria.


## Métricas — 2026-07-01

- Daily notes de junho: 14 arquivos, com cobertura parcial porque o Brain iniciou em 2026-06-12 e houve lacunas.
- Resumos semanais de junho revisados: 3 (`2026-W24`, `2026-W25`, `2026-W26`).
- Resumos mensais: 1 (`01-DIARIO/Mensal/2026-06.md`).
- Notas permanentes de conhecimento elevadas em junho: 11 principais, cobrindo IA/memória, operação e financeiro.
- Arquivos em `99-ARQUIVO`: 0; nenhum arquivamento mensal porque os registros seguem recentes, conectados ou com valor de evidência.
- MOCs/índices atualizados no mês: `INDEX.md`, `MEMORY.md`, `STATUS-BRAIN.md` e este `HEALTH.md`.
- Pontos que reduzem score: cobertura diária parcial e `memory_search` indisponível por quota insuficiente.
