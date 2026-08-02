# Capacidade tecnica nao substitui evidencia de ambiente

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W31
confiabilidade: alta
ultima_revisao: 2026-08-02
tags: [provider, cloud, evidencia, management-plane, read-only, selecao]
```

## Principio

Um provedor pode ter capacidade tecnica oficial para resolver um problema e ainda assim nao estar operacionalmente disponivel para o caso concreto. Se faltam conta, tenant, subscription, projeto, dono aprovado, permissao e trilha de auditoria, a capacidade permanece teorica.

## Aplicacao pratica

- Separar matriz de capacidade de evidencia de ambiente existente.
- Antes de selecionar provider, confirmar por leitura autorizada a existencia do ambiente e seu owner.
- Registrar gaps como `sem superficie disponivel` ou `parcialmente coberto`, sem completar por inferencia.
- Nao escolher por empate aparente quando o bloqueio real e falta de evidencia local.
- Manter credenciais, IDs sensiveis e inventarios brutos fora do Brain/Git; registrar apenas estado sanitizado.

## Exemplo conectado

Na semana 2026-W31, AWS, Azure e Google Cloud cobriam tecnicamente os gaps de cloud/VM, firewall/roteamento, replicacao/snapshot/clone, cleanup/descarte e rollback. Ainda assim, nenhum provider foi selecionado porque nao havia evidencia local de conta, tenant, subscription ou projeto existente e aprovado.

## Relacoes

- `BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md`
- `BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md`
- `BRAIN/01-DIARIO/Semanal/2026-W31.md`
