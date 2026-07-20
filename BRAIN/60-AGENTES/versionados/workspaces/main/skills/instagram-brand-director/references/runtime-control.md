# Controle de runtime

## Estado

Guardar `campaign.json` validado por schema e `events.jsonl` append-only. Usar lock exclusivo, versão monotônica, escrita atômica, fsync e rename.

Cada evento registra event_id, correlation_id, actor, action, object, result, approval_reference, before_hash, after_hash, timestamp UTC e evidência sanitizada.

## Operações externas

Criar `operation-request.json` canônico e SHA-256. O adapter recusa hash divergente, aprovação ausente/vencida/usada, destino diferente, custo acima do teto ou estado incompatível.

## Modos

- advisory: estratégia e preparação local.
- production: adapters reais liberados após preflight.

Não existe fallback automático. A indisponibilidade mantém o estado seguro e exige decisão.

## Segredos

Usar secret store ou variáveis do serviço. Registrar somente nomes de referência. Sanitizar logs e respostas.