# Consolidação diária silenciosa do Brain

```yaml
nome: Consolidação diária silenciosa do Brain
status: ativa
responsavel: Agente Principal / Puppet Master
frequencia: diária
horario_referencia_utc: "18:05"
ultima_revisao: 2026-06-12
fonte: cron d95bbe73-24d9-4e2b-ba57-0032082bb54b e BRAIN/99-SISTEMA/ROTINA-CONSOLIDACAO.md
```

## Finalidade

Executar consolidação diária do Brain sem interromper Hebert, registrando apenas conhecimento com utilidade futura.

## Regras operacionais

- Não enviar mensagem ao Hebert, salvo emergência real.
- Não registrar cumprimentos, ruído ou informação trivial.
- Não criar agente Brain.
- Não acessar sistemas externos sem autorização.
- Atualizar registros existentes antes de criar novos.
- Criar ou atualizar diário em `BRAIN/01-DIARIO/YYYY/YYYY-MM-DD.md`.
- Atualizar `CHANGELOG.md` e `HEALTH.md` quando houver impacto.
- Fazer commit local no repositório Brain quando houver alterações.

## Arquivos relacionados

- `BRAIN/99-SISTEMA/CONFIG.md`
- `BRAIN/99-SISTEMA/ROTINA-CONSOLIDACAO.md`
- `BRAIN/01-DIARIO/2026/2026-06-12.md`
