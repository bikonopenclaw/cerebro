# Bitdefender GravityZone — status da integração

## Situação
Rotina local preparada e autenticada.

## Segredo
- Caminho: `/data/.openclaw/secrets/bitdefender-gravityzone.env`
- Permissão validada: `600`
- Variáveis esperadas: `BITDEFENDER_GZ_BASE_URL`, `BITDEFENDER_GZ_API_KEY`
- API key não deve aparecer em logs, relatórios, mensagens ou arquivos do workspace.

## Teste realizado
- Método: `getCompaniesList`
- Endpoint lógico: `network`
- Resultado: API respondeu com sucesso e retornou 21 empresas.

## Arquivos criados
- `bitdefender-gravityzone/README_OPERACIONAL.md`
- `bitdefender-gravityzone/scripts/gz_client.py`
- `bitdefender-gravityzone/relatorios/empresas-gravityzone.md`
- `bitdefender-gravityzone/status-integracao.md`

## Uso atual
```bash
python3 bitdefender-gravityzone/scripts/gz_client.py companies --format table
python3 bitdefender-gravityzone/scripts/gz_client.py companies-report > bitdefender-gravityzone/relatorios/empresas-gravityzone.md
```

## Próximas frentes quando solicitado
- Inventário de endpoints por empresa.
- Status dos agentes.
- Incidentes.
- Relatórios de segurança.

## Restrições operacionais
- Não enviar comunicação externa sem aprovação do Hebert/Puppet Master.
- Não expor credenciais.
- Não mover segredo para Drive/Telegram.
- Não delegar para Darth Vader, salvo impacto financeiro/faturamento e copiando o Puppet Master.
