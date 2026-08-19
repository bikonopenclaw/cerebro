# Pacote selado auto-reprodutivel antes de privilegio operacional

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W33 e Portal 213 Stage 1B R2.3
confiabilidade: alta
ultima_revisao: 2026-08-19
tags: [pacote, hash, rollback, preflight, root, producao, provimento-213]
```

## Principio

Antes de qualquer etapa com privilegio operacional, o pacote selado precisa provar que e auto-reprodutivel a partir dos proprios bytes. Narrativa, runbook, manifesto ou marcador `PASS` nao bastam se o artefato nao exercita controller, plano, hashes, preflight, canary, ledger e rollback de forma verificavel.

O pacote preparatorio deve falhar antes da ativacao real, nao durante ela.

## Aplicacao pratica

- Validar o hash esperado do pacote e recalcular planos a partir dos bytes selados.
- Exercitar o mesmo engine transacional em backend fake e, quando autorizado, live.
- Testar rollback, preflight, canary e ataques/adversarial cases sem mutacao real quando o escopo for preparatorio.
- Em scripts que poderao rodar com privilegio, exercitar sinais durante rollback, reentrada de fail/rollback, verificacao final de systemd, residuos de segredo temporario, diretorios pais criados na rodada e classificacao real de pacote interrompido.
- Bloquear root, servico, Telegram, DNS/TLS/proxy e producao se o artefato nao for aceito pelo proprio controller.
- Tratar correcao do pacote como nova unidade versionada, com novo hash e nova validacao.

## Exemplo conectado

No Portal 213, o Stage 1A.3 supersedido falhou porque o artefato selado nao era aceito pelo proprio controller como delivery bundle e divergia da matriz de rollback. O Stage 1A.3-R1 corrigiu o controller transacional futuro, validou hashes, plano, release binding e rollback offline/read-only, mas continuou sem autorizar Stage 1B/1C ou ativacao real.

Em 2026-08-19, o Portal 213 Stage 1B R2.3 reforcou o mesmo principio em formato de comando local canary root: o artefato novo foi validado por diff exato, `bash -n`, compilacao de heredocs Python, fixtures de sinais, rollback systemd, pais `/opt`, apt parcial, evidence path e segredo temporario, com root/sudo/systemctl/apt/producao `0`. O `PASS` continua preparatorio e nao autoriza execucao real.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel|Contrato de runtime reprodutivel]]
- [[40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado|Validacao do caminho final instalado]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[01-DIARIO/Semanal/2026-W33|Semana 2026-W33]]
