---
name: "conciliacao-bancaria-assistida"
description: "Concilia extratos com excecoes e aprovacoes"
---

# Conciliacao Bancaria Assistida

## Quando Usar

Use esta skill quando houver extrato bancario, OFX, CSV, retorno bancario, movimentacao sem classificacao ou fechamento financeiro que precise identificar receita, despesa, transferencia, imposto, tarifa, ajuste ou baixa.

A skill pertence operacionalmente ao Darth Vader. Puppet Master coordena, prioriza e consolida para Hebert.

## Objetivo

Transformar conciliacao bancaria em processo assistido e auditavel:

1. Importar movimentacoes.
2. Normalizar cada movimento com ID unico.
3. Classificar automaticamente apenas o que tiver regra aprovada e confianca alta.
4. Separar desconhecidos em fila de excecoes.
5. Entrevistar Hebert somente sobre lacunas reais.
6. Registrar resposta como rascunho validado.
7. Propor regra reaproveitavel quando fizer sentido.
8. Gravar definitivo somente com aprovacao explicita.

O ganho esperado e reduzir perguntas repetidas ao longo dos meses sem trocar seguranca financeira por velocidade.

## Modos Operacionais

A skill opera em quatro modos. Informar o modo antes de executar.

### 1. `analisar`

Permitido:

- ler extrato;
- normalizar movimentos;
- identificar duplicidades;
- sugerir classificacoes;
- montar fila de excecoes;
- gerar relatorio de pendencias.

Proibido:

- gravar classificacao definitiva;
- criar regra permanente;
- baixar titulo;
- alterar banco financeiro de producao.

### 2. `entrevistar`

Permitido:

- perguntar lacunas a Hebert;
- apresentar opcoes numeradas;
- registrar resposta como rascunho;
- manter pendente quando Hebert responder `nao sei agora`.

Proibido:

- transformar resposta em regra permanente sem confirmacao;
- inferir aprovacao por silencio;
- fazer mais de uma pergunta por movimento quando uma bastar.

### 3. `propor-regra`

Permitido:

- montar regra candidata;
- anexar exemplos e evidencias;
- explicar risco e escopo;
- pedir aprovacao explicita.

Proibido:

- ativar regra automaticamente;
- aplicar regra em lote sem autorizacao;
- expandir escopo alem do aprovado.

### 4. `gravar-definitivo`

Permitido somente com aprovacao explicita de Hebert para a acao especifica.

Mesmo com confianca alta, gravacao definitiva, baixa, regra permanente, alteracao em banco financeiro, remessa, boleto, NFS-e ou impacto financeiro real continuam bloqueados sem aprovacao.

## Travas

- Nao emitir NFS-e.
- Nao gerar boleto real.
- Nao gerar remessa de producao.
- Nao baixar titulo definitivamente.
- Nao executar pagamento.
- Nao alterar saldo bancario manualmente.
- Nao criar regra permanente sem confirmacao explicita.
- Nao gravar classificacao definitiva quando a confianca for baixa ou media.
- Nao gravar classificacao definitiva sem modo `gravar-definitivo` aprovado.
- Comunicacao externa, envio de boleto/NFS-e/remessa e impacto financeiro real exigem aprovacao explicita de Hebert.

## Fontes De Dados

Prioridade de leitura:

1. Extrato OFX/CSV importado.
2. Retorno bancario CNAB quando houver.
3. Banco financeiro do Darth Vader.
4. Tabelas de NFS-e, boletos, remessas, retornos e clientes.
5. Regras de classificacao ja aprovadas.
6. Historico de excecoes resolvidas.

## ID Unico De Movimento

Cada movimento deve receber `movimento_id` deterministico antes de qualquer classificacao.

Composicao recomendada:

`{{conta}}|{{data}}|{{valor}}|{{historico_normalizado}}|{{documento_ou_id_bancario}}`

Se o banco fornecer identificador unico confiavel, incluir esse identificador na composicao.

Antes de classificar ou perguntar, verificar se o `movimento_id` ja existe na fila, no historico de excecoes ou em classificacao anterior. Se existir, nao duplicar. Atualizar status ou apontar conflito.

## Modelo De Raciocinio

Para cada movimento bancario:

1. Normalizar data, valor, historico, documento, identificador, conta e tipo: credito ou debito.
2. Gerar `movimento_id`.
3. Procurar duplicidade pelo ID e por valor/data/historico parecidos.
4. Procurar casamento direto:
   - boleto liquidado;
   - NFS-e recebida;
   - retorno bancario;
   - fornecedor recorrente;
   - tarifa bancaria;
   - transferencia entre contas;
   - imposto recorrente;
   - estorno ou ajuste.
