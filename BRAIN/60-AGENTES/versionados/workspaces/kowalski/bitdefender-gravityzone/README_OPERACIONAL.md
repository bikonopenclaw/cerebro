# Bitdefender GravityZone — rotina Kowalski

## Dono da rotina
Kowalski, agente de dados da Bikon Tecnologia.

## Segredo local
A credencial fica fora do workspace:

`/data/.openclaw/secrets/bitdefender-gravityzone.env`

Permissão esperada: `600`.

Variáveis esperadas:

- `BITDEFENDER_GZ_BASE_URL`
- `BITDEFENDER_GZ_API_KEY`

Regra fixa: não copiar esse arquivo para Drive, Telegram, relatório, print, log ou pasta do workspace.

## Escopo autorizado quando solicitado
- Inventário de empresas/clientes
- Inventário de endpoints
- Status dos agentes
- Incidentes
- Relatórios de segurança

## Restrições
- Não enviar comunicação externa sem aprovação do Hebert/Puppet Master.
- Não expor API key em logs, relatórios ou mensagens.
- Não delegar para Darth Vader, salvo impacto financeiro/faturamento e copiando o Puppet Master.
- Relatórios para cliente precisam sair no padrão Bikon, curtos e claros.

## Como usar

Listar empresas em formato seguro:

```bash
python3 bitdefender-gravityzone/scripts/gz_client.py companies --format table
```

Salvar JSON bruto local para análise interna:

```bash
python3 bitdefender-gravityzone/scripts/gz_client.py companies --format json > bitdefender-gravityzone/dados/companies.json
```

Gerar relatório Markdown simples:

```bash
python3 bitdefender-gravityzone/scripts/gz_client.py companies-report > bitdefender-gravityzone/relatorios/empresas-gravityzone.md
```

## Observação técnica
A API GravityZone usa JSON-RPC 2.0 com autenticação Basic. A chave é carregada só em memória a partir do arquivo local de segredo.
