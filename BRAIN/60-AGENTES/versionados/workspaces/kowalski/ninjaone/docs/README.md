# NinjaOne API para relatórios Bikon

Objetivo: permitir ao Kowalski consultar dados do NinjaOne e gerar relatórios técnicos para clientes.

## Credenciais necessárias
- Client ID
- Client Secret
- Token URL
- API Base URL
- Scopes liberados, preferencialmente leitura/relatórios/monitoramento

## Segurança
- Usar app machine-to-machine/OAuth2 client credentials.
- Começar com permissões mínimas de leitura.
- Não usar credencial de usuário humano.
- Segredos devem ficar fora do git e fora de documentos de relatório.

## Primeiros relatórios previstos
1. Inventário de dispositivos por cliente/organização
2. Status de saúde dos endpoints
3. Alertas abertos/recorrentes
4. Patch/updates pendentes
5. Backup/serviços críticos, se esses dados existirem no NinjaOne
