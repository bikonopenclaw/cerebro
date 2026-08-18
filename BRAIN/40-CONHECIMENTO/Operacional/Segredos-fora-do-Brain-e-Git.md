# Segredos fora do Brain e Git

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidações de 2026-06-19 a 2026-06-21 e fechamento documental FIP em 2026-08-18
confiabilidade: alta
ultima_revisao: 2026-08-18
tags: [segredos, credenciais, git, brain, api, seguranca]
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

## Exemplos conectados

- Notaas NFS-e: chave de API fora do Brain/Git; registro apenas de dados fiscais não sensíveis e guardrails.
- Bitdefender GravityZone: registrar desenho, permissões e métricas agregadas; manter API key e inventário detalhado fora do Brain/Git.

## Relações

- `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- `BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md`
- `BRAIN/20-EMPRESAS/BIKON/README.md`

## Reforço 2026-W26

O padrão foi aplicado a SMTP DreamHost, API WhatsApp Bikon, Instagram/Meta, snapshots versionados de agentes e exemplos bancários Cresol. O Brain registra arquitetura, caminhos de cofre, placeholders e estado operacional; tokens, `.env`, logs, caches, retornos brutos e inventários sensíveis ficam fora do Git.

## Reforço 2026-08-18

No fechamento documental FIP Santander/MP, a ausencia de canal local no-echo para CPF/senha bloqueou a decriptacao Santander. O resultado correto foi `FAIL_CLOSED`: pacote validado, senha nao persistida, nao exposta em log/argv/banco e nenhum PDF decriptado deixado como residuo.
