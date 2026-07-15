---
name: "consulta-cns-cartorio"
description: "Consulta CNS oficial no onboarding de cartórios"
---

# Consulta CNS de Cartório

## Objetivo

Usar esta skill quando um novo cliente, prospect ou cadastro operacional envolver cartório, serventia extrajudicial, tabelionato, registro civil, registro de imóveis, registro de títulos e documentos, protesto ou outro serviço notarial/registral regulado pelo CNJ.

A finalidade é orientar o agente a consultar dados oficiais pelo CNS, registrar evidências e evitar contaminação de cadastro por inferência de nome, município, titular ou similaridade com outro cartório.

Esta skill é de consulta, análise e preparação de evidência. Ela não autoriza alteração real em CRM, planilha, banco, arquivo operacional, proposta, contrato, relatório final, automação ou sistema de produção sem aprovação explícita do Hebert.

## Quando Usar

Use quando aparecerem pedidos ou contextos como:

- novo cliente cartório;
- onboarding de serventia;
- cadastro de cartório;
- qual é o CNS desse cartório;
- consultar Justiça Aberta;
- validar dados oficiais de serventia;
- enquadrar cartório para Provimento CNJ 213/2026;
- preparar evidência oficial de cartório.

Não use para empresas comuns, escritórios, CNPJs genéricos, clientes de TI que não sejam serventias extrajudiciais, ou qualquer caso em que o cliente não seja cartório/serventia.

## Regra de Ouro

O CNS vem do humano ou de fonte oficial confirmada. Nunca inferir CNS por nome, município, titular, CNPJ, apelido, cartório parecido ou histórico de outro cliente.

Nomes de cartório variam muito entre denominação fantasia, razão social, titular, interino, número do ofício e comarca. Um chute de CNS pode consultar a serventia errada e contaminar cadastro, faturamento, relatório, proposta e enquadramento regulatório.

Se o humano não tiver o CNS:

1. Não bloqueie o onboarding comercial/operacional.
2. Marque enriquecimento oficial por CNS como pendente.
3. Peça o CNS ao humano responsável.
4. Se usar fonte alternativa de Corregedoria, trate o resultado como CNS candidato, não como CNS confirmado.
5. Não grave conclusão definitiva baseada em CNS candidato.

## Consulta CNJ Justiça Aberta

Com CNS confirmado, consulte a API pública do CNJ Justiça Aberta.

Endpoint base:

```text
GET https://justicaabertaapi.cnj.jus.br/v1/api/serventias/{cns}
```

Regras obrigatórias:

- Remover pontuação do CNS antes da URL.
- Manter zeros à esquerda.
- Incluir sempre o segmento `/v1/`.
- Tratar `404` com CNS pontuado como possível erro de formatação.
- Tratar `404 {"message":"Rota não encontrada"}` como possível ausência do `/v1/` ou rota errada.
- Não usar rota de busca por nome/UF/município como substituto do CNS confirmado.

Exemplo validado em 2026-07-14:

```text
GET https://justicaabertaapi.cnj.jus.br/v1/api/serventias/024067
```

Retorno esperado: JSON com denominação, CNS, status, tipo, situação jurídica e atribuições da serventia.

## Subrotas Úteis

Use apenas quando necessário para o objetivo do onboarding ou diagnóstico.

```text
GET /v1/api/serventias/{cns}
GET /v1/api/serventias/{cns}/arrecadacoes?page=1&perPage=50
GET /v1/api/serventias/{cns}/dados-complementares
GET /v1/api/serventias/{cns}/localizacao
GET /v1/api/serventias/{cns}/responsaveis
```

Uso típico:

- Raiz: identidade oficial, CNS, status e situação jurídica.
- `/responsaveis`: titular, interino, situação do responsável e data de ingresso.
- `/localizacao`: endereço oficial.
- `/arrecadacoes`: histórico de arrecadação por período, quando o caso exigir análise regulatória ou financeira.
- `/dados-complementares`: dados cadastrais adicionais, quando necessários.

## Situação Jurídica VAGO

Se `situacao_juridica_cartorio` vier como `VAGO`, não trate titular antigo como responsável atual.

Ação obrigatória:

1. Consultar `/responsaveis`.
2. Identificar o responsável ativo.
3. Se houver interino, registrar que a serventia está vaga e operada por interino.
4. Não presumir poder decisório sem confirmar interlocutor humano.

## Fonte Alternativa Quando Não Há CNS

Se o CNS não estiver disponível, a fonte alternativa aceitável é lista oficial de serventias da Corregedoria-Geral de Justiça do estado ou Tribunal de Justiça competente.

Regras:

- Cruzar pelo menos dois campos independentes, como número do ofício, município, titular/interino, endereço ou comarca.
- Registrar a fonte, URL ou arquivo consultado e data da consulta.
- Classificar o CNS encontrado como CNS candidato.
- Pedir confirmação ao humano antes de usar como fato fechado.
- Não consultar API CNJ com CNS candidato para gravar cadastro definitivo sem aprovação humana.

