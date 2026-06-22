# API Cove / ARX Backup JSON-RPC

## Fontes oficiais

- Como usar o schema JSON-RPC: `https://developer.n-able.com/n-able-cove/docs/how-to-use-the-backup-manager-json-rpc-api-schema`
- Como montar chamada JSON-RPC: `https://developer.n-able.com/n-able-cove/docs/construct-a-json-rpc-api-call`
- Schema oficial: `https://documentation.n-able.com/covedataprotection/Schema_23.3.json`

Observação oficial importante: o schema lista métodos e parâmetros suportados, mas não gera cliente automaticamente. O client local precisa montar as chamadas manualmente.

## Endpoint

`https://api.backup.management/jsonapi`

## Credenciais locais

Arquivo seguro:
`/data/.openclaw/workspace-kowalski/arx-backup/config/.env`

Campos usados:

- `ARX_BACKUP_JSONRPC_URL=https://api.backup.management/jsonapi`
- `ARX_BACKUP_PARTNER=<valor configurado no .env>`
- `ARX_BACKUP_USERNAME=OpenClaw`
- `ARX_BACKUP_TOKEN` ou `ARX_BACKUP_PASSWORD`

Nunca imprimir token, password ou visa.

## Login validado

Método: `Login`

Parâmetros:

```json
{
  "partner": "<valor configurado no .env>",
  "username": "OpenClaw",
  "password": "<redacted>"
}
```

Resultado validado:

- PartnerId raiz: `2572200`
- Login: OK
- Flags do usuário: `SecurityOfficer`, `NonInteractive`

## Padrão de chamada confirmado pela documentação

Após o login, usar o `visa` retornado nas próximas chamadas:

```json
{
  "jsonrpc": "2.0",
  "visa": "<redacted>",
  "id": "jsonrpc",
  "method": "EnumerateAccountStatistics",
  "params": {
    "query": {
      "PartnerId": 2572200,
      "StartRecordNumber": 0,
      "RecordsCount": 500,
      "Columns": ["T3", "T4", "T7"]
    }
  }
}
```

A resposta vem em `result.result`, e os valores pedidos em `Settings`, como lista de objetos `{ "T3": "..." }`.

## Métodos úteis validados

### EnumerateColumns

Lista os códigos de coluna disponíveis.

```json
{
  "partnerId": 2572200
}
```

### EnumerateChildPartners

Funcionou com:

```json
{
  "partnerId": 2572200,
  "fields": null,
  "range": {"Offset": 0, "Size": 100},
  "partnerFilter": {}
}
```

Observação: `range` precisa de `Offset` e `Size`. `Count` não trouxe `Children`.

### EnumerateAccounts

Funciona por partner filho.

```json
{
  "partnerId": 2668228
}
```

Atenção: a resposta pode trazer `Password` e `Token` de conta/dispositivo. Sanitizar sempre.

### EnumerateAccountStatistics

Método principal para relatório.

```json
{
  "query": {
    "PartnerId": 2572200,
    "Filter": "",
    "ExcludedPartners": [],
    "SelectionMode": "Merged",
    "Labels": [],
    "StartRecordNumber": 0,
    "RecordsCount": 500,
    "OrderBy": "AR ASC, AN ASC",
    "Columns": ["AR", "AN", "AL", "MN", "PN", "TS", "T0", "T3", "T4", "T7", "TB", "TL", "TQ", "TJ", "TO", "TK", "F0", "FL", "F7", "FB", "FJ", "FO", "S0", "SL", "S7", "SB", "SJ", "SO", "Q0", "QL", "Q7", "QB", "QJ", "QO", "H0", "HL", "H7", "HB", "HJ", "HO", "W0", "WL", "W7", "WB", "WJ", "WO"],
    "Totals": ["T3", "T4", "T7"]
  },
  "totalStatistics": {}
}
```

## Códigos de colunas principais

- `AR`: cliente
- `AN`: dispositivo
- `MN`: nome do computador
- `PN`: produto/política de retenção
- `T0`: status total
- `I78`: fontes de dados ativas
- `T1`: total de arquivos/itens na seleção
- `T3`: tamanho selecionado total
- `T4`: tamanho processado total
- `T6`: tamanho protegido total
- `T7`: erros totais
- `TB`: barra de cores/status dos últimos 28 dias do total. Usar para desenhar histórico mensal real, nunca hardcoded.
- `TL`: último sucesso total
- `TJ`: status da última sessão concluída
- `TO`: horário da última sessão concluída
- `F*`: Arquivos e Pastas, incluindo `F1/F3/F6` para seleção/volume e `FB` para barra de 28 dias
- `S*`: System State, incluindo `S1/S3/S6` para seleção/volume e `SB` para barra de 28 dias
- `Q*`: MS SQL, incluindo `Q1/Q3/Q6` para seleção/volume e `QB` para barra de 28 dias
- `H*`: Hyper-V, incluindo `H1/H3/H6` para seleção/volume e `HB` para barra de 28 dias
- `W*`: VMware, incluindo `W1/W3/W6` para seleção/volume e `WB` para barra de 28 dias
- `AA3135` / `AA3308`: possíveis colunas customizadas `_SimpSelectionFS` / `_SelectionFS` para seleção literal de arquivos/pastas. Usar somente se vierem preenchidas.

## Legenda oficial de status

- `1`: InProcess, em processo
- `2`: Failed, falhou
- `3`: Aborted, abortado
- `5`: Completed, concluído
- `6`: Interrupted, interrompido
- `7`: NotStarted, não iniciado
- `8`: CompletedWithErrors, concluído com erros
- `9`: InProgressWithFaults, em progresso com falhas
- `10`: OverQuota, acima da cota
- `11`: NoSelection, sem seleção
- `12`: Restarted, reiniciado

## Scripts locais

- Client base: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/arx_client.py`
- Gerador de relatório: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/gerar_relatorio_arx.py`

Rodar:

```bash
/data/.openclaw/workspace-kowalski/arx-backup/scripts/gerar_relatorio_arx.py
```

Saídas:

- JSON sanitizado: `/data/.openclaw/workspace-kowalski/arx-backup/dados/account-statistics-sanitized.json`
- Markdown: `/data/.openclaw/workspace-kowalski/arx-backup/relatorios/relatorio-arx-backup-YYYY-MM-DD.md`

## Segurança

A API pode retornar `Password`, `Token` e `visa`. O client local redige esses campos automaticamente na saída padrão. Não salvar JSON bruto sem sanitização.
