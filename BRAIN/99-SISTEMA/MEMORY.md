# MEMORY.md

Memória institucional consolidada do Brain.

## Diretrizes permanentes

- O Agente Principal administra o Brain.
- O Brain é patrimônio intelectual acumulado.
- O Brain é a fonte de verdade para classificar e armazenar memórias importantes; memória operacional do OpenClaw é apoio de busca/recall, não substitui curadoria do Brain.
- Registrar apenas informação com utilidade futura.
- Evitar duplicidade antes de criar novos registros.
- Relacionar pessoas, empresas, projetos e conhecimento sempre que possível.
- Consolidar periodicamente, sem atrapalhar a execução do dia.
- Antes de ações que enviem, alterem, criem ou executem algo fora da conversa atual, avisar Hebert e confirmar quando o impacto não estiver previamente autorizado; rotinas silenciosas já autorizadas seguem suas próprias restrições.
- Para NFS-e da Bikon, usar todos os dados disponíveis do cadastro mestre no tomador; se houver endereço, incluir endereço completo. Se o endereço estiver ausente ou ambíguo, tratar como pendência antes da emissão.
- Para e-mails de NFS-e da Bikon, usar `fatura@bikontecnologia.com.br`, template HTML padrão Bikon e anexar DANFSe PDF, XML e boleto PDF quando houver boleto.
- Em lotes de NFS-e, se houver duas ou mais notas para o mesmo ID/documento de cliente, agrupar em um único e-mail por cliente com todos os documentos e boletos anexados.
- Áudios devem ser transcritos primeiro pela instância local faster-whisper; API externa só quando Hebert pedir ou quando a rota local falhar de forma não recuperável.
- Manter API keys, tokens, senhas, `.env`, inventários sensíveis e respostas detalhadas de APIs fora do Brain/Git; registrar apenas arquitetura, escopo, guardrails e métricas agregadas quando útil.
- Canais operacionais devem ter escopo, fora de escopo, roteamento e guardrails explícitos para evitar mistura de assuntos e execução no contexto errado.
- Quando Hebert pedir correção pontual em arte/design/arquivo, preservar a base aprovada e alterar apenas o elemento solicitado, salvo pedido explícito de redesenho amplo.
- Separar teste, rascunho e produção em automações externas: dry-run e preparo interno podem avançar, mas envio, publicação, emissão, remessa ou alteração real exigem confirmação quando houver impacto externo.
- Em testes com dados reais, usar destinatário explícito e impedir lookup automático que possa enviar informação a terceiros.
- Em governança de identidade BIKON ↔ AD local de clientes, começar por auditoria e matriz aprovada; não criar, desativar ou alterar contas/grupos sem validação humana.
- Retorno bancário CNAB400 serve para parser/conciliação quando sanitizado, mas não valida remessa, nosso número, documento ou sequencial.
- Relatórios externos devem ser revisados visualmente antes da entrega, removendo metadados de navegador, cabeçalhos/rodapés automáticos e aparência de HTML impresso.
- Relatórios EOL devem usar o `Modelo de Relatório EOL Bikon`; software EOL vira ação interna Bikon, compra física entra apenas quando houver hardware classificado para substituição, e PDFs finais não entram no Brain/Git.
- Em canais operacionais, grupo permitido e remetente autorizado são dimensões diferentes; `groupAllowFrom` deve representar remetente autorizado.
- Artefatos gerados por execução, homologação, exportação ou rascunho devem ficar fora do Brain/Git; registrar apenas decisões, estado sanitizado e guardrails.
- Ausência de evidência consultável em ferramenta operacional não deve ser interpretada como sucesso nem falha confirmada; quando o dado for necessário, instrumentar coleta explícita.
- Acesso financeiro somente leitura para relatório ou BI não concede permissão operacional para escrita, baixa, emissão, boleto, remessa, retorno ou comunicação externa.
- Homologação bancária, API funcional, boleto renderizado ou pacote local validado não autorizam produção, upload, baixa ou envio externo sem aprovação explícita e procedimento próprio.
- Promessa de retorno sem resposta imediata deve gerar follow-up agendado no Telegram antes de encerrar a interação.
- Bitdefender -> NinjaOne só deve abrir ticket real para critérios aprovados de alta confiança; endpoint sem proteção exige recência inferior a 30 dias, e auto-fechamento depende de nova coleta confirmando resolução.
- Após migração ou upgrade, arquivos presentes não comprovam runtime recuperado; validar rotas ativas, skills indexadas, scheduler, `nextWake`, execuções, supervisor, canais e persistência após restart controlado.
- Upgrade/plugin, modelo/configuração, porta, restart e recuperação de backlog são categorias distintas e devem passar por gates separados.
- Agentes de monitoramento devem operar com menor privilégio: clientes read-only, allowlists, saída sanitizada, auditoria append-only e revogação verificável. Credencial compartilhada ampla continua sendo limitação explícita.
- Evidência operacional precisa de fonte, timestamp e recência adequada. Abertura automática exige sinal atual; encerramento exige nova coleta que confirme resolução.
- Deploy de skill exige plano imutável, algoritmo de hash nomeado, staging no mesmo filesystem, backup verificado, troca atômica, rollback e recibo append-only. Divergência de hash ou validator interrompe a janela sem fallback silencioso.
- Na Produção Assistida, Brand QA aprova somente o snapshot e o hash apresentados. Portão C, geração, composição e publicação permanecem autorizações separadas.
- `SSI` mede snapshots aprovados na primeira submissão sobre o total submetido ao Brand QA. `SFT` mede o tempo do início do congelamento até duas leituras consecutivas idênticas do manifesto canônico.
- Antes de selecionar um modelo, aplicar o Gate D0: se a tarefa inteira tiver procedimento determinístico e resultado objetivo, usar ferramenta, script ou validador sem LLM no caminho feliz; qualquer divergência volta ao roteador.
- Troca de modelo ou nível de pensamento nunca amplia autorização. Produção, root, gasto, comunicação externa, mudança real, risco financeiro, backup e rollback continuam sujeitos aos gates vigentes.
- `Ultra` é perfil de paralelismo e só deve ser avaliado quando houver duas ou mais frentes independentes, ganho real e critério de pronto objetivo.
- O Roteador de Execução v1 está congelado na Etapa 0. Spark, troca automática de modelo e Etapas 1 a 4 permanecem não autorizados até nova decisão do Hebert.
- Autorização operacional é atomica: approval, checkpoint, commit, hash, validação independente e publicação comprovam somente o escopo exato da unidade autorizada.
- Runtime operacional precisa de contrato reproduzível: caminho absoluto, versão final, origem, checksums, arquitetura, Unicode quando aplicável e regra de drift.
- Documento `PROPOSED_NOT_FROZEN` ou `PROPOSED_PENDING_INDEPENDENT_VALIDATION` preserva contexto, mas não é contrato canônico nem autorização operacional.
- Capacidade técnica oficial de provider não substitui evidência local de conta, tenant, subscription, projeto, owner aprovado, permissão e trilha de auditoria.
- Disponibilidade isolada de provider também não prova aplicabilidade; pergunta ou ação específica de AWS/Azure/GCP só é elegível quando o provider já foi selecionado, mandatado por arquitetura aprovada, exigido por controle regulatório aplicável ou necessário para dependência operacional já aprovada.
- Commit de estado, AIR, ICD, journal ou manifesto `PASS` nao equivalem a aceitacao operacional; rota autenticada, dashboard, PDF, token e runtime final precisam ser validados em gate proprio.
- Leitura read-only precisa provar nao mutacao persistida; se uma rota de validacao altera estado canonico ou controle comparativo, a aceitacao deve falhar fechado.
- Teste pre-install ou commit preservado não comprova ferramenta instalada; o caminho final usado pelo operador precisa passar em validação black-box.
- Em esteira fiscal/financeira Bikon, competência deve ser explícita por operação e dinheiro deve trafegar como Decimal/centavos; `float`, default fixo de competência e aprovação booleana reutilizável são riscos P0.
- Em P&L BIKON/FIP, caixa bruto nao prova natureza economica: credito bancario, PIX, boleto, cartao ou recorrencia so entram no resultado aprovado com vinculo suficiente a cliente, contrato, titulo, NFS-e, fatura, competencia, decisao humana ou evidencia equivalente.
- FIP em producao privada nao concede permissao operacional fiscal/bancaria: dashboards, forecasts e cenarios nao autorizam emissao, boleto, remessa, baixa, envio externo ou alteracao de fonte sem Approval proprio.
- Em forecast FIP, cobertura documental parcial nao deve ser maquiada como confianca total: quando entradas/saidas materiais nao atingirem o alvo de evidencia, promover apenas como candidato/partial pass e listar os gaps por materialidade.
- Em Mini App Telegram operacional, bootstrap deve validar `initData`, identidade autorizada e launch context assinado antes de carregar estado canonico; cliente deve tratar erro estruturado e resposta nao JSON sem cair em `ERROR` opaco.
- Executor controlado de segredo ODP precisa validar o conjunto congelado completo no caminho final; binario, sudoers e preflight autenticado nao bastam se contrato, hashes, dono/modo ou manifest final estiverem ausentes.
- Contagem nao e percentual de conclusao: evidencias, conformidade, remediacao ou inventario sem denominador canonico devem ser renderizados como contagens/distribuicoes ou itens em reconciliacao, nunca como `100%` por usar a propria contagem como denominador.
- Verdade canonica exige materializacao e reconciliacao por fonte quando ha corpus historico, runtime atual e extras pos-checkpoint; inventario de paths presentes nao basta para Golden Baseline.
- Segunda-feira dos relatórios operacionais usa fechamento semanal coletado no sábado; não forçar job diário quando não existir coleta/cache diário correspondente.
- Brain v2 possui Commit Link Gate local aceito desde o commit `153129b52ae093c42bb106006de18b78a7ab7dbe`: validar `0` links internos quebrados, `0` markdown uncategorized, ausência de duplicate IDs/aliases e ausência de novos candidatos a segredo antes de tratar uma mudança como saudável.
- A fundação Brain v2 e a reintegração inicial não autorizam edição manual no Obsidian nem sync amplo sem gate; se o vault remoto precisar atualizar, puxar o commit canônico em vez de alterar notas à mão.
- A separação operacional canonica dos relatórios Bikon é Sentinel coletar/consultar fontes operacionais e Kowalski interpretar os dados consolidados para produzir relatórios no padrão Bikon.
- Delegacao de engenharia com escrita exige boundary persistido: writable roots explicitos por tarefa, validacao antes/depois e fail-closed para qualquer arquivo, diretorio, cache ou artefato fora do escopo autorizado.
- Delegacao read-only validada nao herda autorizacao de escrita; schema, runtime, sandbox, validators e enforcement precisam de ramo proprio para a classe de tarefa.
- Em ODP, PostgreSQL operacional deve permanecer separado de SQLite/OpenClaw e de migracoes Provimento 213 ate gates proprios; erratas de baseline aceito devem ser aditivas, limitadas e rastreaveis.

