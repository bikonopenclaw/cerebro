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
