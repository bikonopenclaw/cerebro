# Índice Swagger API WhatsApp Bikon

Fonte: `spec/swagger-v2.json`

Total de endpoints: 113

## ActionCards

- `GET` `/core/v2/api/action-cards`: Lista os cartões de ação do sistema
- `GET` `/core/v2/api/action-cards/quick-answers`: Lista as respostas rápidas da empresa vinculada ao canal
- `GET` `/core/v2/api/action-cards/quick-answers/user/{userId}`: Lista as respostas rápidas do usuário especificado
- `GET` `/core/v2/api/action-cards/quick-answers/{id}`: Busca uma resposta rápida pelo seu ID
- `POST` `/core/v2/api/action-cards/sync-templates`: Solicita sincronização dos templates de mensagem do canal de tipo WhatsAppCloud
- `GET` `/core/v2/api/action-cards/templates`: Lista os templates de mensagem do canal de tipo WhatsAppCloud
- `GET` `/core/v2/api/action-cards/templates/{id}`: Busca um template pelo seu ID (somente WhatsApp Cloud)
- `GET` `/core/v2/api/action-cards/{id}`: Busca um cartão de ação pelo seu ID

## Backups

- `GET` `/core/v2/api/backups`: Lista os backups do sistema
- `GET` `/core/v2/api/backups/{id}`: Busca um backup por seu ID

## Channels

- `GET` `/core/v2/api/channel`: Consulta os dados do canal
- `GET` `/core/v2/api/channel/list`: Busca a lista de canais do sistema
- `POST` `/core/v2/api/channel/reboot`: Faz o reboot do canal
- `GET` `/core/v2/api/channel/status`: Consulta estado atual do canal

## ChatBots

- `GET` `/core/v2/api/chatbots`: Lista dos chatbots da organização a qual o canal do token informado esta vinculado
- `GET` `/core/v2/api/chatbots/{chatbotId}/menus`: Lista os menus do chatbot
- `GET` `/core/v2/api/menus`: Lista os menus do chatbot(PADRÃO) da organização do canal ou mesmo o que esteja configurado no próprio canal

## Chats

- `POST` `/core/v2/api/chats/messages/scheduler`: Agendamento de mensagens
- `POST` `/core/v2/api/chats/messages/scheduler/list`: Lista as mensagens agendadas anteriormente de acordo com os filtros
- `DELETE` `/core/v2/api/chats/messages/scheduler/{scheduleId}`: Cancelamento de mensagem previamente agendada
- `GET` `/core/v2/api/chats/messages/scheduler/{scheduleId}`: Busca mensagem agendada pelo ID
- `GET` `/core/v2/api/chats/messages/{id}`: Busca informações da mensagem
- `POST` `/core/v2/api/chats/send-action-card`: Enviar cartão de ação
- `POST` `/core/v2/api/chats/send-contacts`: Envio de contatos
- `POST` `/core/v2/api/chats/send-copy-button`: Enviar botão com ação de copiar via número (somente waWeb)
- `POST` `/core/v2/api/chats/send-location`: Envio de localização
- `POST` `/core/v2/api/chats/send-media`: Envio de arquivo de midia
- `POST` `/core/v2/api/chats/send-presence-update`: Rota para atualizar o status do chat(somente waWeb)
- `POST` `/core/v2/api/chats/send-template`: Enviar template de mensagem (somente wacloud)
- `GET` `/core/v2/api/chats/send-text`: Envio de texto(Via Query Params)
- `POST` `/core/v2/api/chats/send-text`: Envio de texto
- `POST` `/core/v2/api/chats/{id}/send-buttons`: Enviar menu de botões
- `POST` `/core/v2/api/chats/{id}/send-copy-button`: Enviar botão com ação de copiar (somente waWeb)
- `POST` `/core/v2/api/chats/{id}/send-menu`: Enviar menu de chatBot
- `POST` `/core/v2/api/chats/{id}/send-sections`: Enviar lista de sessões
- `POST` `/core/v2/api/chats/{id}/transfer`: Realiza transferência de atendimento para setor ou usuário especificado

## ChatsActions

