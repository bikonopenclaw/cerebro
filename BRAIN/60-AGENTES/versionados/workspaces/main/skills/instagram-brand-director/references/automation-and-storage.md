# Automação e armazenamento

OpenClaw conversa, decide, solicita aprovação e mantém o estado lógico. O executor aprovado realiza polling, render, cópia ou Buffer. Um único executor altera cada estado.

## Estado canônico

Usar `campaign.json` + `events.jsonl`. Índices externos são projeções, nunca fonte de verdade.

## Ativos

Baixar URLs temporárias imediatamente. Registrar SHA-256, MIME, tamanho, dimensões, duração, origem e timestamp. Preservar `generated/` e versionar `renders/`.

R2 pode ser aprovado como arquivo privado. Se indisponível, parar a etapa de arquivo e pedir nova rota. Não escolher armazenamento alternativo sozinho.

## Retry

Somente operação não paga, idempotente e transitória pode ter retry limitado pelo executor aprovado. Nunca repetir geração, voz paga, publicação, exclusão ou substituição de mídia.

## Segredos

Credenciais ficam fora da skill, prompts, manifestos, Telegram e logs.