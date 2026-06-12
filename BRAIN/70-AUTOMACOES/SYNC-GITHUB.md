# Sync GitHub do Brain

## Objetivo

Sincronizar mudanças locais do Brain com o GitHub automaticamente 4x ao dia.

## Repositório

- Local: `/data/.openclaw/workspace/Brain`
- Remoto: `git@github.com:bikonopenclaw/cerebro.git`
- Branch: `main`

## Frequência

- 06:00 BRT
- 12:00 BRT
- 18:00 BRT
- 23:00 BRT

## Script

`scripts/sync-github.sh`

## Comportamento

1. Verifica se há mudanças locais.
2. Se houver, executa `git add -A` e `git commit`.
3. Executa `git push origin main`.
4. Se não houver mudanças, não cria commit vazio.

## Observação

Essa automação faz upload de mudanças locais. Não foi configurado pull automático para evitar conflito silencioso.
