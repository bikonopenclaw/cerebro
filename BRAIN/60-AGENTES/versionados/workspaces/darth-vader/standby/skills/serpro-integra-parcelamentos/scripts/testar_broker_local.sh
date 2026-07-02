#!/usr/bin/env bash
set -euo pipefail
BROKER_URL="${BROKER_URL:-http://127.0.0.1:8766}"
KEY_HEADER=()
if [[ -n "${BROKER_LOCAL_API_KEY:-}" ]]; then
  KEY_HEADER=(-H "X-Broker-Key: ${BROKER_LOCAL_API_KEY}")
fi

echo "== health =="
curl -sS "${KEY_HEADER[@]}" "$BROKER_URL/health"
echo

echo "== token, mascarado =="
RESP=$(curl -sS "${KEY_HEADER[@]}" "$BROKER_URL/token")
BROKER_RESP="$RESP" python3 - <<'PY'
import json, os
obj=json.loads(os.environ['BROKER_RESP'])
print('ok=', obj.get('ok'))
if not obj.get('ok'):
    print('error=', obj.get('error'))
    raise SystemExit(1)
tok=obj.get('token') or {}
for k,v in tok.items():
    if 'token' in k.lower() and isinstance(v,str):
        print(k, '=', v[:8] + '...' + v[-6:] if len(v) > 18 else '***')
    else:
        print(k, '=', v)
PY
