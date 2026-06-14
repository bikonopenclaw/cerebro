# Análise do arquivo de malote/remessa — exemplo 20260614-0223

Arquivo analisado: `exemplo-malote-20260614-0223-133_CNAB400_1008_27846.rem`

Hash SHA-256:
`9fbe62e26c54743b09b7477e3afa24d30e8c890da3d1682e70e9e5ff2448c9f8`

## Diagnóstico

- Tipo informado pelo nome: Cresol 133, CNAB 400, cooperativa 1008, conta 27846.
- Quantidade de linhas: 2.
- Tamanho das linhas: 400 posições cada.
- Codificação lida: UTF-8.
- Estrutura encontrada:
  - linha 1: registro tipo `0`, header.
  - linha 2: registro tipo `0`, não é detalhe `1` nem trailer `9`.

## Header identificado

| Campo | Posição | Valor |
|---|---:|---|
| Identificação do registro | 001-001 | `0` |
| Identificação arquivo remessa | 002-002 | `1` |
| Literal remessa | 003-009 | `REMESSA` |
| Código serviço | 010-011 | `01` |
| Literal serviço | 012-026 | `COBRANCA` |
| Código empresa/beneficiário | 027-046 | `00000000000000027846` |
| Nome empresa | 047-076 | vazio/brancos |
| Código banco | 077-079 | `133` |
| Nome banco | 080-094 | `Cresol` |
| Data gravação | 095-100 | vazio/brancos |
| Sequencial remessa | 111-117 | vazio/brancos |
| Sequencial registro | 395-400 | `000001` |

## Linha 2

| Campo | Posição | Valor |
|---|---:|---|
| Tipo de registro | 001-001 | `0` |
| Demais campos | 002-394 | brancos |
| Sequencial registro | 395-400 | `000002` |

## Comparação com remessa anterior válida

A remessa anterior `exemplo-malote-20260614-015740.rem` tinha:

- 3 linhas.
- Registro 0 header.
- Registro 1 detalhe com título.
- Registro 9 trailer.
- Dados preenchidos: Bikon, sequencial, carteira, cooperativa, conta, nosso número, vencimento, valor e sacado.

Este novo arquivo parece ser um esqueleto/template ou arquivo incompleto:

- Não tem registro detalhe tipo `1`.
- Não tem trailer tipo `9`.
- Header está sem nome da empresa, data de gravação e sequencial de remessa.
- A segunda linha começa com `0`, o que não fecha com a estrutura CNAB 400 esperada.

## Utilidade para a skill

Serve como referência negativa/teste de validação. A habilidade do Darth Vader deve rejeitar ou marcar como inválido arquivo CNAB 400 Cresol quando:

1. não houver header tipo `0`, detalhe tipo `1` e trailer tipo `9`;
2. existir mais de um registro tipo `0` sem justificativa;
3. header obrigatório estiver em branco;
4. não houver nenhum título na remessa.

## Conclusão

Este arquivo não ajuda a fechar posições 150-400 do detalhe, porque não contém registro detalhe preenchido. Mas é útil para montar validações de sanidade do gerador/importador de remessa.
