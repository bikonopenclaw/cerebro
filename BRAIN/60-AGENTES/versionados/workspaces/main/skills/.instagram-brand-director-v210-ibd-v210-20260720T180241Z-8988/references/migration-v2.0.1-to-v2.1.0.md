# Plano de migração 2.0.1 para 2.1.0

Nenhuma etapa deste plano está autorizada pela preparação da candidata.

## Fase 0, evidência

1. registrar árvore, hash, permissões e testes da v2.0.1;
2. preservar backup integral;
3. inventariar campanhas, approvals e automações existentes;
4. confirmar ausência de execução em andamento.

## Fase 1, staging

1. materializar candidata em diretório irmão;
2. validar frontmatter, schemas, sintaxe e denylist;
3. executar todos os testes;
4. executar preflight build;
5. confirmar providers externos e agentes opcionais desabilitados;
6. testar replay sobre cópia de eventos, nunca sobre produção.

## Fase 2, compatibilidade

1. rodar comandos legados em fixture;
2. migrar cópia de approval antigo sem alterar o original;
3. verificar que consume legado segue single-use;
4. validar Puppet Master, Robotnik e Kowalski;
5. comprovar que publicação e geração ficam bloqueadas.

## Fase 3, corte

Somente com novo OK:

1. backup;
2. rename atômico no mesmo filesystem;
3. sem overlay;
4. validação pós-corte;
5. segundo restart apenas se o runtime exigir descoberta;
6. nenhuma configuração de provider.

## Fase 4, dados

Em janela separada, gerar eventos de baseline para campanhas existentes e manter arquivos originais como evidência. Não reescrever histórico.

## Rollback

No primeiro desvio, renomear a candidata para quarentena, restaurar a v2.0.1 e validar hash e testes. Approvals reservados ou executando na v2.1 não podem ser reutilizados na v2.0.1.