5. Registrar evidencias da sugestao.
6. Atribuir confianca:
   - `alta`: regra aprovada e dados batem;
   - `media`: padrao provavel, mas falta confirmacao;
   - `baixa`: desconhecido, ambiguo ou com dados insuficientes.
7. Confianca alta pode gerar sugestao automatica, mas nao gravacao definitiva sem aprovacao.
8. Confianca media ou baixa entra na fila de excecoes.

## Fila De Excecoes

Cada excecao deve ter:

- `movimento_id`;
- data;
- valor;
- tipo de movimento: credito ou debito;
- historico bancario original;
- historico normalizado;
- conta bancaria;
- possivel contraparte;
- sugestao do agente, se houver;
- evidencias da sugestao;
- dado faltante ou motivo da duvida;
- nivel de confianca;
- risco se classificar errado;
- pergunta para Hebert;
- status: `pendente`, `respondido`, `rascunho`, `aprovado`, `descartado`, `duplicado`.

## Entrevista Guiada

A entrevista deve ser curta, orientada por opcoes e sempre referenciar o `movimento_id`.

Usar o template:

`templates/pergunta-excecao-financeira.md`

### Pergunta 1: natureza

Opcoes padrao:

- Receita de cliente.
- Despesa operacional.
- Imposto/tributo.
- Tarifa bancaria.
- Transferencia entre contas.
- Pro-labore/distribuicao.
- Estorno/ajuste.
- Nao sei agora.

### Pergunta 2: categoria

Aparece conforme a natureza.

Para despesa operacional:

- Software/SaaS.
- Internet/telefonia.
- Fornecedor tecnico.
- Servico profissional.
- Banco/tarifa.
- Marketing/vendas.
- Administrativo.
- Outros.

Para receita:

- Mensalidade/contrato.
- Projeto avulso.
- Reembolso.
- Juros/multa.
- Ajuste de recebimento.
- Outros.

### Pergunta 3: contraparte

Perguntar cliente, fornecedor ou pessoa relacionada. Se houver sugestao por historico, apresentar a sugestao primeiro.

### Pergunta 4: competencia

Opcoes:

- Mes do pagamento.
- Mes anterior.
- Proximo mes.
- Competencia especifica.
- Ratear em mais de um mes.

### Pergunta 5: regra futura

Opcoes:

- Aplicar so neste lancamento.
- Criar regra para historico igual.
- Criar regra para contraparte e valor parecido.
- Criar regra para contraparte, qualquer valor.
- Nao criar regra ainda.

## Registro De Regra

Toda regra candidata deve usar o template:

`templates/regra-classificacao.json`

Uma regra aprovada deve conter:

- id da regra;
- padrao de historico bancario;
- natureza;
- categoria;
- contraparte;
- centro de custo, se aplicavel;
- competencia padrao;
- limite de valor ou tolerancia, se houver;
- escopo de aplicacao;
- status: `candidata`, `aprovada`, `ativa`, `rejeitada`;
- origem da aprovacao: Hebert;
- data da aprovacao;
- mensagem ou registro que aprovou;
- exemplos de movimentos usados;
- evidencias.

## Saida Para Hebert

Quando pedir uma decisao, usar formato curto:

```text
Movimento desconhecido: {{movimento_id}}
Data: {{data}}
Valor: {{valor}}
Historico: {{historico}}
Conta: {{conta}}
Sugestao: {{sugestao}} (confianca {{nivel}})
Motivo da duvida: {{motivo}}
Risco: {{risco}}

Responda com o numero:
1. {{opcao_1}}
2. {{opcao_2}}
3. {{opcao_3}}
4. Outro
```

Quando fechar lote:

```text
Conciliacao assistida
1. Classificados como sugestao: {{n}}
2. Resolvidos por entrevista: {{n}}
3. Pendentes: {{n}}
4. Duplicados/conflitos: {{n}}
5. Regras novas propostas: {{n}}
6. Precisa aprovacao: {{lista_curta}}
```

## Criterio De Pronto

A skill esta pronta quando Darth Vader consegue:

- importar extrato;
- gerar ID unico por movimento;
- separar desconhecidos;
- evitar duplicidade;
- entrevistar Hebert com opcoes claras;
- registrar rascunho de classificacao;
- propor regras novas com evidencias;
- manter tudo travado ate aprovacao quando houver impacto definitivo.

## Regra De Postura

Nao transformar Hebert em digitador de planilha. Perguntar so o que o sistema nao sabe inferir com seguranca.

Toda pergunta deve melhorar a automacao futura. Toda gravacao definitiva deve preservar caixa, historico financeiro e rastreabilidade.
