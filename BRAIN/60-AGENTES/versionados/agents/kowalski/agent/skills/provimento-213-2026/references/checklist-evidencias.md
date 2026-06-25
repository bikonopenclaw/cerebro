# Checklist de evidências, Provimento CNJ 213/2026

Use como base para diagnóstico e dossiê. Status permitido: Atendido, Parcial, Pendente, Não avaliado, Não aplicável.

## Estrutura da matriz

Colunas recomendadas:

`Etapa | Item | Exigência | Classe | Status | Evidência analisada | Lacuna | Risco | Ação recomendada | Responsável | Prazo sugerido`

## Etapa 1, governança e conformidade

| Item | Exigência | Evidências esperadas |
|---|---|---|
| 1.1 | Responsável técnico interno designado | ato interno, e-mail formal, ata, contrato ou termo de designação |
| 1.1 | Responsável pela serventia como controlador de dados | declaração formal, política LGPD, registro interno |
| 1.1 | DPO/encarregado quando aplicável | termo de designação, canal de contato, política publicada |
| 1.2 | Política de Segurança aprovada e divulgada | documento vigente, data, assinatura/aprovação, comprovante de divulgação interna |
| 1.2 | Diretrizes de PCN/PRD planejadas na política | seção com escopo, governança, objetivos, cronograma e critérios de continuidade |
| 1.3 | Autenticação individualizada | lista de usuários, prints de configuração, relatório do sistema |
| 1.3 | MFA em acessos administrativos e críticos | prints/configuração MFA, relatório de usuários, política de acesso |
| 1.3 | Proibição de contas compartilhadas | política, lista de usuários sem genéricos, plano de eliminação se houver exceção temporária |
| 1.4 | Registro de operações de tratamento de dados pessoais | inventário LGPD, ROPA, planilha controlada ou ferramenta equivalente |
| 1.5 | Gestão/comunicação de incidentes críticos | procedimento, matriz de gravidade, fluxo de comunicação à Corregedoria e ANPD quando aplicável |
| 1.7 | Inventário tecnológico completo | inventário de ativos, sistemas, integrações, bancos, certificados, softwares, contratos e atualizações |
| 1.8 | Licenciamento regular | notas fiscais, contratos, painel de licenças, termos de uso |
| 1.8 | Contratos com terceiros revisados | cláusulas de confidencialidade, reversibilidade, portabilidade, documentação técnica, incidentes e LGPD |
| 1.9 | Declaração de conclusão da Etapa 1 | declaração assinada e registro no Justiça Aberta |

## Etapa 2, infraestrutura e continuidade

| Item | Exigência | Evidências esperadas |
|---|---|---|
| 2.1 | Energia estável, aterramento e UPS/SAI | fotos, nota fiscal, laudo/relatório, inventário, teste de autonomia |
| 2.2 | Plano de contingência energética | procedimento com responsáveis e ações em queda de energia |
| 2.3 | Ambiente físico protegido | fotos, controle de acesso, extintor/proteção, sala técnica, temperatura |
| 2.4 | Conectividade compatível com classe | contrato de internet, speed tests, teste de sincronização/backup dentro do RPO |
| 2.4 | Roteador, switch e múltiplos links quando necessário | diagrama, inventário, configurações, contrato do link secundário se houver |
| 2.5 | PCN formalizado | documento com riscos, medidas de mitigação, responsáveis, comunicação, operação mínima |
| 2.5 | PRD formalizado | documento com restauração, ordem de prioridade, RTO/RPO, backup, testes e responsáveis |
| 2.6 | Suporte técnico contínuo | contrato SLA, canal de suporte, escala, evidência de chamados |
| 2.7 | Proteção básica de endpoint | painel antivírus/antimalware, lista de estações/servidores protegidos |
| 2.8 | Documento de arquitetura | topologia, ambientes local/nuvem/híbrido/SaaS, fluxos críticos, backups, integrações, redundância |
| 2.9 | Declaração de conclusão da Etapa 2 | declaração assinada e registro no Justiça Aberta |

## Etapa 3, acervo digital e resiliência

