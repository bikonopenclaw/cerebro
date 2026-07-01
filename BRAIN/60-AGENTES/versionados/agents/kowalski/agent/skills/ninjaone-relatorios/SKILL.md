---
name: ninjaone-relatorios
description: Use para gerar relatórios técnicos e executivos da Bikon a partir da API NinjaOne RMM, incluindo inventário por organização/cliente, dispositivos offline, alertas ativos, saúde operacional, recomendações e rascunhos no padrão visual Bikon.
---

# NinjaOne Relatórios Bikon

Use esta skill quando o pedido envolver **NinjaOne**, **RMM**, inventário de dispositivos, alertas, saúde de endpoints, relatórios técnicos para clientes Bikon, ou consolidação operacional do parque monitorado.

## Fontes e caminhos

- Workspace da integração: `/data/.openclaw/workspace-kowalski/ninjaone`
- Helper API: `/data/.openclaw/workspace-kowalski/ninjaone/scripts/ninjaone_client.py`
- Status da integração: `/data/.openclaw/workspace-kowalski/ninjaone/docs/status-integracao.md`
- Relatórios gerados: `/data/.openclaw/workspace-kowalski/relatorios/ninjaone`
- Identidade visual: `/data/.openclaw/workspace-kowalski/identidade-visual`
- Timbrado aprovado: `/data/.openclaw/workspace-kowalski/identidade-visual/modelos-aprovados/Bikon_Timbrado.docx`

## Segurança

Nunca imprima, copie ou inclua token/secret em relatório, log ou resposta.

Não edite `config/.env` sem autorização explícita do Puppet Master/Hebert.

A skill é de leitura e relatório. Não execute ações de controle, script, alteração ou correção no NinjaOne sem autorização explícita.

## Workflow padrão

1. Buscar dados pelo helper, começando por:
   - `organizations`
   - `devices`
   - `alerts`
   - se precisar de detalhe: `organizations-detailed` e `devices-detailed`
2. Cruzar alertas por `deviceId` com devices para descobrir a organização.
3. Gerar rascunho em Markdown em `/data/.openclaw/workspace-kowalski/relatorios/ninjaone/`.
4. Usar linguagem Bikon: direta, executiva, sem enrolação.
5. Separar relatório em:
   - visão geral executiva
   - indicadores
   - riscos por cliente
   - dispositivos que precisam atenção
   - recomendações práticas
6. Só transformar em modelo padrão depois de aprovação.

## Comandos úteis

Buscar dados brutos:

```bash
/data/.openclaw/workspace-kowalski/ninjaone/scripts/ninjaone_client.py organizations
/data/.openclaw/workspace-kowalski/ninjaone/scripts/ninjaone_client.py devices
/data/.openclaw/workspace-kowalski/ninjaone/scripts/ninjaone_client.py alerts
```

Gerar relatório Markdown:

```bash
/data/.openclaw/workspace-kowalski/ninjaone/scripts/gerar_relatorio_ninjaone.py
```

Gerar relatório para cliente específico:

```bash
/data/.openclaw/workspace-kowalski/ninjaone/scripts/gerar_relatorio_ninjaone.py --cliente-id 6
```

## Indicadores mínimos

Todo relatório geral deve trazer:

- total de organizações
- total de dispositivos
- total de dispositivos offline
- total de alertas ativos/listados
- ranking de organizações por alertas
- ranking de dispositivos por alertas
- tipos de alertas mais frequentes
- recomendações objetivas

Para cliente individual, trazer:

- inventário resumido
- dispositivos offline
- alertas ativos
- riscos que podem virar chamado ou indisponibilidade
- ação recomendada para a Bikon
- mensagem executiva em português BR para o cliente, se solicitado

## Campos já observados

`devices` costuma trazer:

- `id`
- `systemName`
- `dnsName`
- `organizationId`
- `offline`
- `lastContact`
- `lastUpdate`
- `nodeClass`
- `nodeRoleId`
- `rolePolicyId`
- `approvalStatus`

`alerts` costuma trazer:

- `deviceId`
- `conditionName`
- `sourceType`
- `sourceName`
- `subject`
- `message`
- `severity`
- `priority`
- `createTime`
- `updateTime`

## Padrão Bikon

Relatório para cliente não deve parecer exportação crua do RMM.

Priorize:

- resumo executivo
- semáforo de risco
- poucos indicadores bons
- tabela objetiva
- recomendação clara

Evite despejar JSON, logs ou campos técnicos sem explicar impacto.

Nunca usar travessão em copy pública.

### Autoria e solicitante

Regra obrigatória em relatórios operacionais Bikon:

- Não mencionar nome de agente/bot como autor, solicitante ou responsável.
- Quando o pedido vier do Hebert, usar somente `Hebert Mattedi`.
- Quando o pedido vier do Felipe, usar `Hebert Mattedi e Felipe Nogueira`.

### EOL, hardware, software e cotação

Quando o relatório envolver EOL de hardware e software:

- Condensar por máquina/endpoint.
- Não duplicar a mesma máquina quando ela tiver EOL de software e de hardware.
- Software EOL vira plano interno Bikon de reinstalação, atualização ou correção.
- Hardware EOL entra como substituição física e item para cotação.
- Se a mesma máquina tiver os dois, ela entra uma vez na cotação por causa do hardware, com software como observação.
- Sempre separar `Itens para cotação de compra` de `Ações internas de software`.

## Referência detalhada

Se precisar de mais contexto, leia `references/modelo-relatorio.md`.
