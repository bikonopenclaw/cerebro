DROP VIEW IF EXISTS vw_financeiro_boletos;
DROP VIEW IF EXISTS vw_financeiro_contas_receber;
DROP VIEW IF EXISTS vw_financeiro_kpi_mensal;
DROP VIEW IF EXISTS vw_financeiro_clientes;
DROP VIEW IF EXISTS vw_financeiro_remessas;
DROP VIEW IF EXISTS vw_financeiro_retornos;

CREATE VIEW vw_financeiro_boletos AS
WITH base AS (
  SELECT
    b.id AS boleto_id,
    n.id AS nfse_id,
    c.id AS cliente_id,
    c.nome AS cliente,
    c.documento AS cliente_documento,
    n.numero AS nfse_numero,
    n.chave AS nfse_chave,
    n.invoice_id,
    CASE
      WHEN n.data_emissao LIKE '__/__/____'
        THEN substr(n.data_emissao, 7, 4) || '-' || substr(n.data_emissao, 4, 2) || '-' || substr(n.data_emissao, 1, 2)
      ELSE n.data_emissao
    END AS data_emissao,
    n.competencia,
    b.numero_documento,
    b.nosso_numero,
    b.nosso_numero_formatado,
    b.banco,
    b.carteira,
    b.cooperativa,
    b.conta,
    b.vencimento,
    b.data_pagamento,
    b.data_credito,
    b.status AS status_operacional,
    CASE
      WHEN COALESCE(b.valor_pago_centavos, 0) > 0 OR b.data_pagamento IS NOT NULL THEN 'baixado'
      WHEN b.vencimento < date('now') THEN 'vencido'
      ELSE 'em_aberto'
    END AS status_financeiro,
    b.valor_original_centavos,
    COALESCE(b.valor_pago_centavos, 0) AS valor_pago_centavos,
    b.valor_original_centavos - COALESCE(b.valor_pago_centavos, 0) AS saldo_centavos,
    b.juros_mora_centavos,
    b.multa_centavos,
    b.desconto_centavos,
    b.abatimento_centavos,
    b.tarifa_centavos,
    b.outras_despesas_centavos,
    b.outros_creditos_centavos,
    ROUND(b.valor_original_centavos / 100.0, 2) AS valor_original,
    ROUND(COALESCE(b.valor_pago_centavos, 0) / 100.0, 2) AS valor_pago,
    ROUND((b.valor_original_centavos - COALESCE(b.valor_pago_centavos, 0)) / 100.0, 2) AS saldo,
    CASE
      WHEN COALESCE(b.valor_pago_centavos, 0) > 0 OR b.data_pagamento IS NOT NULL THEN 0
      WHEN b.vencimento < date('now') THEN CAST(julianday(date('now')) - julianday(b.vencimento) AS INTEGER)
      ELSE 0
    END AS dias_atraso,
    strftime('%Y-%m', CASE
      WHEN n.data_emissao LIKE '__/__/____'
        THEN substr(n.data_emissao, 7, 4) || '-' || substr(n.data_emissao, 4, 2) || '-' || substr(n.data_emissao, 1, 2)
      ELSE n.data_emissao
    END) AS mes_emissao,
    strftime('%Y-%m', b.vencimento) AS mes_vencimento,
    r.seq_remessa,
    r.arquivo_path AS remessa_arquivo,
    b.linha_digitavel,
    b.codigo_barras,
    b.pdf_path AS boleto_pdf_path,
    n.pdf_path AS nfse_pdf_path,
    n.xml_path AS nfse_xml_path,
    b.pacote_path
  FROM boletos b
  LEFT JOIN nfse n ON n.id = b.nfse_id
  LEFT JOIN clientes c ON c.id = b.cliente_id
  LEFT JOIN remessa_boletos rb ON rb.boleto_id = b.id
  LEFT JOIN remessas r ON r.id = rb.remessa_id
)
SELECT * FROM base;

CREATE VIEW vw_financeiro_contas_receber AS
SELECT *
FROM vw_financeiro_boletos
WHERE status_financeiro IN ('em_aberto', 'vencido');

