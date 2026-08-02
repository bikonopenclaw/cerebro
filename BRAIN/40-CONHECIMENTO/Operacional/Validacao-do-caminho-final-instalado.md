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

- `BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Deploy-atomico-de-skills-com-hash-canonico.md`
- `BRAIN/01-DIARIO/Semanal/2026-W31.md`
