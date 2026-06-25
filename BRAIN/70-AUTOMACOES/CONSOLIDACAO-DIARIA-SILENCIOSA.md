# Consolidação diária silenciosa do Brain

```yaml
nome: Consolidação diária silenciosa do Brain
status: ativa
responsavel: Agente Principal / Puppet Master
frequencia: diária
horario_referencia_utc: "18:05"
ultima_revisao: 2026-06-25
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
- Antes de consolidar, rodar `/data/.openclaw/workspace/Brain/scripts/sync-agentes-versionados.py` para atualizar os snapshots seguros do Kowalski, Darth Vader e Robotnik.
- Criar ou atualizar diário em `BRAIN/01-DIARIO/YYYY/YYYY-MM-DD.md`.
- Atualizar `CHANGELOG.md` e `HEALTH.md` quando houver impacto.
- Fazer commit local no repositório Brain quando houver alterações, incluindo mudanças nos snapshots versionados dos agentes.
- Não versionar segredos, `.env` reais, sessões, caches, relatórios finais, PDFs, imagens, artefatos gerados ou dados brutos sensíveis dos agentes.

## Arquivos relacionados

- `BRAIN/99-SISTEMA/CONFIG.md`
- `BRAIN/99-SISTEMA/ROTINA-CONSOLIDACAO.md`
- `BRAIN/01-DIARIO/2026/2026-06-12.md`
- `BRAIN/01-DIARIO/2026/2026-06-17.md`
- `BRAIN/01-DIARIO/2026/2026-06-18.md`
- `BRAIN/01-DIARIO/2026/2026-06-19.md`
- `BRAIN/01-DIARIO/2026/2026-06-22.md`
- `BRAIN/60-AGENTES/versionados/`
- `scripts/sync-agentes-versionados.py`


## Consolidação semanal

A rotina semanal está registrada em `BRAIN/99-SISTEMA/ROTINA-CONSOLIDACAO.md` e foi executada pela primeira vez em 2026-06-14, gerando `BRAIN/01-DIARIO/Semanal/2026-W24.md`.

Princípios reforçados:

- Revisar apenas daily notes disponíveis dos últimos 7 dias.
- Elevar aprendizados para notas permanentes somente quando houver utilidade futura.
- Arquivar sem relevância quando existir material sem conexão ou prioridade.
