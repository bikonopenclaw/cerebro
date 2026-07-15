# Verificação de segurança de crons

Arquivo principal:

```bash
/data/.openclaw/workspace/scripts/verificar_crons_sobrepostos.py
```

Uso padrão antes de criar ou alterar cron:

```bash
python3 /data/.openclaw/workspace/scripts/verificar_crons_sobrepostos.py
```

Validar um novo cron antes de criar:

```bash
python3 /data/.openclaw/workspace/scripts/verificar_crons_sobrepostos.py \
  --candidate-name "Nome do novo cron" \
  --candidate-expr "15 0 * * 2-5" \
  --candidate-tz America/Sao_Paulo
```

Regras:

- Mesmo minuto = bloqueio.
- Coletas e jobs pesados próximos demais = alerta.
- Envios por cache das 08h são tratados como leves e podem ficar em intervalo de 1 minuto.
- Exit code `1` significa que existe bloqueio e o agendamento não deve ser criado/alterado sem corrigir.

Regra operacional: antes de qualquer novo cron ou ajuste de cron, rodar esta verificação e não seguir se houver bloqueio.

## Validação pós-migração ou upgrade

Em 2026-07-15, a revisão da VPS encontrou 33 jobs preservados no banco, mas o scheduler apontava para o caminho legado `/home/openclaw/.openclaw/cron/jobs.json`. A instância atual usa `/data/.openclaw/cron/jobs.json` e estado SQLite.

Após migração, upgrade ou restauração, validar em conjunto:

- caminho de armazenamento exibido pelo scheduler;
- quantidade total de jobs e distribuição por agente;
- jobs habilitados versus desabilitados;
- presença de `nextWake` futuro;
- jobs vencidos ou marcados como em execução;
- `lastRunStatus`, `consecutiveErrors` e motivo do último erro.

Inventário restaurado não equivale a agenda saudável. Na correção de 2026-07-15, 33 jobs voltaram a aparecer habilitados, mas 11 ficaram com último status de erro após restart do gateway, timeout ou aborto. A validação só termina quando as execuções seguintes concluírem sem erro ou quando cada falha tiver tratamento explícito.

Evitar restart do gateway durante disparo de backlog. Reinícios nessa janela podem interromper jobs e transformar uma correção de armazenamento em falha simultânea de automações.
