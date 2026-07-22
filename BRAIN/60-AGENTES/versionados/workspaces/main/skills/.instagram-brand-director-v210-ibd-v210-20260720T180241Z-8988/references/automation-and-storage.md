# Automação, armazenamento e segredos

## Divisão de responsabilidade

Usar Puppet Master e OpenClaw para:

- conversar com o proprietário;
- delegar;
- aplicar regras;
- solicitar e registrar aprovações;
- manter o estado lógico;
- explicar falhas.

Usar Robotnik para:

- conteúdo;
- geração;
- composição;
- release candidate;
- execução autorizada de Instagram.

Usar Kowalski para:

- handoff de marca;
- brand lock;
- brand QA.

Usar n8n auto-hospedado, quando disponível, somente para:

- webhooks internos;
- polling;
- espera;
- transformação de dados;
- render local;
- cópia local;
- notificações já autorizadas;
- execução de ação externa com approval ID válido.

Não delegar ao n8n estratégia, prompt, escolha de modelo, aprovação ou decisão de publicação.

## Estado

Usar o manifesto como registro portátil. Usar SQLite ou Data Tables locais para índices operacionais.

Registrar:

- campaign ID;
- asset ID;
- versão;
- estado;
- operação;
- payload hash;
- approval ID;
- idempotency key;
- timestamps;
- resultado;
- erro sanitizado.

Não registrar tokens.

## Idempotência

Gerar:

```text
<campaign-id>:<asset-id>:<version>:<operation>:<payload-hash>
```

Antes de executar:

1. consultar a operação;
2. retornar resultado existente se concluída;
3. não duplicar geração ou publicação;
4. retomar polling pelo ID original;
5. criar nova versão somente após decisão explícita.

## Retries

Permitir retry automático somente para operações locais, idempotentes e transitórias.

Não repetir automaticamente:

- geração externa;
- upload externo;
- envio de mensagem;
- publicação;
- edição;
- exclusão;
- alteração de data;
- substituição de mídia.

## Armazenamento

Usar como padrão:

1. filesystem local controlado;
2. MinIO auto-hospedado, quando necessário.

Estrutura:

```text
campaigns/<campaign-id>/<asset-id>/<version>/<stage>/<filename>
```

Aplicar:

- acesso mínimo;
- checksums;
- versionamento lógico;
- tipo MIME correto;
- backup;
- lifecycle;
- criptografia quando disponível.

Upload para armazenamento externo exige Portão X.

## Segredos

Guardar credenciais em secret store ou variáveis de ambiente do serviço responsável.

- Token do Instagram somente para Robotnik ou executor restrito.
- Credenciais Kling somente para o executor de geração.
- Kowalski não recebe tokens de geração ou publicação.
- Puppet Master referencia secret IDs, não valores.

Não incluir valores em:

- SKILL.md;
- referências;
- manifestos;
- mensagens;
- logs;
- prompts;
- exportações n8n sem sanitização.

## Bloqueio técnico

O lock inicia em `true`. Puppet Master pode liberá-lo atomicamente somente para um approval ID, operação e payload específicos. Toda automação de mutação deve verificar:

```text
external_action_lock == false
unlocked_operation == requested_action
unlocked_payload_hash == current_payload_hash
active_approval_id == approval.approval_id
approval.status == approved
approval.payload_hash == current_payload_hash
approval.consumed_at == null
approval.action == requested_action
```

Se qualquer condição falhar, encerrar sem efeito externo. Depois de sucesso, erro, cancelamento ou timeout, reativar o lock. Não manter desbloqueio global ou permanente.

## Degradação

- Sem n8n: executar etapas internas manualmente e registrar o modo.
- Sem MinIO: manter filesystem local e backup controlado.
- Sem executor externo: gerar release candidate e handoff.
- Ausência de infraestrutura opcional nunca remove o Portão X.
