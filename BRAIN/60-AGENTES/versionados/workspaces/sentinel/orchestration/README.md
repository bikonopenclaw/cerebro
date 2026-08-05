# Gate de orquestração Sentinel

Este controlador é o ponto único de entrada para execução crítica do Sentinel.
Mensagem em fila não autoriza trabalho por si só.

Fluxo obrigatório:

1. Puppet Master registra a ordem com `activate`.
2. `activate` exige `supersedes` igual à última ordem terminal, mantém uma única
   ordem ativa e pausa os crons não críticos.
3. Sentinel lê o arquivo e responde com `ack`, repetindo caminho, SHA-256,
   approval ID e execution ID.
4. Puppet Master valida o ACK. Só então `start` pode emitir
   `technical_started_at` e iniciar o lease.
5. Antes de GET, consumo de approval, criação de artefato de execução ou outra
   ação técnica, Sentinel executa `assert` com os mesmos bindings. `assert`
   autoriza somente estado `RUNNING` com lease válido.
6. `close` encerra a ordem, restaura somente os crons que estavam habilitados e
   deixa o resultado como referência obrigatória do próximo `supersedes`.

`STOP` sempre prevalece. Ordem sem registro, com hash divergente, antiga, sem
ACK ou com IDs diferentes fecha em rejeição local, sem ação técnica.

## Travas de produção

- Estado, configuração de cron e runner são fixos nos caminhos canônicos.
- `--state-dir`, `--cron-config`, `--dry-run-cron` e variáveis
  `SENTINEL_ORCHESTRATION_*` não podem desviar a produção.
- Overrides existem somente com `--test-mode`, sob diretório temporário e com
  runner double explícito.
- `renew` renova o lease de uma ordem `RUNNING`.
- `recover` encerra fail-closed uma ordem `RUNNING` com lease expirada.
- `stop --requested-by Hebert|PuppetMaster --reason ...` prevalece sobre o
  fluxo normal e restaura o snapshot de cron.
- Cada disable/enable de cron é consultado novamente e auditado.

## Cliente NinjaOne

O cliente `integrations/ninjaone/ninjaone_readonly.py` exige os cinco bindings:

- `--order-id`;
- `--order-path`;
- `--order-sha256`;
- `--approval-id`;
- `--execution-id`.

O binding é validado antes de ler a credencial, antes de pedir o token e antes
de cada chamada externa. Ausência, ordem velha, STOP, lease expirada ou estado
diferente de `RUNNING` falha antes da rede.

Controlador:

`/data/.openclaw/workspace-sentinel/orchestration/orchestrationctl.py`

Estado:

`/data/.openclaw/workspace-sentinel/orchestration/state/controller-state.json`

Auditoria append-only encadeada:

`/data/.openclaw/workspace-sentinel/orchestration/state/audit.jsonl`
