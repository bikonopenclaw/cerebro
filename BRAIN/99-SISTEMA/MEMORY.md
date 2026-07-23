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

## Padrões consolidados mensalmente

- Padrão mensal de junho/2026: segurança operacional antes de escala; automações podem preparar e validar, mas impactos fiscais, bancários, comunicacionais, publicações e alterações de identidade exigem confirmação explícita quando não autorizados previamente.
- Padrão semanal 2026-W28: maturidade operacional antes de escala; snapshots seguros excluem artefatos derivados, integrações externas permanecem em rascunho/homologação até aprovação, e decisões operacionais dependem de evidência explícita.
- Padrão semanal 2026-W29: recuperação comprovada antes de continuidade; runtime pós-migração exige readiness executável, mudanças ficam separadas por gate e monitoramento usa menor privilégio com evidência recente e revalidação.
- Atualização de 2026-07-21: reconciliação técnica com evidência de relatório indicou que a proposta Instagram Brand Director v2.1.0 está pendente e não ativa; estado de produção assistida segue sob read-only até autorização explícita de corte.
