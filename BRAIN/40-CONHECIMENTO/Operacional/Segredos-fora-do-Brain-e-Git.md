---
id: brain-3e9ad7dafe0a82beb622
type: knowledge
title: Segredos fora do Brain e Git
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T21:07:33.285014Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md#relações
- type: references
  target: BRAIN/20-EMPRESAS/BIKON/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md#relações
---

# Segredos fora do Brain e Git

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidações de 2026-06-19 a 2026-06-21, fechamento documental FIP em 2026-08-18 e incidente ODP Day 4 em 2026-08-21
confiabilidade: alta
ultima_revisao: 2026-08-22
tags: [segredos, credenciais, git, brain, api, seguranca, stdout, env]
```

## Regra

O Brain pode registrar arquitetura, escopo, permissões, caminhos de cofre e decisões operacionais. Não deve registrar API keys, tokens, senhas, respostas sensíveis, inventário detalhado de clientes/endpoints ou arquivos `.env`.

## Aplicação prática

- Registrar apenas dados não sensíveis e agregados.
- Armazenar segredos em cofre local fora do repositório.
- Usar permissões mínimas para cada integração.
- Não solicitar nem receber chaves de API por Telegram quando houver risco de exposição.
- Nao solicitar nem receber CPF, senha de PDF financeiro ou segredo de pessoa fisica por Telegram, argv, log, banco ou relatorio; usar canal local no-echo aprovado ou falhar fechado.
- Não commitar `.env`, tokens, dumps de API ou relatórios sensíveis.
- Relatórios executivos no Brain devem ser agregados, sem dados operacionais sensíveis desnecessários.
- Nao executar discovery amplo de ambiente que imprima `env` em stdout, mesmo filtrado por regex. Em runtime com tokens residentes, filtro textual posterior nao e boundary de segredo.
- Preflight seguro deve consultar apenas nomes permitidos, imprimir metadata/redacao/hash e validar ausencia de segredo antes de devolver saida a chat, transcript, log ou evidence pack.

## Exemplos conectados

- Notaas NFS-e: chave de API fora do Brain/Git; registro apenas de dados fiscais não sensíveis e guardrails.
- Bitdefender GravityZone: registrar desenho, permissões e métricas agregadas; manter API key e inventário detalhado fora do Brain/Git.

## Relações

- [[70-AUTOMACOES/NOTAAS-NFSE|Skill Notaas NFS-e]]
- [[70-AUTOMACOES/BITDEFENDER-GRAVITYZONE|Bitdefender GravityZone - integração Bikon]]
- [[20-EMPRESAS/BIKON/README|BIKON]]

## Reforço 2026-W26

O padrão foi aplicado a SMTP DreamHost, API WhatsApp Bikon, Instagram/Meta, snapshots versionados de agentes e exemplos bancários Cresol. O Brain registra arquitetura, caminhos de cofre, placeholders e estado operacional; tokens, `.env`, logs, caches, retornos brutos e inventários sensíveis ficam fora do Git.

## Reforço 2026-08-18

No fechamento documental FIP Santander/MP, a ausencia de canal local no-echo para CPF/senha bloqueou a decriptacao Santander. O resultado correto foi `FAIL_CLOSED`: pacote validado, senha nao persistida, nao exposta em log/argv/banco e nenhum PDF decriptado deixado como residuo.

## Reforço 2026-08-22

No ODP Day 4, um comando preparatorio de discovery `env | sort | rg -i ...` expôs referencias logicas de credenciais OpenClaw runtime no stdout/tool result/transcripts. O estado correto foi `RECOVERABLE_P0_SECRET_EXPOSURE_PENDING_OPENCLAW_RUNTIME_SECRET_ROTATION`, com Day 4 `NOT_CONTINUED`, sem registrar plaintext no Brain, e retomada bloqueada ate bridge de rotacao/revogacao, validacao de nova credencial sem stdout secreto e suite negativa com exposicao pos-recuperacao zerada.

## Conhecimento recuperado dos históricos — revisão 2026-09-21

Caso histórico de 18/06/2026: Hebert recusou entregar seu certificado A1 ao agente. O desenho de integração deve respeitar esse limite de custódia: não interpretar a posse de um token de serviço como autorização para obter ou exportar o certificado privado. Uma alternativa de autenticação deve preservar o certificado sob controle do titular e ter escopo explicitamente aprovado; esta memória não atesta implantação de broker nem validade atual de credenciais. Fonte: unidades 34654.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.

## Complementos reconciliados — lote 4 de 2026-09-21

Na integração histórica Bitdefender, a pasta de interação no Drive foi reservada aos arquivos que exigiam participação do usuário. Isso não autorizava transferir toda documentação ou segredos para o Drive; o restante deveria permanecer nos locais operacionais definidos. Não extrapolar para política global de armazenamento sem escopo vigente. Fonte: unidades 33707.

Proveniência e disposições: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch4-20260921.json`. Aplicações históricas permanecem delimitadas pelo período e contrato da fonte.

## Complementos reconciliados — lote 5 de 2026-09-21

