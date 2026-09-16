# Estado terminal requer convergencia do lifecycle

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W35, teste controlado de relatorios operacionais em 2026-09-02, publicacao Instagram Bikon em 2026-09-10 e lifecycle ad-hoc ARX em 2026-09-16
confiabilidade: alta
ultima_revisao: 2026-09-16
tags: [lifecycle, execucao, registry, cgroup, terminalidade, reconciliacao, supervisao, transcript]
```

## Principio

Uma execucao so e terminal quando fila, admissao, registry, child, processo fisico e evidencias persistidas convergem para a mesma identidade e para um unico resultado. Estado terminal em apenas uma camada nao prova encerramento do workload.

## Aplicacao pratica

- Criar a identidade duravel antes do child ou do processo fisico.
- Registrar transicoes `accepted -> admitted/deferred -> spawned -> bootstrapped -> workload_started -> output_committed -> terminal`.
- Vincular fila, registry, PID, unit/tmux, cgroup e checkpoint ao mesmo execution ID.
- Considerar terminalidade invalida quando o cgroup canonico ainda possui processo vivo, os bytes continuam mudando ou falta reconciliacao do output.
- Preservar historico factual: lease expirada ou admissao stale nao deve ser reescrita como cancelamento que nao ocorreu.
- Depois de perda de sessao ou gateway, reconciliar a mesma execucao; nao criar retry concorrente por ausencia de observador.
- Tratar transcript e chat como superficies de observacao, nao como fonte terminal; reconstruir o estado pelo registry duravel, checkpoints, artefatos e fila de anuncio.
- Distinguir heartbeat de progresso significativo: apenas transicao de stage, tool concluida, artefato, checkpoint, handoff, gate aceito ou terminalidade avanca o relogio de progresso.
- Pressao transitoria (`EAGAIN`, `pthread_create`, capacidade do app-server) so admite retry limitado quando a operacao e segura, o efeito externo e conhecido e os checkpoints permanecem intactos.
- Quando o efeito externo já foi comprovado, falha posterior de readback, cleanup ou recibo não autoriza repetir o efeito; preservar o estado realizado e retomar somente as etapas idempotentes de fechamento.
- ACK e start sao transicoes duraveis da mesma identidade de execucao, nao mensagens conversacionais. Timeout deve persistir falha terminal e bloquear a request; nao autoriza criar sucessor, trocar rota ou iniciar efeito externo.

## Exemplo conectado

Em 2026-W35, RSE, ODP/B1 e o P1 de Relatorios Operacionais mostraram o mesmo defeito: child criado antes da admissao, caller bloqueado em espera e perda da sessao sem convergencia com registry e processo fisico. A retomada ficou bloqueada ate existir lifecycle canonico e prova terminal compartilhada.

No teste controlado de Relatorios Operacionais de 2026-09-02, um transcript incompleto aparentou stall depois que o Goal ja havia fechado `ACCEPTED`. A reconciliacao pelo supervisor e pelos artefatos duraveis evitou recoleta, regeneracao e reenvio, encerrando o alerta como falso stall.

Na publicação Instagram Bikon de 2026-09-10, o Graph confirmou o `media_id` e o permalink antes de o readback visual falhar por bloqueio do novo CDN. O estado correto permaneceu `PUBLISHED`, com fechamento local pendente; repetir `media_publish` seria duplicar um efeito externo já comprovado.

No request ARX/Cove ad-hoc de 2026-09-15/16, tentativas intermediarias nao autorizaram sucessores em loop. A reconciliacao reteve uma unica linhagem canonica, fechou `FAIL_CLOSED_EXTERNAL_OWNER_GATE` antes do provider e congelou a mesma request ate existirem binding numerico aprovado e gate de rede proprio.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|Ausencia de evidencia nao e status operacional]]
- [[40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel|Contrato de runtime reprodutivel]]
- [[40-CONHECIMENTO/Operacional/Governanca-de-capacidade-nao-e-roteamento-semantico|Governanca de capacidade nao e roteamento semantico]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-RSE|OpenClaw RSE]]
- [[70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM|Relatorios Operacionais Telegram]]
- [[70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK|Instagram Bikon Robotnik]]
- [[70-AUTOMACOES/ARX-BACKUP-NINJAONE|ARX Backup diario e tickets NinjaOne]]
- [[01-DIARIO/Semanal/2026-W35|Semana 2026-W35]]
- [[01-DIARIO/2026/2026-09-03|Diario 2026-09-03]]
- [[01-DIARIO/2026/2026-09-10|Diario 2026-09-10]]
