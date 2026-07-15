---
name: "hermes-openclaw-comparacao-corte"
description: "Gate de corte e producao Hermes controlada"
---

# Hermes OpenClaw Comparacao E Corte

## Quando Usar

Use esta skill quando um bloco operacional estiver rodando em paralelo no Hermes e no OpenClaw e Hebert ou Puppet Master precisarem decidir se o Hermes pode assumir aquele bloco, produzir conteudo real interno ou continuar em dry-run.

Exemplos de blocos:

- WhatsApp Bikon KPI.
- ARX Backup.
- NinjaOne relatorios/tickets.
- Bitdefender GravityZone.
- Robotnik draft editorial.
- Rotinas financeiras read-only para relatorio.
- Conteudo interno pronto para revisao: texto, arte, relatorio, roteiro, briefing, diagnostico ou arquivo.

## Objetivo

Comparar saidas dos dois ambientes com criterio tecnico e operacional, evitando corte por impressao.

A skill gera uma recomendacao clara:

- `manter dry-run`;
- `corrigir Hermes`;
- `corrigir OpenClaw`;
- `liberar producao interna Hermes`;
- `pronto para corte interno`;
- `nao cortar`;
- `exige aprovacao Hebert`;
- `rollback`.

A skill nao aplica corte automaticamente.

## Distincao Critica

Hermes pode ganhar poder para produzir conteudo real interno quando passar pelos gates.

Conteudo real interno permitido, apos aprovacao do bloco:

- rascunho de post;
- roteiro;
- legenda;
- relatorio;
- diagnostico;
- arte ou briefing para revisao;
- arquivo de trabalho;
- resumo executivo;
- material para Puppet Master revisar.

Continua bloqueado sem aprovacao explicita de Hebert:

- envio externo;
- publicacao em canal publico;
- mensagem para cliente;
- alteracao em producao;
- checkout, pagamento, boleto, NFS-e, remessa ou gravacao financeira definitiva;
- gasto acima de R$ 1;
- desligar OpenClaw como fallback.

## Estados Do Bloco

Todo bloco deve estar em um destes estados:

### `dry-run`

Hermes executa localmente ou em ambiente controlado, sem efeito externo e sem substituir OpenClaw.

### `shadow-validado`

Hermes rodou em paralelo e gerou saida equivalente ou melhor que OpenClaw, com evidencia suficiente.

### `producao-interna-hermes`

Hermes pode produzir conteudo real interno para revisao, sem envio externo e sem cortar o fallback OpenClaw.

### `candidato-a-corte`

Hermes passou nos ciclos comparados e pode ser recomendado para assumir o bloco internamente, desde que rollback esteja claro.

### `corte-aprovado`

Corte aprovado explicitamente por Hebert ou por regra operacional ja autorizada.

### `rollback`

Corte revertido ou recomendacao de reversao por falha, divergencia ou risco.

## Entradas Esperadas

Para cada bloco, coletar:

1. Nome do bloco.
2. Estado atual do bloco.
3. Janela comparada em horario de Brasilia/Sao_Paulo.
4. Job/cron OpenClaw correspondente.
5. Job/cron Hermes correspondente.
6. Saida gerada em ambos os lados.
7. Status de execucao: ok, falha, timeout, sem dado, divergente.
8. Canal de entrega: local, Telegram, WhatsApp, e-mail, Instagram ou outro.
9. Se envolve cliente externo, marca publica, financeiro, producao ou pagamento.
10. Pacote de evidencias e rollback.

## Pacote De Evidencias

Antes de recomendar qualquer avanco, reunir:

- saida OpenClaw;
- saida Hermes;
- timestamp em Brasilia;
- fonte dos dados;
- status tecnico;
- diff de conteudo;
- divergencias explicadas;
- risco principal;
- canal envolvido;
- estado recomendado;
- rollback executavel em uma frase.

Sem pacote de evidencias, no maximo manter dry-run.

## Procedimento

1. Confirmar estado atual do bloco.
2. Confirmar que Hermes esta em dry-run/local quando ainda nao houve permissao para produzir conteudo real interno.
3. Comparar horario planejado e horario real.
4. Comparar sucesso tecnico:
   - exit code;
   - timeout;
   - erro de credencial;
   - erro de permissao;
   - job pendurado;
   - falha de provider/modelo;
   - drift de provider/modelo/snapshot;
   - cache espelhado incompleto;
   - runtime diferente sem justificativa.
