# Consulta gerencial não é permissão operacional

```yaml
categoria: financeiro
tipo: guardrail
fonte: consolidação semanal 2026-W28
confiabilidade: alta
ultima_revisao: 2026-07-12
tags: [financeiro, permissoes, relatorios, sqlite, kowalski, darth-vader]
```

## Regra

Acesso de leitura para relatório, BI ou conferência não concede permissão para escrever, baixar, importar retorno, emitir NFS-e, gerar boleto, gerar remessa ou comunicar cliente.

## Aplicação prática

- Separar claramente consumidor gerencial de dono operacional do fluxo.
- Conceder somente leitura para relatórios quando a tarefa for análise ou conferência.
- Manter escrita, baixa, importação e efeitos fiscais/bancários com o agente ou processo responsável.
- Validar permissões técnicas, não apenas intenção operacional.

## Exemplo conectado

Kowalski recebeu acesso somente leitura à base financeira gerencial da BIKON para relatórios e conferências. Darth Vader continua responsável por escrita, importação de retorno, baixa, NFS-e, boleto e remessa.

## Relações

- `BRAIN/70-AUTOMACOES/boletos-malote/README.md`
- `BRAIN/60-AGENTES/DARTH-VADER.md`
- `BRAIN/60-AGENTES/KOWALSKI.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
