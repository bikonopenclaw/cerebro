# Controle de runtime 2.1.0

## Estado

Eventos são a fonte da verdade. \`campaign.json\`, approval e asset manifests são projeções portáteis com escrita atômica e lock. \`events.jsonl\` é append-only, versionado e encadeado por SHA-256.

## Request

Toda mutação externa usa request canônico com campaign_id, asset_id, asset_version, operation, destination, tool, parameters, provider_kind e provider_id. O hash ignora apenas campos derivados. Qualquer mudança invalida o OK.

## Approval

Owner binding exige \`openclaw.inbound_meta.v2\`, sender, canal, chat, message ID, texto e UTC. Approval vincula proprietário, request, provider, ação, destino e versão.

Lifecycle:

- approved: pode ser validado;
- reserved: execution ID foi criado;
- executing: a tentativa começou;
- succeeded, failed ou indeterminate: encerrado e não reutilizável;
- revoked e consumed: terminais legados.

Reservar, iniciar e concluir são operações atômicas e geram eventos. Resultado externo não fica apenas em stdout.

## Providers e governance

Antes de adapter externo, verificar provider registry, actor registry, Governance Engine, stream íntegro e approval. Provider desabilitado bloqueia mesmo com approval.

## Falha fechada

Não trocar provider, fonte, ferramenta ou sequência. Não repetir mutation. Em indeterminate, consultar a operação original.
