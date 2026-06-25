# Resumo operacional, Provimento CNJ 213/2026

Fonte base: Provimento n. 213 de 20 de fevereiro de 2026, CNJ. Usar como apoio técnico, não como parecer jurídico.

## Finalidade

Estabelece padrões mínimos de tecnologia da informação e comunicação para serviços notariais e de registro no Brasil, buscando segurança, integridade, disponibilidade, autenticidade, rastreabilidade e continuidade operacional.

Revoga o Provimento n. 74/2018.

## Conceitos importantes

- Dossiê técnico: conjunto organizado, íntegro e verificável de evidências documentais, técnicas e operacionais para demonstrar cumprimento de etapa ou requisito.
- Incidente crítico: evento de segurança que comprometa ou possa comprometer disponibilidade, integridade, autenticidade, confidencialidade, rastreabilidade ou continuidade.
- PCN: Plano de Continuidade de Negócios.
- PRD: Plano de Recuperação de Desastres.
- RPO: ponto máximo de perda de dados aceitável.
- RTO: tempo máximo para restabelecer operações essenciais.
- Reversibilidade: restituição integral e utilizável de dados, configurações e registros da serventia.
- Portabilidade: extração, transferência e reutilização estruturada dos dados em formato interoperável.

## Classes da serventia

O enquadramento é por arrecadação bruta semestral, conforme diretrizes da Corregedoria Nacional.

- Classe 1: receita semestral até R$ 100.000,00.
- Classe 2 e Classe 3: validar faixas no texto oficial/diretriz aplicável antes de afirmar em relatório.

Se a classe não for informada, não presumir. Marcar como pendência crítica de escopo porque prazos, RTO/RPO, backup e evidências dependem da classe.

## Prazos

Implementação inicial obrigatória, Etapas 1 e 2 do Anexo IV:

- Classe 3: 90 dias da entrada em vigor.
- Classe 2: 150 dias da entrada em vigor.
- Classe 1: 210 dias da entrada em vigor.

Implementação integral, Etapas 1 a 5:

- Classe 3: até 24 meses.
- Classe 2: até 30 meses.
- Classe 1: até 36 meses.

Prorrogação excepcional: até 90 dias, uma única vez, mediante decisão fundamentada da Corregedoria, plano formal com cronograma, responsáveis e medidas compensatórias mínimas.

## Etapas do Anexo IV

### Etapa 1, Governança, estruturação e conformidade legal

Objetivo: instituir governança formal, política interna, LGPD, controle de acessos, inventário e base documental.

Itens centrais:

- designar responsável técnico interno
- reconhecer responsável pela serventia como controlador de dados
- designar DPO/encarregado quando aplicável
- elaborar e divulgar Política de Segurança da Informação com conteúdo mínimo do Anexo III
- planejar diretrizes de PCN/PRD para formalização completa na Etapa 2
- implementar autenticação individualizada e MFA para acessos administrativos
- vedar credenciais compartilhadas
- registrar operações de tratamento de dados pessoais
- definir processo de comunicação de incidentes críticos à Corregedoria
- elaborar inventário completo de ativos, integrações, bancos, certificados, softwares, atualizações e contratos
- regularizar licenciamento e contratos com terceiros, incluindo confidencialidade, reversibilidade, portabilidade, documentação técnica, transição, incidentes e LGPD
- produzir declaração de conclusão e registrar no Justiça Aberta

### Etapa 2, Infraestrutura e continuidade operacional

Objetivo: garantir base física, elétrica, rede, segurança física, PCN e PRD.

Itens centrais:

- fonte de energia estável, aterramento e SAI/UPS
- plano de contingência energética
- ambiente físico com controle de acesso e proteção contra incêndio, inundação e variação térmica
- conectividade compatível com a classe
- roteador, switch e múltiplos links quando necessário
- PCN e PRD com riscos, mitigação, RTO, RPO e medidas de curto e médio prazo
- suporte técnico contínuo
- proteção básica de endpoint em estações e servidores
- documento de arquitetura tecnológica com topologia, ambientes, fluxos críticos, localização de backups, integrações e redundância
- declaração de conclusão e registro no Justiça Aberta

### Etapa 3, Proteção do acervo digital e resiliência tecnológica

Objetivo: proteger acervo eletrônico com criptografia, backup, redundância, monitoramento, firewall, endpoint, SGBD e logs.

