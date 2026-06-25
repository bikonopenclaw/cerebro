# Instagram Bikon, Robotnik

Integração oficial via Meta Graph API para o Robotnik preparar, validar e futuramente publicar posts no Instagram profissional da Bikon.

## Regra inicial

Modo padrão: `draft`.
Robotnik prepara copy, mídia, payload e validações. Publicação real só depois de aprovação do Hebert/Puppet Master.

## Permissões Meta necessárias

- instagram_basic
- instagram_content_publish
- pages_show_list
- pages_read_engagement
- pages_read_user_content, se necessário para descobrir conta vinculada
- business_management, se a Meta exigir pelo Business Manager

## Fluxo técnico de publicação

1. Criar container de mídia em `/{ig-user-id}/media` com `image_url` ou `video_url` e `caption`.
2. Para vídeo/Reels, aguardar processamento do container.
3. Publicar em `/{ig-user-id}/media_publish` com `creation_id`.

## Segurança

- Não guardar login/senha do Instagram.
- Usar token de longa duração da Meta.
- Segredos ficam em `secrets/instagram-bikon.env`, chmod 600.
- Nunca enviar token em resposta ou relatório.
