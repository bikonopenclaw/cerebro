# Contrato de runtime reproduzivel

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W31
confiabilidade: alta
ultima_revisao: 2026-08-02
tags: [runtime, python, reproducibilidade, checksums, supply-chain, drift]
```

## Principio

Runtime operacional nao deve depender de caminho conveniente, instalacao local implicita ou descricao historica ambigua. O contrato precisa permitir reconstruir, auditar e detectar drift.

## Campos minimos

- Sistema operacional e arquitetura.
- Nome e versao final do runtime.
- Caminho absoluto do executavel usado em operacao.
- Origem do artefato e metodo de provisionamento.
- SHA-256 do executavel e, quando aplicavel, hash da arvore instalada.
- Versoes auxiliares relevantes, como Unicode no caso de CPython.
- Regra de drift: o que invalida o runtime e exige novo freeze.

## Aplicacao pratica

- Diferenciar evidencia historica de contrato futuro.
- Nao promover caminho de ambiente local a requisito operacional sem decisao documental.
- Validar o runtime pelo caminho absoluto congelado, nao por `python3` resolvido pelo shell.
- Registrar correcoes de contrato como alteracao documental propria, com novo hash e validacao independente.

## Exemplo conectado

Em 2026-W31, o contrato futuro do Provimento 213 foi alinhado ao CPython `3.14.6` final em `/opt/openclaw/runtimes/cpython-3.14.6/bin/python3`, com Unicode `16.0.0`, hash de executavel e hash de arvore instalada. A referencia historica a `/opt/homebrew/bin/python3` permaneceu evidencia antiga, nao contrato operacional futuro.

## Relacoes

- `BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git.md`
- `BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md`
- `BRAIN/01-DIARIO/Semanal/2026-W31.md`