- `POST` `/core/v2/api/chats/after-hour/finalize`: Finaliza todos os atendimentos fora de hora que tiveram origem pelo token do canal informado
- `POST` `/core/v2/api/chats/create-new`: Cria um novo atendimento
- `POST` `/core/v2/api/chats/finalize`: Finaliza uma 1 ou mais chats baseado nos filtros informados
- `POST` `/core/v2/api/chats/{id}/finalize`: Finaliza um único chat

## ChatsUtilities

- `POST` `/core/v2/api/chats/count`: Busca a quantidade de atendimentos do canal de acordo com os filtros
- `POST` `/core/v2/api/chats/list`: Busca todos os atendimentos do canal de acordo com o estado [paginação de 100]
- `POST` `/core/v2/api/chats/list-lite`: Busca todos os atendimentos do canal de acordo com o estado de forma resumida [paginação de 500]
- `GET` `/core/v2/api/chats/{chatId}`: Busca dados de um chat
- `GET` `/core/v2/api/chats/{id}/get-attributes`: Busca a coleção dos atributos do chat
- `GET` `/core/v2/api/chats/{id}/get-attributes/{key}`: Busca um atributo do chat por seu Key
- `POST` `/core/v2/api/chats/{id}/set-attributes`: Setar atributos no chat

## Common

- `POST` `/core/v2/api/organization/clone`: Usado para criar cópias da empresa/organização da qual esse canal tem vínculo
- `POST` `/core/v2/api/wa-number-check/{number}`: Consulta o status de um número à saber é num número WA válido

## Contacts

- `GET` `/core/v2/api/contacts`: Busca a lista dos contatos baseado na organização ao qual o canal pertence
- `POST` `/core/v2/api/contacts`: Cadastra um novo contato
- `GET` `/core/v2/api/contacts/list`: Busca a lista paginada dos contatos baseado na organização ao qual o canal pertence e nos filtros fornecidos
- `GET` `/core/v2/api/contacts/number/{number}`: Busca os dados do contato pelo número
- `DELETE` `/core/v2/api/contacts/{id}`: Deleta um contato
- `GET` `/core/v2/api/contacts/{id}`: Busca os dados do contato
- `PUT` `/core/v2/api/contacts/{id}`: Edita dados do contato
- `POST` `/core/v2/api/contacts/{id}/archive`: Faz o arquivamento desse contato no whatsapp
- `PUT` `/core/v2/api/contacts/{id}/block`: Bloqueia/desbloqueia o contato no WhatsApp
- `PUT` `/core/v2/api/contacts/{id}/event-lock`: Adiconado uma trava ao contato para que que passe fora das regras do sistema e apenas execute eventos vinculados
- `GET` `/core/v2/api/contacts/{id}/get-attributes`: Busca a coleção dos atributos do contato
- `GET` `/core/v2/api/contacts/{id}/get-attributes/{key}`: Busca um atributo do contato por seu Key
- `GET` `/core/v2/api/contacts/{id}/list-tags`: Busca as tags do contato
- `POST` `/core/v2/api/contacts/{id}/set-attributes`: Setar atributos no contato
- `PUT` `/core/v2/api/contacts/{id}/set-tags`: Atribui tags a um contato de forma a atualizar tudo
- `PUT` `/core/v2/api/contacts/{id}/tags-add`: Adiciona tags a um contato(não irá afetar as demais tags do contato)
- `PUT` `/core/v2/api/contacts/{id}/tags-remove`: Remove tags de um contato(não irá afetar as demais tags do contato)

## Groups

- `GET` `/core/v2/api/groups`: Busca informações sobre o grupo(Válido apenas para canais WhatsappWeb)
- `POST` `/core/v2/api/groups`: Cria um novo grupo(Válido apenas para canais WhatsappWeb)
- `PUT` `/core/v2/api/groups`: Alterar informações do grupo(Válido apenas para canais WhatsappWeb)
- `GET` `/core/v2/api/groups/list`: Busca a lista dos grupos baseado na organização ao qual o canal pertence
- `POST` `/core/v2/api/groups/manage-users`: Gerir usuários do grupo(Válido apenas para canais WhatsappWeb)
- `POST` `/core/v2/api/groups/{groupId}/leave`: Sair do grupo(Válido apenas para canais WhatsappWeb)
- `POST` `/core/v2/api/groups/{inviteCode}/join`: Entrar num grupo por um convite(Válido apenas para canais WhatsappWeb)

## Scripts

