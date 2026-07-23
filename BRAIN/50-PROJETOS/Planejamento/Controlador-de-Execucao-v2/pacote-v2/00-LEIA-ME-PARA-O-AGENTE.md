# Instruções para Atualização pelo Agente

## Objetivo

Incorporar a documentação v2 sem apagar ou reescrever a evidência histórica da v1.

## Ações

1. Salvar os arquivos deste pacote em `docs/workflows/controller/` ou diretório equivalente.
2. Preservar os cinco artefatos originais como histórico.
3. Marcar `PLANO-ROTEADOR-EXECUCAO-V1.md` como superseded pela v2, sem modificar seu conteúdo factual.
4. Revisar a baseline v2 linha a linha contra a coluna `evidencia`.
5. Não ativar roteamento automático.
6. Criar o Registry operacional somente após confirmar quais modelos e snapshots estão realmente disponíveis no ambiente.
7. Executar a Etapa 0.5 em modo read-only e produzir diff documental.
8. Submeter qualquer divergência de C/R/G para aprovação antes de alterar os casos de teste.

## Critérios de pronto

- todos os arquivos salvos e versionados;
- links cruzados válidos;
- CSV abre com delimitador `;` e contém 40 linhas;
- nenhum nome de modelo aparece como regra permanente fora do Registry;
- nenhum gate histórico foi removido;
- nenhuma configuração operacional foi alterada;
- relatório final informa limitações e próximos passos.