## Padrões consolidados mensalmente

- Padrão mensal de junho/2026: segurança operacional antes de escala; automações podem preparar e validar, mas impactos fiscais, bancários, comunicacionais, publicações e alterações de identidade exigem confirmação explícita quando não autorizados previamente.
- Padrão mensal de julho/2026: prova antes de continuidade; status operacional exige evidência recente e rota ativa validada, enquanto publicação, envio, baixa, deploy, restore, provider, target e recorrência permanecem separados por Approval granular.
- Padrão semanal 2026-W28: maturidade operacional antes de escala; snapshots seguros excluem artefatos derivados, integrações externas permanecem em rascunho/homologação até aprovação, e decisões operacionais dependem de evidência explícita.
- Padrão semanal 2026-W29: recuperação comprovada antes de continuidade; runtime pós-migração exige readiness executável, mudanças ficam separadas por gate e monitoramento usa menor privilégio com evidência recente e revalidação.
- Padrão semanal 2026-W31: continuidade governada por unidade; evidência técnica não herda autorização, propostas não viram contratos por inferência, provider exige prova de ambiente existente e instalação precisa de black-box no caminho final.
- Atualização de 2026-08-03: baseline FBCP Fase 0 elevou o padrão de faturamento para manifest/hash de aprovação, competência explícita, dinheiro Decimal/centavos, idempotência/ledger, reserva transacional de nosso número, validador CNAB de contrato e outbox transacional antes de escala.
- Atualização de 2026-08-05: Brain v2 saiu de foundation isolada para primeira reintegração efetiva, com MOC cronológico, wikilinks corrigidos e baseline `0` links quebrados/`0` uncategorized; o sync GitHub automático ainda precisa ser reconciliado com staging por manifest.
- Atualização de 2026-08-07: EDC validou o primeiro piloto Codex Zone A read-only, mas a primeira tarefa real de escrita CPIW V4 falhou fechado por boundary; ODP fechou Day 2 PostgreSQL Foundation como `PASS_ACCEPTED`, com Day 3 ainda bloqueado por autorizacao propria.
- Padrão semanal 2026-W32: aplicabilidade vem antes de disponibilidade tecnica; commit de dados e aceitacao operacional sao gates separados; leitura read-only deve provar ausencia de mutacao; Brain v2 usa gate de links/grafo como saude recorrente depois de notas reais.
- Atualização de 2026-08-11: FIP BIKON atingiu GO-LIVE privado/controlado com pendencias materiais zeradas, regressao financeira, backup/rollback, autenticacao e Tailscale tailnet-only; ODP manteve fail-closed porque o executor instalado nao continha o contrato congelado no caminho final.
- Atualizacao de 2026-08-12: FIP `v1.1.0` consolidou tesouraria com saldo oficial reconciliado, mas `v1.2.0` ficou candidato por cobertura documental parcial; Provimento 213 Mini App passou em testes, rotas, Kowalski e pureza read-only, mas segue fail-closed ate reteste real do iPhone.
- Atualizacao de 2026-08-13: ODP Day 3 fechou `PASS_ACCEPTED` sem Day 4; Provimento 213 provou falso `100%` por contagem convertida em percentual, corrigiu contrato semantico em PDF/ICD/Mini App e manteve Golden Baseline bloqueada por corpus historico `PARTIAL_BLOCKED`.
- Atualização de 2026-07-21: reconciliação técnica com evidência de relatório indicou que a proposta Instagram Brand Director v2.1.0 está pendente e não ativa; estado de produção assistida segue sob read-only até autorização explícita de corte.