5. Comparar conteudo:
   - dados essenciais presentes;
   - cliente correto;
   - periodo correto;
   - contagem ou totais compativeis;
   - formato Bikon preservado;
   - ausencia de vazamento de segredo/log bruto;
   - ausencia de decisao externa nao aprovada.
6. Classificar divergencia:
   - `nenhuma`: saidas equivalentes.
   - `baixa`: diferenca textual sem impacto operacional.
   - `media`: diferenca exige revisao antes de corte ou producao interna.
   - `alta`: nao cortar e nao liberar producao real.
7. Verificar travas:
   - envio externo exige aprovacao explicita;
   - canal publico exige aprovacao explicita;
   - pagamento, checkout, site ou integracao critica exigem aprovacao caso a caso;
   - gasto acima de R$ 1 exige aprovacao;
   - OpenClaw deve continuar fallback ate corte aprovado.
8. Gerar recomendacao e rollback.

## Criterios Para Producao Interna Hermes

Hermes pode ser recomendado para `producao-interna-hermes` quando:

- executou sem erro no ciclo validado;
- nao envolve envio externo automatico;
- nao envolve financeiro definitivo, pagamento, producao ou cliente externo;
- saida foi equivalente ou melhor que OpenClaw, ou a tarefa e nova e foi validada por Puppet Master;
- risco principal esta descrito;
- revisao por Puppet Master continua obrigatoria antes de chegar ao Hebert ou sair para fora.

## Criterios De Corte

Um bloco so pode ser recomendado para `candidato-a-corte` quando:

- Hermes executou sem erro no ciclo comparado;
- OpenClaw continuou ativo como fallback durante a comparacao;
- saida Hermes e OpenClaw sao equivalentes ou melhores;
- nao ha divergencia alta ou media sem explicacao;
- crons recorrentes sensiveis passaram por mais de um ciclo ou justificativa forte;
- provider/modelo/snapshot estao coerentes;
- cache, credenciais, permissoes e runtime foram validados;
- rollback esta descrito em uma frase executavel;
- nao envolve envio externo sem aprovacao.

## Formato Da Saida

Responder assim:

```text
Bloco: {{nome}}
Estado atual: {{estado_atual}}
Janela: {{horario_brasilia}}
Status: {{manter_dry_run|liberar_producao_interna|candidato_a_corte|nao_cortar|rollback}}

Comparacao:
- OpenClaw: {{status_curto}}
- Hermes: {{status_curto}}
- Divergencia tecnica: {{nenhuma|baixa|media|alta}} - {{motivo}}
- Divergencia de conteudo: {{nenhuma|baixa|media|alta}} - {{motivo}}

Evidencia minima:
{{evidencia_curta}}

Risco:
{{risco_principal}}

Rollback:
{{acao_de_rollback}}

Recomendacao:
{{decisao_operacional}}
```

Para Hebert, resumir em 3 linhas quando ele pedir apenas status:

1. O que foi comparado.
2. Resultado e risco.
3. Proximo passo sugerido.

## Travas

- Nao desligar OpenClaw durante comparacao.
- Nao ativar envio externo no Hermes sem aprovacao.
- Nao tratar falso positivo de doctor como falha operacional se teste real passou.
- Nao mascarar divergencia de conteudo como sucesso tecnico.
- Nao recomendar corte se nao houver rollback claro.
- Nao chamar conteudo real interno de envio externo. Sao coisas diferentes.
- Nao liberar producao interna se isso puder disparar cliente, publico, financeiro ou producao sem revisao.

## Observacao De Arquitetura

Na migracao atual, o primeiro candidato de corte e `Kowalski relatorios internos, sem envio externo`.

Hermes pode evoluir como estrutura produtora de conteudo real interno, mas Puppet Master continua CEO/orquestrador no OpenClaw. Envio externo, Robotnik publicacao, producao, checkout, pagamento e integracoes criticas ficam travados ate aprovacao explicita de Hebert.
