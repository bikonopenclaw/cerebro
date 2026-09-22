---
id: brain-semantic-runtime-operations-20260922
type: state
title: Operação da pesquisa semântica e acesso das rotinas do Brain
created: '2026-09-22'
updated: '2026-09-22'
relationships:
- type: references
  target: BRAIN/99-SISTEMA/brain-v2/governance/semantic-coverage-and-archive.md
  reason: A consulta ajuda a encontrar fontes; cobertura e descarte exigem provas próprias.
---

# Operação da pesquisa semântica

Os cinco agentes — main, Kowalski, Darth Vader, Robotnik e Sentinel — usam a habilidade compartilhada `brain-semantic-search`. A consulta executa o modelo local e lê o índice existente. Ela não atualiza o índice, não cria cache e não altera fontes. Similaridade serve para localizar candidatos; os vínculos entre notas precisam de justificativa nas fontes e não representam autorização para executar instruções históricas.

```sh
/data/.openclaw/skills/brain-semantic-search/scripts/search "pergunta sobre uma decisão anterior"
```

O escopo padrão prioriza conhecimento permanente. `--scope all` inclui também diários e estados. Fontes, hashes e vínculos acompanham os resultados. Índice ausente, incompatível ou desatualizado gera indisponibilidade explícita; esse resultado não significa ausência de memória.

## Atualização separada da consulta

O runtime ativo fica em `/data/.openclaw/local/brain-semantic/current`, apontando para a versão `20260922-v3`. Modelo, ambiente Python e índice são compartilhados, fora do Git.

`brain-semantic-index-refresh.path` observa a revisão Git do checkout canônico do Brain. Ao mudar a referência da branch, HEAD ou referências compactadas, aciona `brain-semantic-index-refresh.service`. O serviço roda como openclaw, sem rede, com escrita permitida somente em `/data/.openclaw/local/brain-semantic/index`. O índice conserva no máximo duas gerações e troca a geração corrente atomicamente.

Alterações ainda não commitadas podem deixar a consulta indisponível até a atualização seguinte. Não conceder escrita aos agentes para contornar esse estado. A manutenção autorizada pode consultar o resultado do serviço e, se necessário, acioná-lo novamente. Não criar outro provedor ou baixar modelos automaticamente.

## Consolidação dos perfis

No perfil gerenciado do gateway principal, o acesso adicional aos históricos externos ao workspace é somente de leitura e exige simultaneamente o agente main e uma execução identificada de uma destas rotinas existentes:

| Rotina | ID |
|---|---|
| Diária | `d95bbe73-24d9-4e2b-ba57-0032082bb54b` |
| Semanal | `1a1ed29a-fd45-4c5f-93f6-c3b556a2743c` |
| Mensal | `c8410fc9-1d2f-4ce0-8847-70e69db6f405` |

As fontes permitidas são memórias e históricos dos cinco agentes, nos três perfis conhecidos. As demais tarefas do perfil gerenciado não recebem essa leitura adicional. Main mantém sua permissão preexistente de edição do Brain; Robotnik e Sentinel recebem leitura do Brain para pesquisa.

Os gateways separados de Kowalski e Darth Vader não usam esse perfil de proxy: mantêm o modo `workspace-write` preexistente, que permite leitura mais ampla e limita a escrita ao workspace. O ajuste preserva esse comportamento. A consulta sem escrita funciona também nesse modo; não se deve afirmar que os dois gateways têm o mesmo bloqueio de leitura de segredos do perfil principal. A correção não acrescenta escrita nos históricos nem acesso adicional a segredos, configurações privadas ou chaves SSH.

Cada ciclo deve registrar o que efetivamente leu e como tratou cada fonte. Diretórios visíveis, inventário, resultados de pesquisa e status de cron não comprovam cobertura editorial. A lacuna do ciclo de 22/09 permanece documentada como fato daquele momento; corrigir o ambiente não transforma uma revisão parcial passada em revisão completa.

O envio ao GitHub continua usando a rotina existente. Na execução de 21/09 às 22h BRT, a ferramenta concluiu o sync com `Everything up-to-date`; a falha posterior de geração de resposta do agente foi distinta do resultado do Git. Não ampliar acesso a credenciais com base somente no status agregado dessa execução.

## Reinícios, atualização e recuperação

As permissões são construídas por execução em cópias locais da configuração; o perfil global não é alterado. O ajuste está instalado nos três pacotes atualmente usados pelos gateways. Reinícios comuns conservam os arquivos e a habilidade.

Atualizações de pacote podem substituir esses arquivos. A manutenção deve conferir caminhos e hashes, reavaliar o patch e repetir os testes antes de declarar o acesso validado. Não reaplicar automaticamente sobre código desconhecido nem ampliar permissões como fallback. Os originais, patches, testes e manifesto de recuperação estão em `/var/lib/brain-coverage-20260921/semantic-readonly-deployment`, protegido para administração.

O teste de manutenção deve usar o gerador de permissões e o binário correspondentes a cada instalação: as bases dos perfis não são idênticas. Verificar a consulta real nos cinco agentes, inventário nas três rotinas, recusa de escrita no índice e nas fontes externas, e inacessibilidade dos arquivos sensíveis. Depois de atualizar o plugin, recarregar somente gateways sem trabalho ativo e conferir sua saúde.

Nenhum histórico bruto, modelo ou banco operacional deve ser incluído no Git. A limpeza histórica de 26.329 arquivos tem manifesto e recibo próprios; esta capacidade persistente não cria autorização para novas exclusões automáticas.
