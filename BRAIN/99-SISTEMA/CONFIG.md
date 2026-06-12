# BRAIN ENTERPRISE
## Sistema Corporativo de Gestão do Conhecimento

Versão: 1.0

## Identidade

O Agente Principal desta instância administra o Brain.

O Brain é o sistema permanente de gestão do conhecimento desta instância. Não é agente, não é assistente e não é conversa solta. É patrimônio intelectual acumulado.

## Missão

Transformar interações, decisões, aprendizados, documentos, projetos, empresas e relacionamentos em conhecimento estruturado, preservado, organizado, relacionado, atualizado e recuperável ao longo do tempo.

## Princípio fundamental

O Agente Principal administra o Brain. O Brain administra o conhecimento. O conhecimento preserva a continuidade.

## Objetivos

- Preservar contexto histórico.
- Evitar perda de conhecimento.
- Reduzir retrabalho.
- Registrar decisões.
- Consolidar aprendizados.
- Mapear relacionamentos.
- Estruturar informações.
- Aumentar a capacidade futura de tomada de decisão.

## Responsabilidades do Agente Principal

- Consultar o Brain quando necessário.
- Atualizar o Brain quando necessário.
- Consolidar conhecimento.
- Evitar duplicidades.
- Preservar histórico.
- Relacionar informações.
- Manter a estrutura organizada.
- Garantir integridade dos registros.

## Filosofia de funcionamento

Durante o dia o foco principal é execução. O Agente Principal não deve interromper o trabalho para registrar permanentemente cada interação. O Brain é atualizado através de consolidação periódica.

## Consolidação diária

Uma vez por dia, analisar o contexto acumulado e identificar:

- Conhecimento relevante.
- Pessoas.
- Empresas.
- Projetos.
- Aprendizados.
- Decisões.
- Oportunidades.
- Riscos.
- Registros existentes que precisam de atualização.
- Novos registros necessários.

## Princípio de relevância

Registrar apenas informação com potencial de utilidade futura.

Registrar:

- Decisões.
- Aprendizados.
- Estratégias.
- Processos.
- Relacionamentos.
- Oportunidades.
- Riscos.
- Preferências relevantes.
- Informações empresariais.
- Informações de projetos.

Não registrar:

- Cumprimentos.
- Mensagens triviais.
- Conversas sem valor histórico.
- Repetições desnecessárias.
- Ruído operacional.

## Estrutura oficial

```text
BRAIN/
├── 00-INBOX
├── 01-DIARIO
├── 20-EMPRESAS
├── 30-PESSOAS
├── 40-CONHECIMENTO
├── 50-PROJETOS
├── 60-AGENTES
├── 70-AUTOMACOES
├── 80-DASHBOARDS
└── 99-SISTEMA
```

## 00-INBOX

Área temporária para ideias, documentos, observações e conteúdos ainda não classificados.

Nenhum item deve permanecer indefinidamente na Inbox.

## 01-DIARIO

Registro cronológico consolidado das atividades relevantes. O Diário não é memória permanente, é camada histórica. Informações permanentes devem ser promovidas para Pessoas, Empresas, Projetos, Conhecimento ou Memory.

### Modelo de diário

```markdown
# Data

## Pessoas
## Empresas
## Projetos
## Oportunidades
## Problemas
## Decisões
## Aprendizados
## Ideias
## Próximas ações
```

## 20-EMPRESAS

Armazenar conhecimento organizacional: histórico, estrutura, decisões, oportunidades, riscos, projetos, pessoas e aprendizados relevantes.

## 30-PESSOAS

Gerenciar conhecimento relacional.

Para pessoas físicas, registrar nome, função, empresa, histórico, preferências, interesses, relacionamento e observações relevantes.

Observações comportamentais devem ser apenas operacionais. Nunca registrar diagnóstico médico ou psicológico. Nunca apresentar inferências como fatos.

Sentimento do relacionamento, quando houver evidência suficiente: Positivo, Neutro ou Negativo, sempre com justificativa objetiva.

Para pessoas jurídicas, registrar razão social, segmento, porte, histórico, oportunidades, riscos, relacionamento e projetos associados.

## Mapa de relacionamentos

Manter conexões explícitas entre:

- Pessoa ↔ Pessoa
- Pessoa ↔ Empresa
- Pessoa ↔ Projeto
- Empresa ↔ Projeto
- Projeto ↔ Conhecimento

## 40-CONHECIMENTO

Biblioteca institucional permanente.

Todo conhecimento deve possuir:

```yaml
categoria:
fonte:
confiabilidade:
ultima_revisao:
tags:
```

## 50-PROJETOS

Gerenciar iniciativas.

Todo projeto deve conter:

```yaml
nome:
status:
responsavel:
inicio:
fim:
prioridade:
```

Registrar objetivos, marcos, decisões, riscos, bloqueios e próximos passos.

## 60-AGENTES

Documentação dos agentes existentes: finalidade, capacidades, limitações, integrações e histórico de alterações.

## 70-AUTOMACOES

Registrar workflows, integrações, crons, gatilhos e dependências.

## 80-DASHBOARDS

Consolidar indicadores: projetos ativos, empresas acompanhadas, pessoas relevantes, conhecimento produzido e health score.

## 99-SISTEMA

Arquivos obrigatórios:

- MEMORY.md
- INDEX.md
- CHANGELOG.md
- HEALTH.md
- CONFIG.md

## MEMORY.md

Memória institucional consolidada: preferências recorrentes, padrões observados, decisões estruturantes, aprendizados permanentes e diretrizes relevantes.

## INDEX.md

Mapa geral do Brain para facilitar navegação e descoberta.

## CHANGELOG.md

Registrar criação, atualização, arquivamento e reorganização.

## HEALTH.md

Monitorar duplicados, órfãos, projetos abandonados, empresas sem atualização, pessoas sem atualização e conhecimento desatualizado.

Produzir Health Score de 0 a 100.

## Detecção de duplicidade

Antes de criar qualquer registro:

1. Procurar registros existentes.
2. Verificar possíveis duplicações.
3. Atualizar registros existentes quando apropriado.
4. Evitar fragmentação do conhecimento.

## Relacionamento entre registros

Sempre que possível criar conexões explícitas. Nenhuma informação importante deve permanecer isolada.

Todo conhecimento deve apontar para pessoas, empresas, projetos e aprendizados relacionados quando aplicável.


## Filosofia cognitiva

A filosofia oficial do Brain está em `BRAIN/99-SISTEMA/FILOSOFIA.md`.

Regra central: o Brain não existe para registrar o passado. O Brain existe para melhorar o futuro.

Toda consolidação deve seguir os princípios de memória maior que armazenamento, contexto maior que fato, conhecimento conectado, relevância conquistada e esquecimento saudável.

## Regra final

O Brain não é um arquivo. O Brain não é um repositório de documentos. O Brain é um sistema vivo de conhecimento.

Toda informação registrada deve aumentar a capacidade futura desta instância de compreender contexto, recuperar histórico, apoiar decisões e preservar conhecimento ao longo do tempo.
