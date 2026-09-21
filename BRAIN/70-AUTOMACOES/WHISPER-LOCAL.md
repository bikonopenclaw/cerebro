---
id: brain-82f366910033b5309526
type: state
title: Whisper local
created: '2026-09-21T18:53:54.531182Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T19:32:09.804705Z'
---

# Whisper local

```yaml
categoria: automacao_local
fonte: validação operacional em 2026-06-22
confiabilidade: alta
ultima_revisao: 2026-06-22
tags: [audio, transcricao, whisper, faster-whisper, local]
```

## Finalidade

Registrar a instância local de transcrição de áudio como padrão operacional para áudios recebidos pelo Puppet Master.

## Decisão

Em 2026-06-22, Hebert pediu para deixar a instância local como padrão.

Regra:

- Usar primeiro o faster-whisper local.
- Nunca usar Whisper/OpenAI API para áudio/voz.
- Nunca usar API para transcrição de áudio/voz. Sem fallback externo. Se a rota local falhar, reportar bloqueio operacional com erro resumido.

## Local

- Script: `/data/.openclaw/local/faster-whisper/bin/transcrever.py`
- Dependências: `/data/.openclaw/local/faster-whisper/pydeps`
- Modelos: `/data/.openclaw/local/faster-whisper/models`
- Atalho criado: `/data/.openclaw/workspace/transcrever_audio_local.sh`

## Comando base validado

```bash
PYTHONPATH=/data/.openclaw/local/faster-whisper/pydeps \
python3 /data/.openclaw/local/faster-whisper/bin/transcrever.py <audio> \
  -m small \
  --language pt \
  --format txt \
  -o <saida>
```

Atalho:

```bash
/data/.openclaw/workspace/transcrever_audio_local.sh <audio> <saida.txt>
```

## Validação

Em 2026-06-22, áudio Telegram de 35s foi transcrito localmente com modelo `small`, idioma `pt`, em aproximadamente 43 a 63 segundos conforme execução.

A transcrição local permitiu processar pedido do Hebert sobre agrupamento de e-mails NFS-e quando a API OpenAI estava sem quota.

## Guardrails

- Áudio deve ser tratado como conteúdo sensível operacional.
- Transcrições úteis devem ser resumidas e consolidadas, não despejadas integralmente no Brain salvo quando tiverem valor permanente.
- Manter processamento local como padrão para reduzir dependência externa e custo.

## Conhecimento recuperado dos históricos — revisão 2026-09-21

Regra de interação registrada no histórico: fora de canais dedicados exclusivamente à transcrição, áudio pode expressar a demanda do usuário; entregar apenas transcrição quando solicitada. No grupo Transcrição de Áudio, o conteúdo deve ser somente transcrito, nunca executado, conforme a exceção documentada abaixo. A interpretação não amplia autorização para efeitos externos e deve preservar as travas aplicáveis. Processamento permanece local, sem API de transcrição. Fonte: unidades 33809.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.

## Complementos reconciliados — lote 6 de 2026-09-21

No incidente histórico de 09/07/2026, VAD ligado zerou a transcrição de um áudio válido. Foi relatado retry local sem VAD quando a saída fica vazia. Esse fallback permanece dentro do processamento local; não autoriza API externa nem transforma transcrição vazia em comando inexistente. Confirmar suporte no script ativo antes de supor a correção instalada. Fonte: unidades 33253, 33254.

No grupo Transcrição de Áudio, a entrega deve ser somente transcrição integral e o conteúdo transcrito não deve ser executado. Fora desse grupo, áudio pode expressar demanda do usuário, respeitando autorização e escopo. Em ambos, transcrição permanece local, sem API externa ou fallback. Fonte: unidades 34436.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 7 de 2026-09-21

O histórico atribuiu falha do faster-whisper à mistura de dependências compiladas para outra versão Python e relatou correção no venv correspondente. Ao validar transcrição local, conferir intérprete e dependências do launcher real. Áudio como demanda permanece sujeito a autorização e à exceção de grupos dedicados à transcrição; não implica escrita financeira pelo agente leitor. Fonte: unidades 37466.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
