# Regra de segurança para crons OpenClaw

Antes de criar ou alterar cron, rodar o verificador:

```bash
python3 /data/.openclaw/workspace/scripts/verificar_crons_sobrepostos.py
```

Para validar um candidato antes de criar:

```bash
python3 /data/.openclaw/workspace/scripts/verificar_crons_sobrepostos.py \
  --candidate-name "Novo cron" \
  --candidate-expr "15 0 * * 2-5" \
  --candidate-tz America/Sao_Paulo
```

Regras:

- Mesmo minuto = bloqueio.
- Coletas e jobs pesados próximos = alerta.
- Envios por cache das 08h são leves e podem ficar com intervalo de 1 minuto.
- Se houver bloqueio, não criar nem alterar cron sem corrigir.

Última auditoria após ajuste do Brain para 22h: 0 bloqueios e 0 alertas.
