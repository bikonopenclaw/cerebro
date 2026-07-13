---
name: "conciliacao-bancaria-assistida"
description: "Fila de excecoes e entrevista para conciliar extratos"
---

# Conciliacao Bancaria Assistida

## Quando Usar

Use esta skill quando houver extrato bancario, OFX, CSV, retorno bancario, movimentacao sem classificacao ou fechamento financeiro que precise identificar receita, despesa, transferencia, imposto, tarifa, ajuste ou baixa.

A skill pertence operacionalmente ao Darth Vader. Puppet Master coordena, prioriza e consolida para Hebert.

## Objetivo

Transformar conciliacao bancaria em processo assistido:

1. Importar movimentacoes.
2. Classificar automaticamente o que ja tem regra.
3. Separar desconhecidos em fila de excecoes.
4. Entrevistar Hebert apenas sobre lacunas reais.
5. Registrar a resposta como rascunho validado.
6. Criar regra reaproveitavel quando Hebert aprovar.

O ganho esperado e reduzir perguntas repetidas ao longo dos meses. Cada resposta de Hebert deve virar regra operacional quando fizer sentido.

## Travas

- Nao emitir NFS-e.
- Nao gerar boleto real.
- Nao gerar remessa de producao.
- Nao baixar titulo definitivamente.
- Nao executar pagamento.
- Nao alterar saldo bancario manualmente.
- Nao criar regra permanente sem confirmacao explicita.
- Nao gravar classificacao definitiva quando a confianca for baixa.
- Comunicacao externa, envio de boleto/NFS-e/remessa e impacto financeiro real exigem aprovacao explicita de Hebert.

## Fontes De Dados

Prioridade de leitura:

1. Extrato OFX/CSV importado.
2. Retorno bancario CNAB quando houver.
3. Banco financeiro do Darth Vader.
4. Tabelas de NFS-e, boletos, remessas, retornos e clientes.
5. Regras de classificacao ja aprovadas.
6. Historico de excecoes resolvidas.

## Modelo De Raciocinio

Para cada movimento bancario:

1. Normalizar data, valor, historico, documento, identificador e conta.
2. Procurar casamento direto:
   - boleto liquidado;
   - NFS-e recebida;
   - retorno bancario;
   - fornecedor recorrente;
   - tarifa bancaria;
   - transferencia entre contas;
   - imposto recorrente;
   - estorno ou ajuste.
3. Atribuir confianca:
   - `alta`: regra aprovada e dados batem.
   - `media`: padrao provavel, mas falta confirmacao.
   - `baixa`: desconhecido ou ambiguo.
4. Movimentos de confianca alta podem gerar sugestao automatica.
5. Movimentos de confianca media ou baixa entram na fila de entrevista.

## Fila De Excecoes

Cada excecao deve ter:

- id interno;
- data;
- valor;
- tipo de movimento: credito ou debito;
- historico bancario original;
- conta bancaria;
- possivel contraparte;
- sugestao do agente, se houver;
- nivel de confianca;
- pergunta para Hebert;
- status: `pendente`, `respondido`, `rascunho`, `aprovado`, `descartado`.

## Entrevista Guiada

A entrevista deve ser curta e orientada por opcoes.

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

## Saida Para Hebert

Quando pedir uma decisao, usar formato curto:

```text
Movimento desconhecido:
Data: {{data}}
Valor: {{valor}}
Historico: {{historico}}
Sugestao: {{sugestao}} (confianca {{nivel}})

Escolha:
1. {{opcao_1}}
2. {{opcao_2}}
3. {{opcao_3}}
4. Outro
```

Quando fechar lote:

```text
Conciliação assistida
1. Classificados automaticamente: {{n}}
2. Resolvidos por entrevista: {{n}}
3. Pendentes: {{n}}
4. Regras novas propostas: {{n}}
5. Precisa aprovação: {{lista_curta}}
```

## Registro De Regra

Uma regra aprovada deve conter:

- padrao de historico bancario;
- natureza;
- categoria;
- contraparte;
- centro de custo, se aplicavel;
- competencia padrao;
- limite de valor ou tolerancia, se houver;
- origem da aprovacao: Hebert;
- data da aprovacao;
- exemplos de movimentos usados.

## Criterio De Pronto

A skill esta pronta quando Darth Vader consegue:

- importar extrato;
- separar desconhecidos;
- entrevistar Hebert com opcoes claras;
- gerar rascunho de classificacao;
- propor regras novas;
- manter tudo travado ate aprovacao quando houver impacto definitivo.

## Regra De Postura

Nao transformar Hebert em digitador de planilha. Perguntar so o que o sistema nao sabe inferir com seguranca. Toda pergunta deve melhorar a automacao futura.
