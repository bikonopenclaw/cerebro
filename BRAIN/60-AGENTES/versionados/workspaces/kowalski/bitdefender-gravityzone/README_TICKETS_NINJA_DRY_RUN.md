# Bitdefender -> Ninja tickets, Fase 1 dry-run

## Objetivo
Validar a automacao Bitdefender GravityZone -> tickets Ninja sem criar ticket real, sem cron de producao e sem auto-fechamento.

## Script
`bitdefender-gravityzone/scripts/monitorar_bitdefender_ninja_tickets.py`

## Regra de abertura simulada
O dry-run simula ticket quando encontra:

- ameaca ativa;
- malware nao resolvido;
- endpoint sem protecao visto ha menos de 30 dias;
- politica critica violada;
- bloqueio/falso positivo que exige acao, quando houver fonte dedicada em fase futura.

Nao abre para ruido informativo nem historico ja resolvido.

### Regra de 30 dias para endpoint sem protecao

- `endpoint_sem_protecao` so entra no volume acionavel quando ha `lastSeen` confiavel e a ultima visualizacao foi ha 30 dias ou menos.
- Se o `lastSeen` for maior que 30 dias, o item vira `maquina_inativa` e fica fora dos tickets simulados.
- Se nao houver data confiavel, o item vira `validacao_manual` e tambem fica fora do volume acionavel principal.
- Sem data confiavel, nao liberar para ticket real.

## Padrao do ticket simulado
- Sistema: Ninja.
- Fila: padrao / triagem interna Bikon.
- Prioridade: padrao.
- Cliente afetado no assunto e no corpo.
- Sem API key, segredo, credencial, cookie ou cabecalho de autenticacao.

Assunto:

```text
Bitdefender - [tipo] - [cliente afetado] - [endpoint/resumo curto]
```

## Deduplicacao
Chave:

```text
cliente + endpoint + tipo de alerta + identificador da ameaca
```

Na Fase 1 o estado e lido de `bitdefender-gravityzone/jobs/bitdefender-ninja-ticket-state.json` se existir, mas o dry-run nao grava estado por padrao.

## Como rodar
Validacao completa:

```bash
python3 bitdefender-gravityzone/scripts/monitorar_bitdefender_ninja_tickets.py
```

Amostra rapida:

```bash
python3 bitdefender-gravityzone/scripts/monitorar_bitdefender_ninja_tickets.py --max-companies 2
```

## Saidas
O script grava:

- JSON em `bitdefender-gravityzone/relatorios/dry-run/`;
- Markdown em `bitdefender-gravityzone/relatorios/dry-run/`.

O resumo inclui:

- tickets simulados;
- endpoint sem protecao dentro de 30 dias;
- maquinas inativas excluidas;
- validacao manual sem data;
- garantia de zero ticket real e zero cron.

## Travas
- Nao chama API do Ninja.
- Nao cria ticket real.
- Nao fecha ticket real.
- Nao cria cron.
- Nao executa remediacao no endpoint.
- Nao imprime segredo.
