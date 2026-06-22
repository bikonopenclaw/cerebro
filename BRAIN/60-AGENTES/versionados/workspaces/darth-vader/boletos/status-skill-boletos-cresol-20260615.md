# Status skill boletos Cresol

## Atualizado em 2026-06-15

A skill formal do Darth Vader foi criada em:

`/data/.openclaw/agents/darth-vader/agent/skills/boletos-cresol/SKILL.md`

## Documentos adicionados

- Boleto exemplo: `exemplos/Boleto_exemplo_6_1.pdf`
- Especificações técnicas: `manual-cresol/Especificacoes_tecnicas_5_1.pdf`
- Remessa CNAB400: `manual-cresol/Padrao_Remessa_CNAB400_Cresol_133_5_1.pdf`
- Remessa/Retorno CNAB240: `manual-cresol/Padrao_Remessa_e_Retorno_CNAB240_Cresol_133_5_1.pdf`
- Retorno CNAB400: `manual-cresol/Padrao_Retorno_CNAB400_Cresol_133_5_1_1.pdf`

Todos tiveram texto extraído em `.txt` no mesmo diretório.

## Implementado agora

- Catálogo de documentos em `references/catalogo-documentos-cresol.md`.
- Mapa inicial de remessa CNAB400 em `manual-cresol/mapa-remessa-cnab400-cresol-133-v5_1.json`.
- Validador básico CNAB400 em `scripts/validar_cnab400.py`.
- Teste validado contra exemplo bom e exemplo inválido/template negativo.

## Trava de segurança

Ainda não gerar remessa real para produção. Próximo passo é fechar mapa fino das posições 150-400 diretamente contra o PDF de remessa novo e implementar gerador em modo rascunho/homologação.
