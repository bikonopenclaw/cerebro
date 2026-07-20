# Fluxo de campanha

## Estados

`intake`, `brief-pending`, `brief-approved`, `research-pending`, `research-ready`, `strategy-pending`, `strategy-approved`, `creative-pending`, `creative-approved`, `generation-authorization-pending`, `generation-submitted`, `generation-ready`, `asset-selected`, `composition-pending`, `composition-ready`, `qa-pending`, `qa-failed`, `final-approval-pending`, `final-approved`, `draft-authorization-pending`, `draft-created`, `schedule-authorization-pending`, `scheduled`, `publish-authorization-pending`, `published`, `measurement-pending`, `measured`, `blocked`, `failed`, `cancelled`, `archived`.

Somente o controlador de estado pode transicionar. Não pular aprovação.

## Aprovação

Registrar portão, decisão, actor_id, chat_id, message_id, timestamp UTC, validade, ressalvas, operation, request_hash e used_at.

Uma aprovação é de uso único e autoriza somente o JSON canônico do hash. Qualquer mudança cria nova versão e nova aprovação.

## Idempotência

Chave: `campaign_id:asset_id:operation:version`. Antes de executar, retornar resultado concluído ou retomar pelo ID existente. Nunca duplicar gasto ou publicação.

## Falhas

Usar `blocked` para dependência ou decisão ausente, `failed` para execução encerrada com erro e `cancelled` por decisão humana. Registrar evento de compensação ou rollback sem apagar o evento original.