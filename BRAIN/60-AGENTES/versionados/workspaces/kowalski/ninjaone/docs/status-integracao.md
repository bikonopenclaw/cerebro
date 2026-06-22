# Status integração NinjaOne

Data: 2026-06-15
Tenant: https://bikon.rmmservice.com/
Docs: https://bikon.rmmservice.com/apidocs/?links.active=core

## Status
Integração autenticada com sucesso via OAuth2 Client Credentials.

## Configuração local
- Arquivo de credenciais: `config/.env`
- Permissão aplicada: `600`
- Token URL: `https://bikon.rmmservice.com/ws/oauth/token`
- API Base: `https://bikon.rmmservice.com/v2`
- Scopes atuais: `monitoring management`

## Scripts prontos
- `scripts/test_ninjaone_auth.py`: valida autenticação e `/organizations`.
- `scripts/ninjaone_client.py`: helper de leitura para endpoints permitidos.

## Endpoints validados
- `/v2/organizations`: OK, 30 organizações.
- `/v2/devices`: OK, 339 devices.
- `/v2/alerts`: OK, 122 alertas ativos/listados no momento do teste.

## Endpoints úteis para relatórios
- `/v2/organizations`
- `/v2/organizations-detailed`
- `/v2/devices`
- `/v2/devices-detailed`
- `/v2/alerts`
- `/v2/activities`
- `/v2/policies`

## Próximo passo
Criar gerador de relatório por organização/cliente no padrão Bikon, começando por:
1. Inventário de dispositivos por cliente.
2. Saúde/alertas por cliente.
3. Dispositivos offline ou com alerta crítico.
4. Patches/atividades se os campos disponíveis forem suficientes.

## Segurança
Não imprimir token nem secret em logs. Se houver suspeita de vazamento, rotacionar o secret no NinjaOne e atualizar `config/.env`.
