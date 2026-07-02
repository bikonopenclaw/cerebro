#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

FORBIDDEN = [
    r'\bOpenClaw\b', r'\bPuppet Master\b', r'\bKowalski\b',
    r'\bDarth Vader\b', r'\bRobotnik\b', r'\bagente\b', r'\bbot\b',
    r'file://', r'/data/\.openclaw', r'/tmp/', r'localhost:',
    r'__pycache__', r'\.env\b', r'token\s*[:=]', r'senha\s*[:=]',
    r'api[_-]?key\s*[:=]', r'client_secret\s*[:=]',
]
REQUIRED_HINTS = [r'Bikon', r'(Hebert Mattedi|Felipe Nogueira|Bikon Tecnologia)']


def read_text(path: Path) -> str:
    data = path.read_bytes()
    if b'\0' in data[:4096]:
        raise SystemExit('ERRO: arquivo parece binário. Valide PDF exportando texto antes ou revise visualmente.')
    return data.decode('utf-8', errors='replace')


def main() -> int:
    ap = argparse.ArgumentParser(description='Valida sujeira operacional em relatório Bikon Markdown/HTML/TXT')
    ap.add_argument('arquivo')
    args = ap.parse_args()
    path = Path(args.arquivo)
    if not path.exists():
        raise SystemExit(f'ERRO: arquivo não encontrado: {path}')
    text = read_text(path)

    errors: list[str] = []
    warnings: list[str] = []

    for pat in FORBIDDEN:
        if re.search(pat, text, flags=re.I):
            errors.append(f'conteúdo proibido ou operacional encontrado: {pat}')

    if '—' in text or '–' in text:
        errors.append('travessão encontrado. Use ponto, vírgula ou parênteses.')

    for pat in REQUIRED_HINTS:
        if not re.search(pat, text, flags=re.I):
            warnings.append(f'indício obrigatório não encontrado: {pat}')

    if not re.search(r'(cliente|empresa|organização|organizacao)', text, flags=re.I):
        warnings.append('não encontrei indicação clara de cliente/empresa/organização')
    if not re.search(r'(período|periodo|data|emitido em|analisado em)', text, flags=re.I):
        warnings.append('não encontrei indicação clara de data ou período')

    if errors:
        print('REPROVADO')
        for e in errors:
            print(f'- ERRO: {e}')
        for w in warnings:
            print(f'- AVISO: {w}')
        return 2

    print('APROVADO COM AVISOS' if warnings else 'APROVADO')
    for w in warnings:
        print(f'- AVISO: {w}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