Em 02/07/2026, a alternativa à entrega do A1 foi um broker experimental somente em loopback no computador sob controle de Hebert. O objetivo era manter certificado e senha nesse ambiente e permitir consumo de tokens sem transportar a chave privada para o agente. Pacotes de código não continham certificado, senha, token ou .env real. Consulta fiscal e emissão continuavam separadas; esse desenho histórico não autoriza expor o broker em rede, transferir o certificado à VPS ou manter dados desta limpeza no Mac permanentemente. Fonte: unidades 35719, 35722, 35725, 35740.

No experimento SERPRO de 03/07/2026, a tentativa de acessar broker por túnel encontrou endereço interno inacessível, e Hebert pediu retornar ao método local do dia anterior. A localização do OpenClaw na nuvem não autoriza expor broker/certificado nem inventar acesso público. Confirmar rota e custódia autorizadas antes de propor conectividade; consulta local do titular permanece distinta de operação remota pelo agente. Fonte: unidades 37963.

Redação de segredos não deve destruir a estrutura necessária para interpretar a resposta. Separar parsing interno da saída sanitizada; quando o conteúdo redigido ficar inválido, não tratar extração parcial por regex como prova completa de resposta fiscal. Caso histórico SERPRO precisa conservar limites da evidência. Fonte: unidades 38060.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch5-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 6 de 2026-09-21

Em 19/06/2026 foi criada no Drive a pasta Integrações para documentação de APIs/integrações, com registro Bitdefender. A regra era guardar referência técnica sem chaves ou segredos. Essa finalidade documental não autoriza usar Drive como cofre ou perpetuar o fluxo temporário de transferência de credenciais observado em seguida. Fonte: unidades 33706.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 8 de 2026-09-21

Auditoria estática que sinaliza child_process em integração ampla indica capacidade a revisar, não invasão comprovada. Avaliar escopos e scripts reais antes de quarentena/correção. Quando há proxy, confiar apenas nas origens verificadas; runtime/filesystem amplos aceitáveis num cenário solo não demonstram isolamento multiusuário. Os findings de julho não são estado atual. Fonte: unidades 32525.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch8-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 15 de 2026-09-21

Na extração de equivalência Kowalski em 26/07, grep acusou chat_id/ticket_id em listas de campos proibidos e expressões que produziam apenas booleanos. Um nome de campo em código/validador não demonstra vazamento do valor. Examinar fluxo e saída reais, distinguir schema/literal de identificador sensível e testar allowlist de campos e ausência de valores; renomear/fragmentar literal para ficar invisível ao scanner não é prova de privacidade. Regenerar manifesto após qualquer patch. A equivalência final posterior prevalece sobre a validação intermediária deste snapshot. Fonte: unidades 8586.

Na seleção de serventia revision 3 em 30/07, a minimização encontrou duas ocorrências do nome desnecessário, enquanto a expectativa inicial era três. A transformação precisava contar ocorrências reais e validar o resultado, preservando campos institucionais necessários, sem inventar a terceira ocorrência. A classificação por declaração do Owner permaneceu distinta de publicação oficial CNJ. Quantidade esperada em autorização não substitui inspeção do artefato; qualquer diferença deve ser reconciliada antes de declarar cumprimento exato. Fonte: unidades 9000.

Em OAuth, distinguir URL de autorização de callback recebido e validar os parâmetros obrigatórios antes de trocar o código. Resultado vazio de parser pode ser falso negativo: conferir formato e integridade do artefato antes de concluir ausência ou mutação. Restaurar o arquivo local de token preserva seus bytes, mas não garante que o provedor aceite novamente a credencial anterior; não declarar rollback externo apenas com prova de rollback local. Nunca consolidar códigos, estados ou tokens brutos no Brain. Fonte: unidades 36890.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 18 de 2026-09-21

No fluxo histórico OAuth NinjaOne de 18/07, a mensagem de state validado foi corrigida após constatar que o processo de stdin encerrou antes de receber o callback. Conhecer visualmente o valor esperado não prova que o executor recebeu, comparou e vinculou o callback. Registrar precisamente a etapa alcançada, número de POSTs e efeitos persistidos; não consumir ou repetir código com base apenas no resumo. O bloqueio desse pré-check foi superado por tentativa posterior independente, sem tornar o token daquela data uma credencial atual. Fonte: unidades 36902.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch18-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 25 de 2026-09-21

Na validação histórica praxis-gws, um padrão iniciado por hífens foi interpretado como opção e rg terminou com unrecognized flag. O marcador subsequente SECRET_SIGNATURES=absent era inválido e foi descartado. A execução corrigida com padrão explícito (-e) terminou com exit code 1, zero matches e ausência de mutações no escopo examinado. Distinguir erro do scanner, ausência de correspondência e conclusão do controlador; zero matches vale somente para padrões e arquivos efetivamente examinados, não prova ausência universal de segredos. Não imprimir valores sensíveis no diagnóstico nem transportar o sucesso da instalação para autenticação ou operação externa. Fonte: unidades 9447.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch25-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
