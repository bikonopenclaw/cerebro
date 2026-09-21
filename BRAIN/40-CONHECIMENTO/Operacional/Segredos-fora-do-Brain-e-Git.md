---
id: brain-3e9ad7dafe0a82beb622
type: knowledge
title: Segredos fora do Brain e Git
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T18:55:38.578515Z'
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
