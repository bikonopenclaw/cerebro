#!/usr/bin/env python3

# Local skill path and vendored dependencies
import sys as _sys
from pathlib import Path as _Path
_skill_root = _Path(__file__).resolve().parent.parent
_vendor = _skill_root / 'vendor'
for _p in (_skill_root, _vendor):
    if _p.exists() and str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

"""Cadastro simples de clientes para emissão em lote."""
import argparse, json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Cadastrar cliente no data/clientes.json')
    parser.add_argument('--documento', help='CPF ou CNPJ do tomador, detectado automaticamente')
    parser.add_argument('--cpf', help='CPF do tomador pessoa física')
    parser.add_argument('--cnpj', help='CNPJ do tomador pessoa jurídica, mantido por compatibilidade')
    parser.add_argument('--nome', required=True)
    parser.add_argument('--email', default='')
    parser.add_argument('--codigo', required=True, help='Código LC 116')
    parser.add_argument('--descricao', required=True)
    parser.add_argument('--valor', type=float, required=True)
    parser.add_argument('--aliquota', type=float, default=0)
    args = parser.parse_args()
    documento = args.documento or args.cpf or args.cnpj
    if not documento:
        parser.error('informe --documento, --cpf ou --cnpj')
    digits = ''.join(ch for ch in documento if ch.isdigit())
    if len(digits) == 11:
        args.cpf = digits
        args.cnpj = None
    elif len(digits) == 14:
        args.cnpj = digits
        args.cpf = None
    else:
        parser.error('documento inválido: CPF deve ter 11 dígitos e CNPJ 14 dígitos')
    args.documento = digits
    base = Path(__file__).parent.parent / 'data'
    base.mkdir(exist_ok=True)
    path = base / 'clientes.json'
    clientes = []
    if path.exists():
        clientes = json.loads(path.read_text(encoding='utf-8') or '[]')
    clientes.append(vars(args))
    path.write_text(json.dumps(clientes, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Cliente cadastrado em {path}: {args.nome}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
