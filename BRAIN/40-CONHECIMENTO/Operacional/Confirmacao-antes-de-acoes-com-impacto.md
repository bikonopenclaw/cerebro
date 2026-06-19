# Confirmação antes de ações com impacto

```yaml
categoria: operacional
tipo: guardrail
fonte: orientação de Hebert em 2026-06-18/19
confiabilidade: alta
ultima_revisao: 2026-06-19
tags: [guardrails, confirmacao, telegram, execucao, mensagens, seguranca-operacional]
```

## Regra

Antes de iniciar ações que gerem envio, alteração, criação ou execução fora da conversa atual, avisar Hebert e obter confirmação quando o impacto não estiver previamente autorizado.

## Inclui

- Enviar ou repostar mensagens em grupos/canais.
- Acionar agentes para execução com efeito externo.
- Alterar arquivos, configurações ou recursos operacionais fora de uma rotina já autorizada.
- Criar integrações, chaves, recursos, jobs ou artefatos com impacto operacional.
- Disparar comunicação externa, emissão fiscal, boleto, remessa, webhook ou chamada real a API sensível.

## Exceções

- Pesquisas simples e levantamento de informação sem impacto externo.
- Rotinas silenciosas já autorizadas, como a consolidação diária do Brain, desde que respeitem suas próprias restrições.
- Preparos internos reversíveis em rascunho, quando não enviem, publiquem, acionem terceiros ou exponham dados sensíveis.

## Motivo

A regra reduz risco de execução fora de contexto, postagem no canal errado, alteração indesejada e exposição acidental de informação sensível.

## Relações

- `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
- `BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md`
- `BRAIN/99-SISTEMA/MEMORY.md`
