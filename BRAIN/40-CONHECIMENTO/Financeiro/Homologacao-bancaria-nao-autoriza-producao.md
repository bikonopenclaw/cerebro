# Homologação bancária não autoriza produção

```yaml
categoria: financeiro
tipo: guardrail
fonte: consolidação semanal 2026-W28
confiabilidade: alta
ultima_revisao: 2026-07-12
tags: [cresol, homologacao, boletos, remessa, baixa, producao]
```

## Regra

Homologação técnica, pacote local validado, API funcional ou boleto renderizado corretamente não autorizam uso em produção, upload bancário, baixa financeira ou envio externo.

## Aplicação prática

- Manter produção bloqueada por padrão até autorização explícita.
- Separar criação/consulta de título de teste de operações produtivas.
- Exigir procedimento próprio para baixa por API, com validação, rollback e aprovação.
- Registrar no Brain apenas estado, guardrails e evidência sanitizada; payloads, respostas e PDFs oficiais de homologação ficam fora do Git.
- Antes de upload, validar localmente remessa, totais, sequenciais, contrato, carteira, nosso número e documentação oficial.

## Exemplo conectado

Na semana 2026-W28, a API Cresol avançou em homologação, a remessa CNAB400 local foi validada e o boleto PDF foi conferido, mas nenhum upload no portal, envio bancário, baixa por API ou comunicação externa foi autorizado.

## Relações

- `BRAIN/70-AUTOMACOES/boletos-malote/README.md`
- `BRAIN/40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
