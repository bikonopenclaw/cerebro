# Validação do runtime pós-migração

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W29
confiabilidade: alta
ultima_revisao: 2026-07-17
tags: [openclaw, migracao, runtime, scheduler, skills, readiness, rollback]
```

## Princípio

Arquivo restaurado não comprova carregamento, configuração válida nem execução. Uma migração só termina quando o runtime ativo descobre, executa e preserva os componentes esperados depois de restart controlado.

## Gate mínimo

1. Confirmar versão alinhada entre CLI e serviços.
2. Confirmar supervisor, unit e state dir realmente usados.
3. Validar rotas ativas de workspaces, skills e configurações.
4. Confirmar skills indexadas, não apenas presentes em disco.
5. Validar armazenamento do scheduler, jobs habilitados, `nextWake`, vencidos/em execução e erros consecutivos.
6. Executar provas read-only ou canários permitidos para confirmar funcionamento real.
7. Verificar canal, RPC, portas e exposição esperada.
8. Fazer restart controlado e repetir o readiness para provar persistência.

## Separação de mudanças

Upgrade, plugin, modelo/configuração, porta, restart e recuperação de backlog são categorias distintas. Não misturar para ganhar tempo. No primeiro erro de versão, migração, plugin ou supervisor, parar e restaurar o último estado conhecido antes de escolher outra rota.

## Backlog

Antes de reiniciar ou reabrir canais, inspecionar jobs vencidos, em execução e filas pendentes. Depois da recuperação, deduplicar por identificador e responder apenas ao pedido mais recente quando mensagens antigas já foram superadas.

## Relações

- `BRAIN/50-PROJETOS/Planejamento/Migracao-Hostinger-VPS-OpenClaw.md`
- `BRAIN/70-AUTOMACOES/openclaw-crons/README-verificacao-crons.md`
- `BRAIN/01-DIARIO/Semanal/2026-W29.md`
