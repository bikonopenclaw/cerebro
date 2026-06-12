# Skill Notaas NFS-e

## Status

Instalada com hardening em 2026-06-12.

## Locais

- Skill exclusiva Darth Vader: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse`
- Auditoria: `/data/.openclaw/workspace/audits/notaas-nfse/AUDITORIA.md`
- Instalação: `/data/.openclaw/workspace/audits/notaas-nfse/INSTALACAO.md`

## Finalidade

Emitir, consultar, baixar e cancelar NFS-e via API Notaas.

## Guardrails aplicados

- `--dry-run` e alias `--teste` para simulação sem chamada à API.
- Emissão real exige `--confirmar-emissao`.
- Cancelamento real exige `--confirmar-cancelamento`.
- Dependências instaladas em `vendor/`, sem mexer no Python global.
- `.env` com permissão `600`.
- `.env.example` criado.
- `scripts/cadastrar_cliente.py` criado.
- `SKILL.md` corrigido com frontmatter obrigatório.

## Validação

- Skill visível no OpenClaw: `openclaw skills info notaas-nfse` retorna `Ready`.
- `emitir_nota.py --dry-run` validado sem envio.
- `emitir_lote.py --dry-run` validado sem envio.
- `cancelar_nota.py --dry-run` validado sem envio.
- Operação real sem confirmação é bloqueada.

## Configuração

Configurada em 2026-06-12 para Bikon Tecnologia da Informação Ltda Me.

Dados não sensíveis registrados:

- CNPJ: 34.191.026/0001-86
- Inscrição Municipal: 083712941
- Cidade/UF: Vitória/ES
- Código IBGE: 3205309

A API key foi armazenada apenas nos arquivos locais `.env` e `config/empresa.json`, com permissão `600`. Não registrar segredo no Brain nem no Git.

## Regra operacional

Qualquer emissão ou cancelamento real de NFS-e deve ser previamente autorizado pelo Hebert/Puppet Master, por envolver obrigação fiscal.

## Exclusividade

Em 2026-06-12, a skill foi restringida para uso exclusivo da Darth Vader.

Validação realizada:

- `openclaw skills check --agent darth-vader` mostra `notaas-nfse`.
- `openclaw skills check --agent main` não mostra `notaas-nfse`.
- `openclaw skills check --agent kowalski` não mostra `notaas-nfse`.

A skill foi removida dos diretórios globais/main e mantida apenas no workspace da Darth Vader.
