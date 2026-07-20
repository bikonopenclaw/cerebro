# Publicação e aprendizado

Buffer é o único escritor do estado de publicação.

## Payload

Fixar account_id, organization_id, channel_id, profile_id, campaign_id, asset_id, version, media_hash, legenda, alt text, horário UTC, fuso e action.

## Ações

`dry-run`, `create-draft`, `schedule`, `publish`, `edit` e `delete` têm requests e aprovações independentes.

Consultar destino e idempotency_key antes. Depois, registrar ID remoto, estado e resposta sanitizada. Não repetir automaticamente.

Publicação é irreversível. Editar ou excluir exige nova autorização. Falha mantém estado seguro e abre incidente de compensação.

## Métricas

Registrar janela, alcance, impressões, visualizações, retenção, conclusão, salvamentos, compartilhamentos, comentários, cliques, conversão, crescimento, custo e limitações. Separar fato de hipótese.