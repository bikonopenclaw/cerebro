# Fluxo de campanha e portões

## Estados

Usar transições explícitas:

```text
intake
brief-pending
brief-approved
brand-context-pending
brand-locked
research-pending
strategy-pending
strategy-approved
creative-approved
generation-approval-pending
generation-submitted
generated
asset-selected
composition-pending
qa-pending
brand-qa-pending
release-candidate
owner-approval-pending
external-action-approved
external-action-running
published
measured
archived
blocked
```

Não pular estados que representem aprovação ou validação de marca.

## Portão A — Briefing

Aprovar objetivo, público, oferta, formato, prazo, KPI, orçamento e restrições.

## Portão K — Marca

Kowalski fornece manual e brandpack vigentes e emite `brand-lock`. Esse parecer habilita produção, mas não autoriza ação externa.

## Portão B — Estratégia e rota

O proprietário aprova pilar, ângulo, hook, roteiro, direção visual e rota criativa.

## Portão C — Geração externa

Antes de Kling ou outro provedor explicitamente autorizado, apresentar:

- comando;
- tipo de mídia;
- modelo;
- prompt;
- referências;
- dados enviados;
- proporção e resolução;
- duração;
- quantidade;
- custo ou saldo;
- hash dos parâmetros.

Uma aprovação autoriza somente o conjunto apresentado. Nova variante exige novo OK.

## Portão D — QA e marca

Exigir:

- QA técnico;
- QA visual;
- QA textual;
- QA legal aplicável;
- `brand-qa: pass` de Kowalski.

Nenhum desses pareceres substitui o Portão X.

## Portão X — Ação externa

O proprietário aprova uma ação exata:

- `generate_external`;
- `upload_external`;
- `send_external`;
- `publish_now`;
- `schedule_and_publish`;
- `edit_remote`;
- `delete_remote`.

Aprovar “agendar” não autoriza publicação futura, salvo quando o resumo explicitar `schedule_and_publish`.

## Registro de aprovação

Registrar:

- approval ID;
- portão;
- decisão;
- aprovador humano;
- mensagem original;
- data e fuso;
- campanha, ativo e versão;
- ação e destino;
- hash do payload;
- parâmetros aprovados;
- ressalvas;
- status;
- horário de consumo.

Usar `{baseDir}/assets/approval-record.yaml` como modelo.

## Validade

Uma aprovação é inválida quando:

- foi revogada;
- já foi consumida;
- o payload mudou;
- a versão mudou;
- o destino mudou;
- a ação executada não coincide com a aprovada;
- o contexto da mensagem “OK” é ambíguo.

## Idempotência

Usar:

```text
campaign_id + asset_id + version + operation + payload_hash
```

Antes de repetir uma ação, consultar se a operação anterior já foi concluída. Em dúvida sobre resultado remoto, não repetir mutação.


## Eventos e pipeline 2.1

Cada transição gera evento encadeado. Assets seguem source, generated, selected, composed, qa, release-candidate e archived. Ação externa usa approved, reserved, executing e outcome. Não projetar published a partir de stdout; exigir resultado persistido.
