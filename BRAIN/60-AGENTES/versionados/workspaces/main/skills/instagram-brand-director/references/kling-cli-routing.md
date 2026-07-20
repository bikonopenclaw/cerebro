# Kling via executor tipado

Usar Kling somente para imagem e vídeo. Não usar para estratégia, copy, composição, publicação ou métricas.

## Preflight

Verificar existência e versão do binário, autenticação, `who_am_i`, conta e saldo. Dependência ausente gera `blocked`; instalação e login são janelas separadas.

## Execução

O modelo prepara JSON validado. O wrapper monta argv internamente e chama processo sem shell. Não aceitar comando pronto ou opção arbitrária.

Allowlist: `who_am_i`, `account`, `text_to_image`, `image_to_image`, `text_to_video`, `image_to_video`, `query_tasks`, `tool_list`.

Validar modelo anunciado, parâmetros permitidos, quantidade, proporção, resolução, duração, URLs HTTPS e arquivos dentro da campanha.

## Aprovação paga

Apresentar modelo, prompt, referências, parâmetros, quantidade, estimativa, saldo, teto e request_hash. Autorização é de uso único.

Depois, registrar generationId, creditsConsumed, saldo anterior/posterior, parâmetros, URLs e cobrança em falha. Consultar somente o ID original. Não reenviar, trocar prompt ou modelo sem nova autorização.