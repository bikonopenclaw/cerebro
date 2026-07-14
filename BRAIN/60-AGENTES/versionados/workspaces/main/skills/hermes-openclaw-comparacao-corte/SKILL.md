---
name: "hermes-openclaw-comparacao-corte"
description: "Compara dry-runs Hermes x OpenClaw antes de corte"
---

# Hermes OpenClaw Comparacao E Corte

## Quando Usar

Use esta skill quando um bloco operacional estiver rodando em paralelo no Hermes e no OpenClaw e Hebert ou Puppet Master precisarem decidir se o Hermes pode assumir aquele bloco.

Exemplos de blocos:

- WhatsApp Bikon KPI.
- ARX Backup.
- NinjaOne relatorios/tickets.
- Bitdefender GravityZone.
- Robotnik draft editorial.
- Rotinas financeiras read-only para relatorio.

## Objetivo

Comparar saidas dos dois ambientes com criterio tecnico e operacional, evitando corte por impressao. A skill gera uma recomendacao clara:

- `manter dry-run`;
- `corrigir Hermes`;
- `corrigir OpenClaw`;
- `pronto para corte interno`;
- `nao cortar`;
- `exige aprovacao Hebert`.

A skill nao aplica corte automaticamente.

## Entradas Esperadas

Para cada bloco, coletar:

1. Nome do bloco.
2. Janela comparada em horario de Brasilia/Sao_Paulo.
3. Job/cron OpenClaw correspondente.
4. Job/cron Hermes correspondente.
5. Saida gerada em ambos os lados.
6. Status de execucao: ok, falha, timeout, sem dado, divergente.
7. Canal de entrega: local, Telegram, WhatsApp, e-mail, Instagram ou outro.
8. Se envolve cliente externo, marca publica, financeiro, producao ou pagamento.

## Procedimento

1. Confirmar que o bloco Hermes esta em dry-run/local quando ainda nao houve corte aprovado.
2. Comparar horario planejado e horario real.
3. Comparar sucesso tecnico:
   - exit code;
   - timeout;
   - erro de credencial;
   - erro de permissao;
   - job pendurado;
   - falha de provider/modelo.
4. Comparar conteudo:
   - dados essenciais presentes;
   - cliente correto;
   - periodo correto;
   - contagem ou totais compativeis;
   - formato Bikon preservado;
   - ausencia de vazamento de segredo/log bruto.
5. Classificar divergencia:
   - `nenhuma`: saidas equivalentes.
   - `baixa`: diferenca textual sem impacto operacional.
   - `media`: diferenca exige revisao antes de corte.
   - `alta`: nao cortar.
6. Verificar travas:
   - envio externo exige aprovacao explicita;
   - canal publico exige aprovacao explicita;
   - pagamento, checkout, site ou integracao critica exigem aprovacao caso a caso;
   - gasto acima de R$ 1 exige aprovacao.
7. Gerar recomendacao e rollback.

## Criterios De Corte

Um bloco so pode ser recomendado para corte interno quando:

- Hermes executou sem erro no ciclo comparado.
- OpenClaw continuou ativo como fallback durante a comparacao.
- Saida Hermes e OpenClaw sao equivalentes ou melhores.
- Nao ha divergencia alta ou media sem explicacao.
- Rollback esta descrito em uma frase executavel.
- Nao envolve envio externo sem aprovacao.

## Formato Da Saida

Responder assim:

```text
Bloco: {{nome}}
Janela: {{horario_brasilia}}
Status: {{pronto_para_corte|manter_dry_run|nao_cortar}}

Comparacao:
- OpenClaw: {{status_curto}}
- Hermes: {{status_curto}}
- Divergencia: {{nenhuma|baixa|media|alta}} - {{motivo}}

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

## Observacao De Arquitetura

Na migracao atual, o primeiro candidato de corte e `Kowalski relatorios internos, sem envio externo`. Envio externo, Robotnik publicacao, producao, checkout, pagamento e integracoes criticas ficam travados ate aprovacao explicita de Hebert.
