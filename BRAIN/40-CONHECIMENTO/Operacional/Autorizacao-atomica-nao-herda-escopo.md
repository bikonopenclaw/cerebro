# Autorizacao atomica nao herda escopo

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W31; consolidacao semanal 2026-W37; projeto LinkedIn Robotnik 2026-09-17
confiabilidade: alta
ultima_revisao: 2026-09-18
tags: [approval, checkpoints, escopo, governanca, fail-closed, provimento-213, linkedin, oauth, versao, artefato, publicacao]
```

## Principio

Autorizacao operacional deve ser atomica. Um approval, checkpoint, commit, hash, validacao independente ou publicacao comprova somente o escopo exato que foi autorizado e executado.

Nenhuma evidencia tecnica herda permissao para a proxima etapa.

## Aplicacao pratica

- Separar documento, implementacao, commit, push/publicacao, homologacao, deploy, recorrencia e rollback.
- Usar cada `approval_id` e `execution_id` apenas para a unidade autorizada.
- Tratar ordem terminal como encerrada; falha, timeout ou sucesso parcial nao autorizam reuso.
- Antes de continuar, declarar o novo impacto, os limites e o rollback da proxima unidade.
- Quando faltar evidencia completa, manter bloqueado em vez de reconstruir estado por resumo, memoria ou hash isolado.
- Vincular parecer, aceite e autoridade a identidade logica, versao e bytes exatos do artefato; alteracao posterior abre um novo gate e nao herda o veredito anterior.
- Separar criacao, revisao, entrega, aceite humano, publicacao e readback. Sucesso em uma etapa nao autoriza a seguinte nem retry de um efeito externo ja comprovado.
- Em integrações externas, separar credenciamento do app, associação/verificação da organização, concessão de produto/scope, OAuth, acesso ao segredo, aprovação do payload e publicação. Uma autorização não atravessa essas fronteiras.

## Exemplo conectado

Na semana 2026-W31, o OpenClaw - Provimento 213 teve EPs documentais, commits, hashes, validacoes independentes e publicacao canonica. Esses marcos nao autorizaram provider, target, preflight, restore, contato externo, envio de PDF, deploy ou recorrencia.

Na semana 2026-W37, o marketing Bikon preservou autoridade por versao: o aceite do piloto inicial nao autorizou publicacao; o parecer da V3 do 365 Control nao alcançou a V6; e a publicacao comprovada de 10/09 bloqueou novo `media_publish` mesmo enquanto readback e recibo permaneciam pendentes.

No LinkedIn Robotnik, Hebert autorizou somente o Gate A de credenciamento. A falta de navegador anexável bloqueou a execução antes do portal; o approval não foi interpretado como permissão para OAuth, secret store, scope adicional ou publicação.

## Relacoes

- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
- `BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md`
- `BRAIN/01-DIARIO/Semanal/2026-W31.md`
- [[01-DIARIO/Semanal/2026-W37|Semana 2026-W37]]
- [[50-PROJETOS/Em-Andamento/LinkedIn-Robotnik-Publisher|LinkedIn Robotnik Publisher]]
