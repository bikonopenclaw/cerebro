# Interfaces persistentes participam do contrato de compatibilidade

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W35
confiabilidade: alta
ultima_revisao: 2026-08-30
tags: [compatibilidade, telegram, mini-app, deep-link, versionamento, regressao]
```

## Principio

Cards fixados, deep links, atalhos, bookmarks e parametros versionados continuam sendo interfaces ativas depois do deploy. Um build novo nao e compativel apenas porque o backend e os testes internos passam; ele precisa aceitar as entradas persistentes ainda autorizadas ou coordenar sua migracao explicita.

## Aplicacao pratica

- Inventariar interfaces persistentes antes de promover um build.
- Manter fixtures dos parametros e links ainda ativos na regressao obrigatoria.
- Validar compatibilidade no cliente real, alem de testes de maquina e validacao independente.
- Quando houver quebra intencional, migrar ou substituir o artefato persistente com owner, janela e rollback definidos.
- Preservar a falha anterior na linhagem de evidencia; repair build nao apaga o contrato que foi quebrado.

## Exemplo conectado

Em 2026-W35, o primeiro aceite real do Portal 213 falhou porque o card Telegram fixado enviava parametros do baseline anterior e o runtime aceitava apenas o sufixo do build atual. O repair build adicionou compatibilidade, passou validacao tecnica e independente e so foi aceito depois do teste real no iPhone.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Validacao-tecnica-nao-substitui-aceite-humano|Validacao tecnica nao substitui aceite humano]]
- [[40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao|Validacao do runtime pos-migracao]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[01-DIARIO/Semanal/2026-W35|Semana 2026-W35]]