CREATE VIEW vw_financeiro_kpi_mensal AS
SELECT
  COALESCE(mes_emissao, mes_vencimento) AS mes,
  COUNT(DISTINCT cliente_id) AS clientes,
  COUNT(DISTINCT nfse_id) AS nfse,
  COUNT(*) AS boletos,
  SUM(valor_original_centavos) AS faturado_centavos,
  SUM(valor_pago_centavos) AS recebido_centavos,
  SUM(saldo_centavos) AS aberto_centavos,
  SUM(CASE WHEN status_financeiro = 'vencido' THEN saldo_centavos ELSE 0 END) AS vencido_centavos,
  ROUND(SUM(valor_original_centavos) / 100.0, 2) AS faturado,
  ROUND(SUM(valor_pago_centavos) / 100.0, 2) AS recebido,
  ROUND(SUM(saldo_centavos) / 100.0, 2) AS aberto,
  ROUND(SUM(CASE WHEN status_financeiro = 'vencido' THEN saldo_centavos ELSE 0 END) / 100.0, 2) AS vencido
FROM vw_financeiro_boletos
GROUP BY COALESCE(mes_emissao, mes_vencimento);

CREATE VIEW vw_financeiro_clientes AS
SELECT
  cliente_id,
  cliente,
  cliente_documento,
  COUNT(*) AS boletos,
  COUNT(DISTINCT nfse_id) AS nfse,
  MIN(data_emissao) AS primeira_emissao,
  MAX(data_emissao) AS ultima_emissao,
  SUM(valor_original_centavos) AS faturado_centavos,
  SUM(valor_pago_centavos) AS recebido_centavos,
  SUM(saldo_centavos) AS aberto_centavos,
  SUM(CASE WHEN status_financeiro = 'vencido' THEN saldo_centavos ELSE 0 END) AS vencido_centavos,
  ROUND(SUM(valor_original_centavos) / 100.0, 2) AS faturado,
  ROUND(SUM(valor_pago_centavos) / 100.0, 2) AS recebido,
  ROUND(SUM(saldo_centavos) / 100.0, 2) AS aberto,
  ROUND(SUM(CASE WHEN status_financeiro = 'vencido' THEN saldo_centavos ELSE 0 END) / 100.0, 2) AS vencido
FROM vw_financeiro_boletos
GROUP BY cliente_id, cliente, cliente_documento;

CREATE VIEW vw_financeiro_remessas AS
SELECT
  r.id AS remessa_id,
  r.seq_remessa,
  r.banco,
  r.layout,
  r.status,
  r.quantidade_titulos AS titulos_esperados,
  COUNT(rb.boleto_id) AS titulos_vinculados,
  r.valor_total_centavos AS valor_remessa_centavos,
  COALESCE(SUM(b.valor_original_centavos), 0) AS valor_boletos_centavos,
  ROUND(r.valor_total_centavos / 100.0, 2) AS valor_remessa,
  ROUND(COALESCE(SUM(b.valor_original_centavos), 0) / 100.0, 2) AS valor_boletos,
  CASE
    WHEN r.quantidade_titulos = COUNT(rb.boleto_id)
     AND r.valor_total_centavos = COALESCE(SUM(b.valor_original_centavos), 0)
      THEN 'ok'
    ELSE 'divergente'
  END AS status_conferencia,
  r.arquivo_path,
  r.pacote_path,
  r.criado_em,
  r.atualizado_em
FROM remessas r
LEFT JOIN remessa_boletos rb ON rb.remessa_id = r.id
LEFT JOIN boletos b ON b.id = rb.boleto_id
GROUP BY r.id;

CREATE VIEW vw_financeiro_retornos AS
SELECT
  ro.id AS ocorrencia_id,
  rt.id AS retorno_id,
  rt.arquivo_path,
  rt.data_arquivo,
  rt.data_credito AS retorno_data_credito,
  ro.boleto_id,
  b.numero_documento,
  b.nosso_numero,
  c.nome AS cliente,
  ro.ocorrencia_codigo,
  ro.ocorrencia_descricao,
  ro.data_ocorrencia,
  ro.vencimento,
  ro.valor_titulo_centavos,
  ro.valor_pago_centavos,
  ro.tarifa_centavos,
  ro.data_credito,
  ro.conciliado,
  ro.observacao,
  ROUND(COALESCE(ro.valor_titulo_centavos, 0) / 100.0, 2) AS valor_titulo,
  ROUND(COALESCE(ro.valor_pago_centavos, 0) / 100.0, 2) AS valor_pago,
  ROUND(COALESCE(ro.tarifa_centavos, 0) / 100.0, 2) AS tarifa
FROM retorno_ocorrencias ro
LEFT JOIN retornos rt ON rt.id = ro.retorno_id
LEFT JOIN boletos b ON b.id = ro.boleto_id
LEFT JOIN clientes c ON c.id = b.cliente_id;
