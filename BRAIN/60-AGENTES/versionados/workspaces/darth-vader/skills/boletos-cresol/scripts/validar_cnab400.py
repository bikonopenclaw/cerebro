#!/usr/bin/env python3
import argparse
from pathlib import Path


def split_lines_preserve(path: Path):
    raw = path.read_bytes()
    text = raw.decode('latin-1')
    return text.splitlines()


def validar(path: Path):
    linhas = split_lines_preserve(path)
    erros = []
    avisos = []
    if not linhas:
        erros.append('arquivo vazio')
        return erros, avisos, linhas
    for idx, linha in enumerate(linhas, 1):
        if len(linha) != 400:
            erros.append(f'linha {idx}: tamanho {len(linha)} diferente de 400')
    tipos = [linha[:1] for linha in linhas if linha]
    if tipos[0] != '0':
        erros.append(f'primeiro registro deve ser 0/header, veio {tipos[0]!r}')
    if tipos[-1] != '9':
        erros.append(f'último registro deve ser 9/trailer, veio {tipos[-1]!r}')
    detalhes = [t for t in tipos if t == '1']
    if not detalhes:
        erros.append('arquivo sem registro detalhe tipo 1')
    invalidos = sorted(set(t for t in tipos if t not in {'0', '1', '9'}))
    if invalidos:
        erros.append(f'tipos de registro inválidos: {invalidos}')
    if len(linhas) < 3:
        erros.append('arquivo CNAB400 de remessa deve ter header, ao menos 1 detalhe e trailer')
    if tipos.count('0') != 1:
        avisos.append(f'quantidade de headers tipo 0: {tipos.count("0")}')
    if tipos.count('9') != 1:
        avisos.append(f'quantidade de trailers tipo 9: {tipos.count("9")}')
    return erros, avisos, linhas


def main():
    ap = argparse.ArgumentParser(description='Valida estrutura básica CNAB400 Cresol')
    ap.add_argument('arquivo')
    args = ap.parse_args()
    path = Path(args.arquivo)
    erros, avisos, linhas = validar(path)
    print(f'arquivo={path}')
    print(f'linhas={len(linhas)}')
    if linhas:
        print('tipos=' + ''.join(l[:1] for l in linhas))
    for aviso in avisos:
        print('AVISO:', aviso)
    if erros:
        for erro in erros:
            print('ERRO:', erro)
        raise SystemExit(1)
    print('OK: estrutura CNAB400 básica válida')


if __name__ == '__main__':
    main()