Agregadores comerciais, diretórios privados e páginas não oficiais só servem como pista. Nunca prevalecem sobre CNJ ou Corregedoria.

## Hierarquia de Fontes

Quando houver conflito, use esta ordem:

1. API pública do CNJ Justiça Aberta por CNS confirmado.
2. Lista oficial da Corregedoria estadual ou Tribunal competente.
3. Informação fornecida diretamente pelo humano responsável, quando acompanhada de contexto verificável.
4. Agregadores comerciais e páginas de terceiros apenas como pista.

Se duas fontes oficiais divergirem, registre conflito e escale ao Hebert ou ao humano responsável. Não escolha em silêncio.

## Provimento CNJ 213/2026 e Classe Regulatória

Classificação regulatória só pode ser feita quando o pedido exigir explicitamente adequação ao Provimento CNJ 213/2026 ou norma equivalente.

Regra dura: não classificar por analogia, porte percebido, cliente parecido, cidade, quantidade de atos ou opinião.

Antes de classificar, exigir:

1. Fonte oficial da norma vigente.
2. Tabela oficial de faixas, classes, prazos e critério de semestre de referência.
3. Data de acesso à norma.
4. Arrecadação real consultada em `/arrecadacoes`.
5. Indicação do período usado e justificativa.

Se a norma, tabela, prazos ou semestre de referência não estiverem disponíveis, entregue somente: dados consultados, lacuna de norma/fonte e recomendação de validação. Não invente classe.

Se a serventia estiver perto de uma fronteira entre classes, sinalize explicitamente como risco de oscilação. Não esconda a proximidade do limite.

Prorrogação de prazo só pode ser considerada se houver documento ou fonte oficial específica. Não presumir prorrogação automática.

## Evidência Obrigatória

Toda conclusão precisa ter evidência.

Ao consultar a API, preparar um pacote de evidência com:

- CNS consultado, com e sem pontuação se houver;
- URL chamada;
- data e hora da consulta;
- endpoint usado;
- JSON bruto retornado;
- resumo humano dos campos relevantes;
- observações sobre pendências, conflitos ou CNS candidato;
- fonte usada para qualquer dado externo à API.

A resposta bruta da API deve ser preservada como evidência preparada ou anexo interno. Não gravar automaticamente em CRM, banco, planilha, pasta operacional, relatório final ou cadastro real sem aprovação explícita do Hebert.

## Saída Esperada

Para resposta ao Hebert ou relatório de validação, usar formato curto:

```text
1. O que foi consultado: {{cartorio/CNS/fonte}}
2. O que foi confirmado: {{dados oficiais principais}}
3. Pendências/riscos: {{CNS candidato, conflito, norma ausente, classe não calculada}}
4. Próximo passo: {{pedir CNS, confirmar candidato, anexar evidência, validar norma}}
```

Para pacote técnico interno, incluir também:

```text
CNS: {{cns}}
Status CNJ: {{ativo/inativo}}
Situação jurídica: {{provido/vago}}
Responsável ativo: {{nome e condição}}
Endereço oficial: {{endereço}}
Arrecadação usada: {{período e valor, se aplicável}}
Fonte: {{URL/API/documento}}
Consulta em: {{timestamp}}
Evidência bruta: {{arquivo/anexo preparado}}
```

## Erros Comuns

| Sintoma | Causa provável | Correção |
|---|---|---|
| `404` consultando CNS | CNS enviado com ponto/traço | Remover pontuação e preservar zeros à esquerda |
| `404 {"message":"Rota não encontrada"}` | URL sem `/v1/` ou rota errada | Usar `/v1/api/serventias/{cns}` |
| `401` ou resposta pedindo login | Tentativa de busca/listagem, não ficha por CNS | Pedir CNS ao humano ou usar fonte oficial alternativa como candidato |
| Titular parece desatualizado | Cartório VAGO ou interino ativo | Consultar `/responsaveis` |
| Nome diverge entre fontes | Nome fantasia, razão social e titular variam | Confirmar identidade pelo CNS, não pelo nome |
| Classe Prov. 213 sugerida sem tabela oficial | Falta de fonte normativa | Não classificar, registrar lacuna |

## Travas

- Não inferir CNS.
- Não transformar CNS candidato em CNS confirmado.
- Não registrar conclusão sem evidência bruta.
- Não escrever em sistema real sem aprovação explícita.
- Não classificar Provimento 213 sem fonte oficial da norma vigente.
- Não usar agregador comercial como fonte final.
- Não ocultar conflito de fontes.
- Não tratar cartório vago como se tivesse titular formal ativo.

## Manutenção

Esta metodologia deve ser revisada se o CNJ alterar endpoint, autenticação, formato de resposta, campos de arrecadação, regra de responsáveis, ou se nova norma substituir/alterar o Provimento CNJ 213/2026.

Quando houver mudança de API ou norma, criar proposta de atualização da skill antes de aplicar alteração real.