| Item | Exigência | Evidências esperadas |
|---|---|---|
| 3.1 | Criptografia em trânsito | configuração TLS, URLs, certificados, relatório técnico |
| 3.1 | Criptografia em repouso e backups | configuração de disco, banco, backup, cofre/chave, relatório do fornecedor |
| 3.1 | Gestão de chaves/certificados | inventário, política de rotação, controle de acesso, logs de renovação/revogação |
| 3.2 | Backup completo automatizado | política, agenda, logs, relatórios de execução |
| 3.2 | Backup incremental compatível com RPO | logs, relatório de janela de backup, evidência de sincronização |
| 3.2 | Dois ambientes independentes ou nuvem equivalente | arquitetura, contrato, retenção imutável, redundância geográfica, segregação de acesso |
| 3.2 | Proteção contra ransomware/exclusão indevida | WORM, retention lock, versionamento bloqueado, cofre isolado ou equivalente |
| 3.3 | Monitoramento de backup com alertas | prints de alertas, e-mails, dashboard, histórico de falhas e tratamento |
| 3.4 | Firewall stateful com IPS/IDS e segmentação | configuração, topologia, VLANs, regras, relatório do firewall |
| 3.5 | Endpoint avançado quando compatível | EDR/XDR/MDR ou justificativa técnica proporcional à classe |
| 3.6 | SGBD com integridade transacional e logs ativos | configuração do banco, logs, documentação do sistema |
| 3.7 | Tolerância a falhas/alta disponibilidade | redundância, cluster, replicação, spare, plano documentado |
| 3.8 | Trilhas de auditoria técnicas imutáveis | logs com usuário/data/hora/ação/resultado, NTP, retenção, proteção contra alteração |
| 3.9 | Declaração de conclusão da Etapa 3 | declaração assinada e registro no Justiça Aberta |

## Etapa 4, monitoramento e validação

| Item | Exigência | Evidências esperadas |
|---|---|---|
| 4.1 | Relatório de conformidade de trilhas de auditoria | relatório atestando imutabilidade, usuário, tempo sincronizado, retenção e backup dos logs |
| 4.2 | Rotina de atualização periódica | política de patch, calendário, registros de atualização |
| 4.3 | Gestão formal de vulnerabilidades | ferramenta, planilha, relatórios, classificação, responsável e datas |
| 4.3 | Críticas tratadas conforme Anexo II | evidência de correção, contenção, exceção justificada, prazo e responsável |
| 4.4 | Simulação anual de desastre | ata, roteiro, resultado, falhas encontradas, plano de correção |
| 4.5 | Teste documentado de restauração | ata/modelo, logs, tempo medido, dados restaurados, conclusão |
| 4.6 | Avaliações técnicas periódicas | relatório de análise, hardening, varredura, revisão de configuração |
| 4.7 | Classe 3, pentest ou equivalente | relatório, escopo, metodologia, correções, reteste ou justificativa normativa |
| 4.8 | Análise de causa raiz e lições aprendidas | RCA, plano de ação, revisão de processo após incidentes |
| 4.9 | Declaração de conclusão da Etapa 4 | declaração assinada e registro no Justiça Aberta |

## Etapa 5, interoperabilidade e governança evolutiva

| Item | Exigência | Evidências esperadas |
|---|---|---|
| 5.1 | Integração com plataformas de fiscalização | documentação técnica, teste de integração, evidência de transmissão/consulta |
| 5.2 | Padrões abertos e neutralidade tecnológica | formato de exportação, APIs, documentação, ausência de lock-in injustificado |
| 5.3 | Capacitação periódica | lista de presença, pauta, materiais, periodicidade, avaliação |
| 5.4 | Revisão da política e criptografia | ata de revisão, changelog, versão nova, avaliação de protocolos/algoritmos |
| 5.5 | Registros auditáveis por 5 anos | política de retenção, armazenamento, permissões, amostra de evidência |
| 5.6 | Plano de reversibilidade e portabilidade | plano, papéis, formato de dados, roteiro de extração, fornecedor envolvido |
| 5.6 | Simulação de extração integral do acervo | relatório de teste, hash, validação de consistência, amostragem, tempo e resultado |
| 5.7 | Declaração de conclusão da Etapa 5 | declaração assinada e registro no Justiça Aberta |

## Evidências fortes

Priorizar evidências que tenham data, responsável, origem, integridade e relação clara com o requisito.

Boas evidências:

- relatório exportado do sistema
- print com data e identificação do ambiente, sem credenciais
- contrato/cláusula assinada
- ata assinada
- hash de arquivo
- log de execução
- ticket/chamado concluído
- configuração exportada
- relatório técnico de fornecedor

Evidências fracas, usar só como apoio:

- declaração verbal
- print sem contexto
- promessa de fornecedor
- planilha sem responsável/data
- política sem aprovação ou divulgação

## Red flags

Marcar como crítico quando aparecer:

- backup sem teste de restauração
- backup só local no mesmo ambiente de produção
- backup sem retenção imutável ou equivalente
- ausência de MFA administrativo
- conta compartilhada para atos críticos
- logs que podem ser apagados por usuário comum
- ausência de PCN/PRD na Etapa 2
- contrato sem portabilidade/reversibilidade
- fornecedor único sem teste de extração do acervo
- classe não informada em diagnóstico com prazo normativo relevante
