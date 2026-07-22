# Event Sourcing

\`events.jsonl\` é append-only. Cada linha contém:

- event_id, event_type e stream_version;
- correlation_id, campaign_id e asset_id;
- timestamp UTC e ator;
- ação, resultado e detalhe sanitizado;
- before_hash e after_hash quando houver projeção;
- prev_event_hash;
- event_hash calculado sobre o evento sem o próprio hash.

## Invariantes

- lock exclusivo durante leitura do head e append;
- stream_version cresce em um;
- primeiro evento usa prev_event_hash vazio;
- nenhuma edição ou exclusão;
- correção é novo evento;
- evento inválido bloqueia replay e ação externa;
- segredo nunca entra em detail;
- projeção pode ser reconstruída dos eventos;
- resultado externo deve virar evento antes do retorno do adapter.

\`scripts/event_store.py verify\` valida JSON, sequência e hash chain. \`replay\` gera uma projeção sem reescrever o stream.
