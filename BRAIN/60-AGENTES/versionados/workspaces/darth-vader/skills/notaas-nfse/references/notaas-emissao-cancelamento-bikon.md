# Notaas, emissão e cancelamento NFS-e, guia operacional Bikon

Fonte oficial: https://docs.notaas.com.br
Consulta feita em: 2026-07-01

## Base da API

- Base URL: `https://platform.notaas.com.br/api/v1`
- Autenticação: header `x-api-key`
- Operações fiscais reais exigem confirmação explícita do Hebert no processo Bikon.

## Emissão individual, POST /emitir

A emissão é assíncrona.

Fluxo correto:

1. Enviar `POST /emitir`.
2. A API retorna HTTP `202 Accepted` com `invoiceId`, `status: queued` e `pollUrl`.
3. Fazer polling em `GET /invoices/{invoiceId}/status` até:
   - `issued`: nota emitida;
   - `error`: falha fiscal/técnica;
   - `cancelled`: nota cancelada.
4. Depois de `issued`, baixar XML e PDF.

Campos principais do payload:

- `tomador.cnpj` ou `tomador.cpf`: obrigatório usar um deles, só dígitos.
- `tomador.nome`: obrigatório.
- `tomador.email`: opcional. No processo Bikon, omitir na emissão para evitar disparo automático pela plataforma. E-mail ao cliente é etapa separada.
- `tomador.endereco`: recomendado/obrigatório quando disponível no cadastro Bikon. Se informado, cidade e UF precisam estar corretas para resolução IBGE.
- `servico.descricao`: obrigatório.
- `servico.codigo`: código LC 116 com 6 dígitos numéricos. Exemplo Bikon: `010701`.
- `valores.total`: obrigatório, em reais.
- `valores.aliquotaIss`: obrigatório, em percentual. Exemplo: `5` para 5%.
- `valores.issRetido`: opcional, default `false`.
- `competencia`: opcional no formato `YYYY-MM`, mas no processo Bikon deve sempre ser enviado explicitamente.
- `referencia`: opcional, útil para idempotência/rastreamento interno quando adotarmos.

## Status, GET /invoices/{id}/status

Status esperados:

- `queued`
- `processing`
- `issued`
- `error`
- `cancelled`

Quando `issued`, podem aparecer:

- `chNFSe`: chave/código de verificação.
- `numeroNfe`: número/chave textual retornada pela API.
- `emittedAt`: timestamp da emissão.
- `ambiente`: `producao` ou `homologacao`.
- `pdfUrl`: URL pública CDN do PDF quando o documento estiver cacheado.
- `xmlUrl`: URL pública CDN do XML quando cacheado.
- `documentsCached`: `true` quando documentos foram armazenados no CDN.

Observação prática Bikon:

- No lote 092, a API retornou `documentsCached: true` e `xmlUrl`, mas algumas respostas não trouxeram `pdfUrl`, e o endpoint `/pdf` retornou `503`/`429` temporariamente.
- Portanto, para decidir envio ao cliente, validar arquivo PDF no disco, não apenas `issued`.

## XML, GET /invoices/{id}/xml

- Sem query: XML de emissão.
- Com `?type=cancel`: XML de cancelamento, disponível apenas para notas canceladas.

Comportamentos documentados:

- `302`: redireciona para CDN quando cacheado.
- `200 application/xml`: fallback direto quando não cacheado.
- `409`: invoice ainda não emitida/cancelada conforme o tipo pedido.
- `404`: XML não disponível.

Processo Bikon:

- XML é obrigatório antes de boleto/e-mail.
- Salvar XML localmente no pacote do lote.
- Para cancelamento, salvar também XML de cancelamento quando disponível.

## PDF, GET /invoices/{id}/pdf

Retorna DANFSE/PDF.

Comportamentos documentados:

- `302`: redireciona para CDN quando cacheado.
- `200 PDF`: fallback ao vivo conforme provedor municipal.
- `409`: nota ainda não emitida.
- `422`: dados insuficientes, certificado ausente ou chave inválida.
- `501`: sistema municipal não suporta download PDF.
- `502`: portal externo retornou erro.

Comportamento observado no lote 092:

- `503` e `429` podem acontecer temporariamente mesmo com nota `issued`.
- Deve haver retry espaçado.
- Não enviar e-mail ao cliente enquanto faltar PDF da NFS-e, salvo autorização explícita do Hebert para exceção.

## Webhooks úteis

Eventos Notaas:

- `nfse.issued`: nota emitida.
- `nfse.error`: falha de emissão.
- `nfse.cancelled`: cancelada.
- `nfse.documents_ready`: documentos cacheados.
- `batch.completed`: lote finalizado.

Ponto crítico sobre `nfse.documents_ready`:

- Pode disparar até 2 vezes para a mesma invoice.
- Primeira chamada pode vir `documentStatus: partial`, com XML pronto e `pdfUrl: null`.
- Segunda chamada pode vir até 10 minutos depois com `documentStatus: complete`, XML e PDF prontos.
- Se o retry esgotar sem sucesso, pode não haver novo webhook.

Processo Bikon:

- Mesmo com webhook, o checklist de envio deve verificar existência local de PDF + XML.
- Webhook é bom para reduzir polling, mas não substitui validação antes do e-mail.

## Lote, POST /emitir/batch

A Notaas suporta batch com `POST /emitir/batch`, retornando `batchId`.

Processo Bikon:

- Não usar batch cego para produção Bikon, salvo exceção explicitamente aprovada.
- Padrão Bikon é `scripts/emitir_lote_cadenciado.py`: 1 nota por vez, ciclo mínimo de 60s entre início de uma nota e início da próxima, aguardando `issued` + XML + PDF.

## Cancelamento, POST /cancelar

Cancelamento também é assíncrono.

Payload:

```json
{
  "invoiceId": "...",
  "motivo": "texto livre até 255 caracteres"
}
```

Regras Bikon:

1. Cancelamento fiscal real sempre exige autorização explícita do Hebert.
2. Antes de cancelar, conferir:
   - invoiceId;
   - número da NFS-e;
   - cliente/tomador;
   - valor;
   - motivo;
   - impacto em boleto/remessa/e-mail.
3. Rodar primeiro `--dry-run`.
4. Rodar real só com `--confirmar-cancelamento`.
5. Fazer polling até `cancelled` ou erro.
6. Baixar e arquivar XML de cancelamento com `GET /invoices/{id}/xml?type=cancel` quando disponível.
7. Não reemitir automaticamente. Reemissão é outra aprovação.

## Checklist Bikon antes de emitir

- Cadastro do tomador conferido por `cliente_id`, não só nome/documento.
- CPF/CNPJ válido.
- Endereço completo e cidade com acento/nome oficial quando necessário para IBGE.
- Competência explícita `YYYY-MM`.
- Serviço/código conferidos.
- Valor total aprovado pelo Hebert. Diferença item x total por desconto só é aceita se Hebert confirmar para o lote.
- E-mail do tomador omitido no payload fiscal, salvo decisão explícita.
- Emissão real aprovada no chat.

## Checklist após emissão

- Status `issued`.
- `invoiceId` salvo.
- Número/chave da NFS-e extraído do status/XML.
- XML baixado.
- PDF baixado.
- XML conferido: tomador, endereço, valor, serviço, competência.
- Só depois gerar boleto/remessa/e-mail.

## Checklist antes de e-mail

- PDF NFS-e anexado.
- XML NFS-e anexado.
- PDF boleto anexado quando houver boleto.
- Agrupar por `cliente_id`, não só CPF/CNPJ, para evitar misturar cadastros diferentes do mesmo documento, como Celi Aracruz e João Neiva.
- CC obrigatório: `financeiro@bikon.com.br`.
- Envio externo exige aprovação explícita.
