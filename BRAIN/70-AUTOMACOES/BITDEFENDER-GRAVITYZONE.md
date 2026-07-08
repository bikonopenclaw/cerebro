# Bitdefender GravityZone - integração Bikon

```yaml
categoria: automacao_seguranca
fonte: conversa com Hebert em 2026-06-18/19, documentação pública Bitdefender consultada na sessão e relatório executivo gerado em 2026-06-19
confiabilidade: media
ultima_revisao: 2026-07-08
tags: [bikon, bitdefender, gravityzone, seguranca, inventario, endpoints, relatorios]
```

## Finalidade

Registrar o desenho inicial para integração da Bikon com a Public API do Bitdefender GravityZone, visando inventário, saúde de endpoints, incidentes e relatórios por cliente.

## Escopo inicial recomendado

- Inventário de empresas/clientes no GravityZone.
- Lista de endpoints por cliente.
- Status do agente Bitdefender.
- Identificação de máquinas sem proteção, offline ou com problema.
- Consulta de incidentes/detecções recentes.
- Relatório mensal por cliente.
- Alertas operacionais internos.

## APIs/permissões sugeridas

Fase inicial:

- `Network API`: clientes, grupos, endpoints e status.
- `Reports API`: geração/consulta de relatórios.
- `Incidents API`: alertas e incidentes de segurança.

Fase posterior:

- `Event Push Service API`: eventos em tempo real via webhook HTTPS.
- `Quarantine API`: consulta de quarentena, se houver necessidade operacional.

## Autenticação e segredos

- GravityZone usa API Key pelo Control Center e chamadas JSON-RPC 2.0.
- A API key deve ser exclusiva para integração, com permissão mínima necessária.
- A chave aparece uma vez só no painel; deve ser copiada e armazenada com cuidado.
- Não registrar API key no Brain, Telegram, Git ou arquivos versionados.
- Sugestão de cofre local fora do repositório: `/data/.openclaw/secrets/bitdefender-gravityzone.env`.

## Guardrails

- Não executar chamadas reais sem autorização explícita do Hebert.
- Não solicitar ou receber chave de API por Telegram.
- Não commitar arquivos `.env`, tokens, respostas sensíveis ou inventário detalhado de clientes/endpoints.
- Começar por teste controlado de autenticação e leitura, sem alteração de políticas, pacotes ou configurações.
- Ações de remediação, alteração de política, isolamento ou quarentena exigem aprovação explícita e registro operacional.

## Relatório executivo 2026-06-19

Artefatos gerados no workspace do Kowalski:

- Markdown: `/data/.openclaw/workspace-kowalski/relatorios/bitdefender/relatorio-executivo-licencas-bitdefender-2026-06-19.md`
- PDF: `/data/.openclaw/workspace-kowalski/relatorios/bitdefender/relatorio-executivo-licencas-bitdefender-2026-06-19.pdf`

Resumo agregado:

- 21 clientes.
- 785 licenças.
- 651 slots usados.
- 759 dispositivos.
- 647 dispositivos gerenciados.
- 112 dispositivos não gerenciados.

Observação: manter apenas métricas agregadas no Brain; não registrar API keys, respostas sensíveis ou inventário detalhado de clientes/endpoints.


## Relatório diário de ameaças 2026-07-02

Resumo observado na rotina diária:

- 0 ameaças detectadas.
- 0 itens em quarentena.
- 0 pendências humanas reportadas.

Observação: manter no Brain apenas agregados executivos; não versionar respostas brutas, inventário detalhado ou credenciais.

## Relatório diário de ameaças 2026-07-06

Resumo observado na rotina diária:

- 2 detecções/ameaças ativas encontradas na leitura.
- 2 endpoints afetados: `NOTE-271 | 11 - Unus` e `SCFR01 | 16 - Cartório Ferreira Rocha`.
- 0 bloqueios/quarentenas confirmados pela API para os itens retornados.
- 54 endpoints vistos em 30 dias com assinatura/produto desatualizado.

Próxima ação: revisar os endpoints com `malwareStatus` positivo diretamente no console GravityZone antes de qualquer remediação, isolamento, alteração de política ou comunicação externa.

Observação: manter apenas agregados e nomes operacionais necessários; não versionar respostas brutas, API keys ou inventário detalhado.

## Relações

- Empresa: `BRAIN/20-EMPRESAS/BIKON/README.md`
- Diretriz operacional: `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
