# Lote de NFS-e + boleto + remessa

## Padrão operacional

Hebert entrega uma lista de notas para emitir em lote. A skill transforma cada linha em um job individual e gera um pacote consolidado.

## Formatos aceitos

Preferência, nessa ordem:

1. `.xlsx` ou `.csv` com uma linha por nota.
2. `.json` com array de notas.
3. Texto/tabela colada no chat, se for pequeno.

## Campos mínimos por nota

| campo | obrigatório | exemplo |
|---|---:|---|
| cliente_slug | sim | cliente-exemplo |
| tomador_nome | sim | CLIENTE EXEMPLO LTDA |
| tomador_cnpj | sim | 00.000.000/0001-00 |
| tomador_endereco | sim | RUA EXEMPLO, 123 |
| tomador_cep | sim | 00000000 |
| tomador_cidade | recomendado | VITORIA |
| tomador_uf | recomendado | ES |
| competencia | sim | 06/2026 |
| data_emissao | sim | 16/06/2026 |
| codigo_tributacao | sim | 010701 |
| valor_total | sim | 18004,19 |
| vencimento | sim | 20/06/2026 |
| numero_documento | sim | 105601 |
| nosso_numero | sim | 1533 |
| seq_remessa | sim | 0000084 |
| descricao_servico | sim | texto livre ou referência aos itens |
| itens_json | opcional | lista detalhada dos itens |
| email_tomador | opcional | financeiro@cliente.com |

## CSV exemplo

```csv
cliente_slug,tomador_nome,tomador_cnpj,tomador_endereco,tomador_cep,tomador_cidade,tomador_uf,competencia,data_emissao,codigo_tributacao,valor_total,vencimento,numero_documento,nosso_numero,seq_remessa,descricao_servico,email_tomador
cliente-exemplo,CLIENTE EXEMPLO LTDA,00.000.000/0001-00,"RUA EXEMPLO, 123, CENTRO",00000000,VITORIA,ES,06/2026,16/06/2026,010701,"585,00",30/06/2026,105600,1500,0000080,"Serviços de infraestrutura e monitoramento",financeiro@clienteexemplo.com.br
```

## Saída esperada

Para cada nota:

- Pacote individual em `/data/.openclaw/workspace-darth-vader/boletos/pacotes-emissao/`.
- Status individual.
- Boleto PDF/HTML de homologação/conferência.
- Remessa CNAB400 individual ou item dentro de remessa consolidada, conforme estratégia do lote.

Para o lote:

- `status-lote.md` com sucesso, falha e pendências por cliente.
- Pasta única do lote em `/data/.openclaw/workspace-darth-vader/boletos/lotes-emissao/YYYYMMDD-HHMMSS/`.
- Arquivo `.zip` opcional para entrega.

## Estratégia de remessa

Padrão recomendado: gerar uma remessa consolidada com múltiplos detalhes quando o lote for para o mesmo banco/conta/carteira/data de gravação.

Gerar remessas separadas quando:

- houver bancos/contas/carteiras diferentes;
- o Hebert pedir separação por cliente;
- algum título precisar de instrução bancária diferente.

## Travas

- Não emitir produção automaticamente.
- Notaas em homologação pode emitir lote de teste se Hebert autorizar.
- Se faltar campo obrigatório, marcar linha como `bloqueada` e seguir as demais quando for seguro.
- Não inventar nosso número, documento ou sequencial. Se faltar, pedir ou calcular apenas quando houver regra aprovada.

## E-mail automático para cliente

Ao final do pacote, se a NFS-e real tiver PDF/XML no job, gerar rascunho de e-mail para os e-mails financeiros do cadastro ou `email_tomador`.

- Saída por pacote: `email-nfse-cliente.eml` e `email-nfse-cliente.json`.
- Layout padrão: HTML Bikon em `templates/email_nfse_bikon.html` com fallback texto simples.
- Envio real só com aprovação explícita do Hebert.
- Se faltar e-mail financeiro, marcar a linha como pendência cadastral para envio.

## Agrupamento por cliente

Se o lote tiver duas ou mais emissões para o mesmo `cliente_id`, CPF/CNPJ ou documento do tomador, preparar um único e-mail para esse cliente.

Regra:

- Um e-mail por cliente, mesmo quando houver duas ou mais notas e boletos no mesmo envio.
- Corpo do e-mail lista cada NFS-e com número, chave, valor e boleto relacionado.
- Anexos incluem todos os PDFs/XMLs das NFS-e e todos os boletos PDF daquele cliente.
- Usar `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/preparar_emails_lote_clientes.py` quando houver lista de jobs já emitidos.
- Em teste controlado, usar destinatário explícito e não buscar cadastro financeiro automaticamente.