Itens centrais:

- criptografia em trânsito e em repouso, inclusive backups
- gestão formal de chaves e certificados
- backups completos e incrementais automatizados
- no mínimo dois ambientes tecnicamente independentes ou nuvem com redundância geográfica, retenção imutável, segregação de acesso, logs auditáveis e restauração comprovável
- monitoramento de backup com alertas e registro formal de falhas
- firewall stateful com IPS/IDS e segmentação lógica
- proteção avançada de endpoint quando compatível com a classe
- SGBD com integridade transacional e logs ativos
- tolerância a falhas ou alta disponibilidade compatível com a classe
- trilhas de auditoria técnicas imutáveis, sincronização de tempo confiável e integração com backup/recuperação
- declaração de conclusão e registro no Justiça Aberta

### Etapa 4, Monitoramento, auditoria e validação de controles

Objetivo: validar controles, rastreabilidade, vulnerabilidades e restauração.

Itens centrais:

- relatório de conformidade de trilhas de auditoria
- rotina documentada de atualização de sistemas e aplicações
- gestão formal de vulnerabilidades
- contenção e correção emergencial preferencialmente em até 72 horas em caso de exploração ativa ou risco iminente
- simulação anual de desastre para validar PCN/PRD
- testes documentados de restauração de backups conforme classe
- avaliações técnicas periódicas de segurança
- Classe 3: pentest ou metodologia equivalente, conforme Anexo II
- análise de causa raiz e lições aprendidas para incidentes
- declaração de conclusão e registro no Justiça Aberta

### Etapa 5, Interoperabilidade, consolidação e governança evolutiva

Objetivo: interoperabilidade, revisão contínua, capacitação e portabilidade.

Itens centrais:

- adequar sistemas para interoperabilidade com plataformas eletrônicas de fiscalização
- adotar padrões abertos e neutralidade tecnológica
- prevenir dependência exclusiva de fornecedor
- capacitação periódica com registro formal
- revisar política de segurança e padrões criptográficos quando houver mudança normativa ou evolução tecnológica
- manter registros auditáveis por no mínimo 5 anos
- manter plano formal de reversibilidade e portabilidade
- simular extração integral do acervo em formato interoperável e não proprietário
- periodicidade da simulação de extração: Classe 3 a cada 24 meses, Classe 2 a cada 30 meses, Classe 1 a cada 36 meses, ou imediatamente em alteração relevante de fornecedor/arquitetura/governança
- declaração de conclusão e registro no Justiça Aberta

## RTO, RPO e backup

RPO mínimo:

- Classe 3: até 4 horas.
- Classe 2: até 12 horas.
- Classe 1: até 24 horas.

RTO mínimo:

- Classe 3: até 8 horas.
- Classe 2: até 24 horas.
- Classe 1: até 24 horas, admitida restauração simplificada documentada.

Backup completo:

- Classe 3: intervalo máximo 24 horas.
- Classe 2: intervalo máximo 48 horas.
- Classe 1: intervalo máximo 72 horas, se cumprir o RPO.

Backup incremental deve ser compatível com o RPO da classe.

## Evidência e guarda

- Classe 1: relatório simplificado, contratos, notas fiscais e evidências guardados por no mínimo 5 anos.
- Classes 2 e 3: dossiê técnico com mecanismo de integridade, no mínimo hashes dos arquivos e lista assinada digitalmente, ou documento eletrônico único assinado acompanhado de relatório de hash.
- Evidência mínima: relatório em formato aberto, prints/logs/configurações/relatórios de fornecedor, responsável, data e status.

## Itens técnicos recorrentes

- MFA obrigatório para acessos administrativos, gestão de sistemas, bancos de dados e funcionalidades críticas.
- Contas genéricas e credenciais compartilhadas são vedadas.
- Criptografia em trânsito: TLS 1.2 ou superior, ou versão mantida e suportada.
- Criptografia em repouso para dados críticos: AES-256 ou equivalente/superior.
- Logs devem registrar usuário, data, hora, minuto, segundo, ação e resultado, protegidos contra alteração, exclusão não autorizada e perda acidental.
- Política de Segurança precisa cobrir governança, acessos, uso aceitável, PCN/PRD, proteção física, incidentes, vulnerabilidades, LGPD, criptografia, fornecedores, revisão e auditoria.
