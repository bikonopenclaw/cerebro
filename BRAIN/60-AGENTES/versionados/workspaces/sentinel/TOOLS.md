# TOOLS

## Ferramentas permitidas

- Leitura de arquivos e evidencias do proprio workspace.
- memory_search e memory_get para contexto autorizado.
- sessions_send para coordenacao interna.
- Consultas read-only em fontes operacionais explicitamente autorizadas.
- exec somente para diagnostico local sem alterar estado.

## Fontes operacionais

NinjaOne, ARX, Bitdefender, Cove e outras integracoes so podem ser usadas quando
o acesso estiver configurado para o Sentinel ou quando outro agente autorizado
fornecer a evidencia. Nao copiar credenciais de outro workspace.

### NinjaOne read-only

- Acesso aprovado por Hebert em 2026-07-15 usando a credencial M2M compartilhada.
- Cliente permitido: `integrations/ninjaone/ninjaone_readonly.py`.
- O cliente solicita sempre token temporario com escopo exato `monitoring`.
- Metodos permitidos: somente `GET` na allowlist interna do cliente.
- Validacao: `python3 integrations/ninjaone/ninjaone_readonly.py probe`.
- Proibido usar diretamente o `.env`, alterar escopo, montar URL livre ou chamar
  endpoint de escrita, ticketing, management ou control.
- Esta e uma trava operacional. A credencial-base compartilhada continua capaz
  de solicitar `management`; segregacao real exige uma aplicacao M2M exclusiva.

### ARX Backup/Cove read-only

- Acesso aprovado por Hebert em 2026-07-15 usando a credencial de integracao `OpenClaw` ja existente.
- Cliente permitido: `integrations/arx/arx_readonly.py`.
- Comandos permitidos: `probe` e `status`.
- Metodos JSON-RPC permitidos: somente `Login` e `EnumerateAccountStatistics`.
- O Cove usa HTTP `POST` tambem para leitura; o bloqueio ocorre pela allowlist de metodos JSON-RPC.
- Validacao: `python3 integrations/arx/arx_readonly.py probe`.
- Proibido usar diretamente o `.env`, chamar outro metodo JSON-RPC, gerar relatorio,
  criar/fechar ticket, enviar e-mail ou salvar resposta bruta.
- A credencial-base e compartilhada. A protecao implantada e operacional, nao uma
  segregacao de permissao oferecida pelo provedor.

### Bitdefender GravityZone read-only

- Acesso aprovado por Hebert em 2026-07-16 pela rota oficial ja configurada.
- Cliente permitido: `integrations/bitdefender/bitdefender_readonly.py`.
- Comandos permitidos: `probe`, `companies`, `endpoints`, `quarantine` e `incidents`.
- Metodos permitidos: `network.getCompaniesList`, `network.getEndpointsList`,
  `quarantine/computers.getQuarantineItemsList` e, no endpoint oficial v1.2,
  `incidents.getIncidentsList`.
- Parametros sao fixos e limitados; a saida contem somente contagens agregadas,
  versao, operacao e metodo. Nomes, IDs e dados brutos ficam bloqueados.
- A credencial permanece externa ao workspace e deve usar permissao `600`.
- Nenhum metodo de politica, quarentena ativa, isolamento, remediacao ou escrita
  e permitido. Nao ha fallback nem troca de endpoint.
- Validacao: `python3 integrations/bitdefender/bitdefender_readonly.py probe`.

### Contexto operacional sanitizado

- Acesso aprovado por Hebert em 2026-07-16 como etapa 4 da preparacao do Sentinel.
- Cliente permitido: `context/operational_context.py`.
- Fonte cadastral exata: cadastro mestre de clientes ativos mantido por Darth Vader.
- Comandos permitidos: `summary`, `clients`, `client <client_id>` e `severity`.
- Saida permitida: ID interno, razao social, estado ativo e contexto de cartorio.
- CPF/CNPJ, inscricoes, endereco, telefone e e-mails financeiros nunca sao expostos.
- SLA, janela de manutencao e responsavel operacional permanecem `not_configured`
  enquanto nao existir fonte autoritativa aprovada. E proibido inferir esses campos.
- Ativos e saude devem ser consultados ao vivo pelos clientes read-only do NinjaOne
  ARX/Cove e Bitdefender.
- Validacao: `python3 context/operational_context.py summary`.

### Logs operacionais read-only

- Acesso aprovado por Hebert em 2026-07-16 como etapa 5 da preparacao do Sentinel.
- Cliente permitido: `integrations/logs/operational_logs.py`.
- Comandos permitidos: `sources`, `health` e `tail arx|bitdefender --lines N`.
- Gateway: somente contagens por nivel e categoria segura do arquivo do dia UTC.
  Texto, horario, subsistema, metadados, tail bruto, mensagens, sessoes e eventos
  de canal ficam bloqueados.
- Jobs: somente os logs exatos de ARX -> NinjaOne e Bitdefender -> NinjaOne.
- Toda saida passa por redacao de token, chave, senha, Authorization, JWT, parametro
  sensivel de URL e e-mail. O limite e 200 linhas e 20 MiB por fonte.
- Excluidos: SQLite, WhatsApp, Hermes bruto, sessoes, mensagens, segredos,
  `journalctl`, logs de sistema e qualquer caminho arbitrario.
- Validacao: `python3 integrations/logs/operational_logs.py health`.
- O acesso e estritamente local e read-only. Nao rotaciona, apaga, cria ou corrige log.

### Controle e auditoria de acesso

- Etapa 6 autorizada por Hebert em 2026-07-16.
- Inventario: `access_control/source_inventory.json`.
- Revogacao: `access_control/REVOGACAO.md`; qualquer execucao exige aprovacao do Hebert.
- Auditoria: `logs/access-audit.jsonl`, append-only operacional, permissao `600`.
- Campos permitidos na auditoria: ator fixo `Sentinel`, fonte, operacao, horario UTC,
  resultado, correlacao aleatoria e SHA-256 do cliente. Dados retornados e segredos
  nunca entram no registro.
- NinjaOne, ARX/Cove, contexto e logs registram sucesso e falha. Falha na auditoria
  bloqueia a operacao.
- Clientes credenciados recusam segredo ausente, symlink, proprietario inesperado
  ou permissao diferente de `600` antes de ler a credencial.
- Bitdefender registra somente os cinco comandos da allowlist, sem resposta bruta.
- A segregacao das credenciais NinjaOne, ARX/Cove e Bitdefender continua
  operacional, nao real.

## Coordenacao

- Puppet Master: `agent:main:main`
- Kowalski: `agent:kowalski:main`
- Darth Vader: `agent:darth-vader:main`
- Robotnik: `agent:robotnik:main`
- Sentinel: `agent:sentinel:main`

Usar `sessions_send(sessionKey="SESSAO_CANONICA", message=brief)`. O brief deve conter contexto, tarefa, restricoes, criterio de pronto e aprovacao do Hebert quando existente. Fila ou sessao ocupada nao autoriza reenvio. Em falha real, parar e avisar `agent:main:main`.

## Proibicoes

- Sem root ou sudo.
- Sem envio externo.
- Sem comando remoto ou script em cliente sem aprovacao.
- Sem fallback de fonte ou ferramenta quando a rota aprovada falhar.
- Sem segredo em terminal, log, relatorio ou mensagem.
