# Corte atômico e rollback 2.1

## Pré-corte

1. Confirmar o segundo OK do proprietário.
2. Calcular inventário e SHA-256 da v1 ativa.
3. Salvar cópia íntegra da pasta ativa em diretório de rollback com timestamp UTC.
4. Registrar o caminho de rollback e o correlation ID.
5. Validar a candidata com quick_validate, validate_skill, preflight build e testes.
6. Não reiniciar gateway, instalar dependência ou chamar serviço externo nesta etapa.

## Corte

1. Preparar a candidata em diretório irmão no mesmo filesystem.
2. Validar novamente o diretório preparado.
3. Renomear a pasta ativa para backup de corte.
4. Renomear a candidata para o nome ativo.
5. Não fazer overlay. A árvore ativa deve corresponder exatamente à candidata.
6. Registrar o evento de mudança e os hashes.

## Pós-corte

1. Validar estrutura e testes sem chamada externa.
2. Confirmar que a v1 segue íntegra no backup.
3. Abrir sessão nova somente se a descoberta da skill exigir.
4. Não ativar publicação ou geração.
5. Aguardar aprovação separada para configurar identidade, templates e adapters.

## Rollback

Se qualquer validação falhar, renomear a candidata com falha para quarentena e restaurar a pasta anterior pelo rename no mesmo filesystem. Validar a v1 restaurada com os testes e preflight build. Não reaproveitar approvals criados por outra versão. Streams v2.1 e approvals reserved, executing ou indeterminate exigem análise antes de rollback.
