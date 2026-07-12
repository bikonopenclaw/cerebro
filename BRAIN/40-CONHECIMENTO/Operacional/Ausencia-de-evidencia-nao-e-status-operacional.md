# Ausência de evidência não é status operacional

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W28
confiabilidade: alta
ultima_revisao: 2026-07-12
tags: [monitoramento, evidencia, ninjaone, backup, hyper-v, operacao]
```

## Princípio

Quando uma ferramenta operacional não expõe dado explícito, a conclusão correta é "sem evidência consultável", não sucesso presumido nem falha confirmada.

## Aplicação prática

- Em monitoramento, diferenciar ausência de job, alerta, atividade ou custom field de falha real.
- Não afirmar que backup, replicação, atualização ou remediação está OK sem campo, log, job ou evento oficial.
- Registrar a lacuna de instrumentação como pendência quando a informação for necessária para decisão.
- Criar integração, monitor, script ou custom field específico quando o dado precisa ser acompanhado de forma recorrente.

## Exemplo conectado

Em 2026-07-07, o NinjaOne expôs inventário, conectividade, volumes, alertas e atividades de `HOST1 | Magnitos Granitos`, mas não expôs conclusão de backup nem status de Hyper-V replication. O status correto foi registrar ausência de evidência e apontar instrumentação necessária.

## Relações

- `BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md`
- `BRAIN/60-AGENTES/KOWALSKI.md`
- `BRAIN/20-EMPRESAS/BIKON/README.md`