- `GET` `/core/v2/api/scripts`: Busca a lista de scripts do sistema a qual o canal do token informado esta vinculado
- `POST` `/core/v2/api/scripts`: Adiciona um novo script
- `POST` `/core/v2/api/scripts/delaied`: Execução do script com atraso configurável
- `GET` `/core/v2/api/scripts/events`: Lista completa dos tipos de evento disponíveis para vinculo no script
- `POST` `/core/v2/api/scripts/execute`: Faz a execução de um script junto ao seu contexto
- `POST` `/core/v2/api/scripts/scheduler`: Agendamento de script para execução
- `POST` `/core/v2/api/scripts/scheduler/list`: Lista os scripts que já tenham sido agendado
- `DELETE` `/core/v2/api/scripts/scheduler/{scheduleScriptId}`: Cancelamento de script agendado seja por data, ou por delay
- `DELETE` `/core/v2/api/scripts/{id}`: Deleta um script
- `GET` `/core/v2/api/scripts/{id}`: Busca um script por seu ID
- `PUT` `/core/v2/api/scripts/{id}`: Edita um script existente
- `POST` `/core/v2/api/scripts/{id}/new-webhook`: Rota utilizada para gerar um novo endereço webhook para acionamento do script
- `POST` `/core/v2/api/scripts/{id}/set-lock`: Faz o bloqueio de um script

## Sectors

- `GET` `/core/v2/api/sectors`: Busca a lista de setores da organização a qual o canal do token informado esta vinculado
- `GET` `/core/v2/api/sectors/{id}`: Busca um setor pelo seu ID

## ServiceTimeRules

- `GET` `/core/v2/api/check-is-service-time`: Valida se é ou não hora útil com base num setor
- `GET` `/core/v2/api/service-time-rules`: Busca a lista completa das regra de horário do sistema

## System

- `POST` `/core/v2/api/block-notifications`: Realiza bloqueio de alguns tipos de notificação a nível de sistema
- `GET` `/core/v2/api/distribution-roulette`: Busca as configurações da Roleta de Distribuição do Sistema
- `PUT` `/core/v2/api/distribution-roulette`: Altera as configurações da Roleta de Distribuição do Sistema
- `GET` `/core/v2/api/distribution-roulette/active`: Busca se a Roleta de Distribuição está ativa no sistema
- `PUT` `/core/v2/api/distribution-roulette/active`: Ativar/desativar distribuição da roleta
- `GET` `/core/v2/api/general-settings`: Busca as configurações gerais a nível sistema
- `POST` `/core/v2/api/general-settings`: Configurações gerais a nível sistema
- `GET` `/core/v2/api/get-attributes`: Busca a coleção dos atributos do sistema
- `GET` `/core/v2/api/get-attributes/{key}`: Busca um atributo do sistema por seu Key
- `POST` `/core/v2/api/ignore-story-mentions`: Define se deve ignorar mensagens do tipo menção em story nos canais Facebook/Instagram, para não iniciar atendimento e não desenhar na plataforma este tipo de mensagem
- `POST` `/core/v2/api/set-attributes`: Setar atributos no sistema ao qual o canal pertence
- `GET` `/core/v2/api/system/variables`: Consulta todas as variáveis de ambiente disponíveis no sistema

## Tags

- `GET` `/core/v2/api/tags`: Lista as tags da organização a qual o canal do token informado esta vinculado
- `POST` `/core/v2/api/tags`: Adiciona uma nova tag
- `DELETE` `/core/v2/api/tags/{id}`: Deleta um tag
- `GET` `/core/v2/api/tags/{id}`: Busca os dados da tag
- `PUT` `/core/v2/api/tags/{id}`: Edita dados de um tag

## Users

- `GET` `/core/v2/api/users`: Busca a lista de usuários do sistema
- `POST` `/core/v2/api/users/login`: Rota para verificação dos dados de login
- `GET` `/core/v2/api/users/{id}`: Busca os dados do usuário por seu ID
- `GET` `/core/v2/api/users/{id}/attributes`: Busca a coleção dos atributos do usuário
- `POST` `/core/v2/api/users/{id}/attributes`: Setar atributos no usuário
- `GET` `/core/v2/api/users/{id}/attributes/{key}`: Busca um atributo do usuário por seu Key
