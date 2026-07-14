# Carteira de cartórios atendidos, CNS por serventia

Handoff externo recebido do Herald OS em 2026-07-14. Fonte declarada: Postgres do Herald OS, schema `bikon`, ex-`pepper`, relatórios de verificação já ingeridos no acervo e arquivos do workspace `containers/Bikon/acervo/`. Nenhum CNS foi inferido.

## Carteira formal Provimento 213, 6 serventias

| Serventia | Apelido | Município/UF | CNS formatado | CNS numérico | Fonte do CNS | Situação Prov.213 |
|---|---|---|---|---|---|---|
| Registro Civil e Tabelionato da Sede, código TJES 720 | Cartório João Neiva | João Neiva/ES | 02.406-7 | 024067 | `containers/Bikon/acervo/verificacao-classe-joao-neiva-2026-07-14.md` §1 e §8.1, API CNJ HTTP 200, `bikon.acervo_cliente` código 26, id 14 | Classe 2, sem prorrogação, data-limite 22/07/2026, `core.prazo_legal` id=1, `verificacao='comprovada'` |
| Cartório do Único Ofício de São Domingos do Araguaia | Cartório Ferreira Rocha | São Domingos do Araguaia/PA | 06.700-9 | 067009 | `containers/Bikon/acervo/verificacao-classe-cartorios-pa-2026-07-14.md`, Bloco 2, citado em docs 941/945/946/947/953/956/957, API CNJ | Classe 3, prorrogação de 90 dias deferida e documentada, Decisão PJe nº 0002358-37.2026.2.00.0814 CGJ-PA, data-limite 21/08/2026, `core.prazo_legal` id=3, `verificacao='comprovada'` |
| Cartório do 1º Ofício de Notas e Registro de Imóveis de Marabá | RI Marabá | Marabá/PA | 12.963-5 | 129635 | `containers/Bikon/acervo/verificacao-classe-cartorios-pa-2026-07-14.md`, Bloco 1, docs 893/894/895, API CNJ | Classe 3, prorrogação requerida, deferimento não documentado no acervo, data-limite tratada como 21/08/2026 apenas em `core.prazo_legal` id=4, `verificacao='lembrada'` |
| Cartório do 3º Ofício Tabelionato de Notas da Comarca de Aracruz, código TJES 633 | Cartório Celi Cabral | Aracruz/ES | 02.387-9 | 023879 | `containers/Bikon/acervo/verificacao-classe-cartorios-es-2026-07-14.md` §3, PDF oficial TJES 16/01/2026, API CNJ, `bikon.acervo_documento` doc 1092 | Classe 3, prorrogação de 90 dias documentada, Decisão CGJ-ES SEI 7005394-59.2026.8.08.0000, data-limite 21/08/2026, `core.prazo_legal` id=2, `verificacao='comprovada'` |
| Cartório Capixaba, 4º Ofício de Notas de Vitória, código TJES 465 | Cartório Capixaba | Vitória/ES | 02.321-8 | 023218 | `containers/Bikon/acervo/verificacao-classe-cartorios-es-2026-07-14.md` §2, PDF oficial TJES 16/01/2026, API CNJ, `bikon.acervo_documento` doc 1091 | Classe 3, prorrogação de 90 dias documentada, Decisão CGJ-ES SEI 7005394-59.2026.8.08.0000, data-limite 21/08/2026, `core.prazo_legal` id=5, `verificacao='comprovada'` |
| Cartório do Terceiro Ofício de Cariacica, código TJES 655 | 3º Ofício de Cariacica, Cartório Alzira | Cariacica/ES | 02.368-9 | 023689 | `containers/Bikon/acervo/verificacao-classe-cartorios-es-2026-07-14.md` §1, PDF oficial TJES 16/01/2026, API CNJ, `bikon.acervo_documento` doc 1090 | Classe 3, prorrogação de 90 dias documentada, Decisão CGJ-ES SEI 7005394-59.2026.8.08.0000, data-limite 21/08/2026, `core.prazo_legal` id=6, `verificacao='comprovada'` |

## Mapeamento para cadastro operacional Darth Vader

Atualizado no cadastro ativo em `/data/.openclaw/workspace-darth-vader/cadastros/clientes/` em 2026-07-14:

| cliente_id | razão social no cadastro | CNS numérico |
|---|---|---|
| `alzira-maria-viana-135600` | ALZIRA MARIA VIANA | 023689 |
| `marcello-antonio-ferreira-rocha-039200` | MARCELLO ANTONIO FERREIRA ROCHA | 067009 |
| `marcos-alberto-pereira-santos-845172` | MARCOS ALBERTO PEREIRA SANTOS | 129635 |
| `celi-maria-guisso-cabral-311772` | CELI MARIA GUISSO CABRAL, Aracruz/ES | 023879 |
| `celi-maria-guisso-cabral-311772-29680-000-109-joao-neiva` | CELI MARIA GUISSO CABRAL, João Neiva/ES | 024067 |
| `marla-dayane-silva-camilo-849215` | MARLA DAYANE SILVA CAMILO | 023218 |

## Fora da carteira ativa Provimento 213

| Item | Situação | Regra de uso |
|---|---|---|
| Cartório 2º Ofício Vila Velha, código cliente `07`, `bikon.acervo_cliente.id=4` | CNS pendente, contrato encerrado em 28/06/2024 por solicitação do cliente, sem registro em `core.prazo_legal` | Não buscar CNS para carteira ativa sem ordem específica. Registrar apenas como histórico de acervo/contrato encerrado. |
| Cartório Camburi | Sem cadastro próprio em `bikon.acervo_cliente`, sem CNS localizado, documento avulso sob cliente `11 Grupo UNUS`; no painel Prov.213 consta como cliente somente do produto ARX Backup | Não tratar como cliente de adequação completa Prov.213. Usar apenas em relatórios de backup/ARX quando o pedido for desse escopo. |

## Pendências e cautelas

1. Cartório 2º Ofício Vila Velha: CNS não localizado e contrato encerrado. Transparência histórica, sem ação ativa recomendada.
2. Cartório Capixaba: requerimento de prorrogação tinha campo CNS em branco, mas o CNS da serventia está confirmado por PDF TJES e API CNJ.
3. RI Marabá: CNS confirmado, mas deferimento da prorrogação não documentado no acervo. Sinalizar como lacuna documental em relatórios.
4. Cartório Camburi: sem CNS localizado e fora da adequação completa, por decisão do dono. Não promover para carteira Prov.213.

## Regras

- Não inferir CNS.
- Não usar esta referência para criar cliente financeiro novo.
- Não classificar item fora da carteira como cliente Prov.213 ativo sem aprovação explícita do Hebert.
- Para relatório externo, citar fonte interna e, quando necessário, preparar evidência CNJ atualizada antes do envio.
