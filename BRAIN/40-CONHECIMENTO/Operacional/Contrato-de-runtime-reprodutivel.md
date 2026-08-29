# Contrato de runtime reproduzivel

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W31; bootstrap RSE M2 em 2026-08-28/29
confiabilidade: alta
ultima_revisao: 2026-08-29
tags: [runtime, python, reproducibilidade, checksums, supply-chain, drift, cgroup, executor, lifecycle]
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
- Em execucoes longas, provar PID, tmux/unit real, cgroup efetivo e limites lidos do processo; o nome ou scope planejado nao comprova onde o workload esta rodando.
- Separar durabilidade do trabalho da vida da conversa/control-plane: clone, checkpoints, logs e identidade precisam sobreviver ao encerramento do turno.
- Nao declarar isolamento de recursos quando o scope limitado esta inativo e o processo real pertence a outro cgroup.

## Exemplo conectado

Em 2026-W31, o contrato futuro do Provimento 213 foi alinhado ao CPython `3.14.6` final em `/opt/openclaw/runtimes/cpython-3.14.6/bin/python3`, com Unicode `16.0.0`, hash de executavel e hash de arvore instalada. A referencia historica a `/opt/homebrew/bin/python3` permaneceu evidencia antiga, nao contrato operacional futuro.

No bootstrap RSE M2 de 2026-08-28/29, uma continuacao direta caiu quando o scope pai do OpenClaw terminou. O tmux persistente preservou o trabalho, mas a auditoria mostrou que o executor real estava em `session-3.scope`, nao no scope limitado reportado. O aprendizado e verificar o cgroup efetivo do processo antes de afirmar durabilidade ou resource envelope.

## Relacoes

- `BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git.md`
- `BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md`
- `BRAIN/01-DIARIO/Semanal/2026-W31.md`
