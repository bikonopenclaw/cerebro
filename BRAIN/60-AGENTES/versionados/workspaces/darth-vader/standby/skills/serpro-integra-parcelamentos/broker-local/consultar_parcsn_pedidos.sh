#!/usr/bin/env bash
set -euo pipefail

BROKER_URL="${BROKER_URL:-http://127.0.0.1:8766}"
SERPRO_BASE_URL="${SERPRO_BASE_URL:-https://gateway.apiserpro.serpro.gov.br/integra-contador/v1}"
CNPJ="${CNPJ:-34191026000186}"
SERVICO="${SERVICO:-PEDIDOSPARC163}"
SISTEMA="${SISTEMA:-PARCSN}"
VERSAO="${VERSAO:-1.0}"
# Para PEDIDOSPARC163 o SERPRO retornou: remover campo dados.
# Valores: omit | empty_string | json_string
DADOS_MODE="${DADOS_MODE:-omit}"

curl_broker() {
  if [ -n "${BROKER_LOCAL_API_KEY:-}" ]; then
    curl -sS -H "X-Broker-Key: ${BROKER_LOCAL_API_KEY}" "$@"
  else
    curl -sS "$@"
  fi
}

echo "== pegando token local, sem imprimir token =="
TOKEN_JSON="$(curl_broker "$BROKER_URL/token")"
export TOKEN_JSON
read -r ACCESS_TOKEN JWT_TOKEN < <(python3 - <<'PY'
import json, os
obj=json.loads(os.environ['TOKEN_JSON'])
if not obj.get('ok'):
    print('ERRO_BROKER', obj.get('error','erro broker'))
    raise SystemExit(2)
tok=obj.get('token') or {}
print(tok.get('access_token',''), tok.get('jwt_token',''))
PY
)

if [ "$ACCESS_TOKEN" = "ERRO_BROKER" ] || [ -z "$ACCESS_TOKEN" ] || [ -z "$JWT_TOKEN" ]; then
  echo "ERRO: broker não retornou access_token e jwt_token completos." >&2
  exit 2
fi

echo "Token local OK. access_token e jwt_token recebidos, não serão exibidos."

PAYLOAD="$(python3 - <<PY
import json
cnpj='$CNPJ'
dados_mode='$DADOS_MODE'
pedido={
  'idSistema': '$SISTEMA',
  'idServico': '$SERVICO',
  'versaoSistema': '$VERSAO',
}
if dados_mode == 'empty_string':
    pedido['dados'] = ''
elif dados_mode == 'json_string':
    pedido['dados'] = '{}'
elif dados_mode != 'omit':
    raise SystemExit('DADOS_MODE inválido: ' + dados_mode)
body={
  'contratante': {'numero': cnpj, 'tipo': 2},
  'autorPedidoDados': {'numero': cnpj, 'tipo': 2},
  'contribuinte': {'numero': cnpj, 'tipo': 2},
  'pedidoDados': pedido,
}
print(json.dumps(body, ensure_ascii=False))
PY
)"

echo "== consulta segura =="
echo "Endpoint: ${SERPRO_BASE_URL}/Consultar"
echo "Serviço: ${SISTEMA} ${SERVICO}"
echo "DADOS_MODE: ${DADOS_MODE}"
echo "CNPJ: ${CNPJ:0:2}.***.***/****-${CNPJ:12:2}"

tmp_body="$(mktemp)"
tmp_headers="$(mktemp)"
cleanup() { rm -f "$tmp_body" "$tmp_headers"; }
trap cleanup EXIT

HTTP_CODE="$(curl -sS -o "$tmp_body" -D "$tmp_headers" -w '%{http_code}' \
  -X POST "${SERPRO_BASE_URL}/Consultar" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "jwt_token: ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")"

echo "HTTP_CODE=$HTTP_CODE"
echo "== resposta resumida e mascarada =="
python3 - <<'PY' "$tmp_body"
import json, re, sys
from pathlib import Path
text=Path(sys.argv[1]).read_text(errors='replace')
text=re.sub(r'\b(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})\b', r'\1.***.***/****-\5', text)
try:
    obj=json.loads(text)
except Exception:
    print(text[:2000])
    raise SystemExit(0)
print('tipo=', type(obj).__name__)
if isinstance(obj, dict):
    print('chaves=', ', '.join(list(obj.keys())[:20]))
    for key in ['status','title','detail','type','instance','mensagem','codigo','descricao','dados','mensagens']:
        if key in obj:
            val=obj[key]
            if key == 'dados' and isinstance(val, str) and len(val) > 1200:
                val = val[:1200] + '...'
            print(f'{key}=', str(val)[:1600])
    sample=json.dumps(obj, ensure_ascii=False)[:2000]
    print('amostra=', sample)
else:
    print(json.dumps(obj, ensure_ascii=False)[:2000])
PY
