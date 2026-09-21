---
id: brain-f819c078460db8166730
type: knowledge
title: Validacao do caminho final instalado
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T17:53:52Z'
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Deploy-atomico-de-skills-com-hash-canonico.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado.md#relações
- type: references
  target: BRAIN/01-DIARIO/Semanal/2026-W31.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado.md#relações
---

# Validacao do caminho final instalado

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W31
confiabilidade: alta
ultima_revisao: 2026-08-02
tags: [instalacao, launcher, black-box, dre, runtime, validacao]
```

## Principio

Teste em clean root, pre-install ou commit preservado nao comprova que a ferramenta instalada funciona. O caminho final usado pelo operador precisa ser validado em black-box.

## Gate minimo

1. Instalar no caminho final esperado.
2. Executar o binario ou launcher pelo mesmo comando que o usuario usara.
3. Confirmar que caminhos internos sao relocatable ou calculados a partir do local correto.
4. Validar saida, exit code, logs e ausencia de dependencia acidental do diretorio de build.
5. Reverter a instalacao se o caminho final resolver artefato incorreto.

## Exemplo conectado

Na semana 2026-W31, o OpenClaw DRE v1 tinha commit preservado, `75/75` testes pre-install e `git fsck` PASS, mas a instalacao foi revertida porque `/usr/local/bin/openclaw-dre` resolvia incorretamente `/usr/local/src/dre.py`. O estado correto ficou como nao instalado.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao|Validação do runtime pós-migração]]
- [[40-CONHECIMENTO/Operacional/Deploy-atomico-de-skills-com-hash-canonico|Deploy atômico de skills com hash canônico]]
- [[01-DIARIO/Semanal/2026-W31|Semana 2026-W31, cobertura parcial]]
