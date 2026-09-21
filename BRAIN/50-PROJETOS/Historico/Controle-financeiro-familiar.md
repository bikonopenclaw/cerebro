---
id: brain-1d17a713055824592c3c
type: state
title: Controle financeiro familiar — blueprint histórico
created: '2026-09-21T19:31:17.466455Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T19:50:50.519705Z'
---

# Controle financeiro familiar — blueprint histórico

Proposta importada em junho de2026. Implementação nesta VPS não comprovada; escopo distinto do FIP corporativo.

## Relações

- [[50-PROJETOS/README|Projetos]]
- [[60-AGENTES/DARTH-VADER|Darth Vader]] — contexto histórico de conciliação assistida.

## Complementos reconciliados — lote 8 de 2026-09-21

Blueprint familiar importado em28/06/2026 descreve nota fiscal→compra/cabeçalho+itens categorizados em transação e dashboard por categoria. Planejava ciclo orçamentário dia5 ao4 com tetos definidos no painel, e lista assistida alimentada pela família durante a compra, não automaticamente pela nota; cruzamento com nota seria opcional. Propunha usuário identificado, domínio familiar isolado e MFA, com stack Python/Flask/SQLite só de referência. Arquivo era estrutura sem dados pessoais; declarações de implementação pertencem ao Herald de origem, não provam implantação nesta VPS. Fonte: unidades 29795.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch8-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 9 de 2026-09-21

Blueprint histórico de controle financeiro familiar offline-first: SQLite local para categorias, compras/itens, contas/cartões/parcelas, orçamento/metas e conciliação; UI web local Flask/FastAPI, anexos locais e entrada manual. OCR local era opção limitada; IA online/sincronização seriam complementos opcionais. O JSON era desenho de produto, não código pronto nem implantação comprovada. Conectar à nota de menor privilégio que preserva a restrição histórica por IP da empresa; não inferir firewall aplicado. Fonte: unidades 29818.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch9-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 12 de 2026-09-21

O blueprint familiar propunha contas/carteiras, conciliação entre nota/boleto/comprovante/extrato/fatura, compra parcelada ligada às parcelas e visões separadas de caixa e competência. Incluía metas, recorrências esperadas, alertas acionáveis e fechamento mensal que separa gasto de reserva/investimento. Exemplos de6meses de reserva,80%do orçamento e3dias antes do vencimento eram sugestões de desenho, não parâmetros aprovados nem aconselhamento atual. Fonte: unidades 29806.

No desenho histórico local, bot e dashboard seriam serviços launchd separados, com logs próprios e dashboard em loopback. Reinício automático após login não oferece disponibilidade quando o Mac dorme; disponibilidade24x7 requer ambiente apropriado. Comandos/paths antigos e porta8765 eram exemplos, não instrução atual de instalação nem obrigação de manter arquivo de recuperação no Mac. Fonte: unidades 29995.

Auditoria proposta para o kit familiar incluía Telegram com allowlist de chat, validação de anexos sem executar conteúdo, dashboard loopback, segredos fora do código, integridade/duplicidade no SQLite e revisão humana antes de lançamento definitivo. No escopo auditado, OCR deveria ser local (AppleVision com Tesseract de fallback) sem enviar documentos financeiros a APIs externas; QR/chaveNFC-e era melhoria prioritária. Isso qualifica a opção genérica anterior de IA online: depende de mudança de escopo aprovada, não é default do kit privado. Fonte: unidades 30001.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch12-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 13 de 2026-09-21

No blueprint familiar proposto, despesa prevista não contava como realizada; compra precisava itens ou justificativa e reconciliação total×itens com tolerância explícita. Nota podia conferir lista de compras, sem alimentá-la automaticamente; ações tinham autoria e dados separados porfamília. Categoria Outros era fallback sujeito à revisão. Tetos/ciclo5→4, baixa colaborativa, histórico depreços e MFA eram desenho/roadmap, não implementação comprovada. Fonte: unidades 29798.

Auditoria histórica do kit familiar fase2 apontou bot fail-open quando allowlist vazia, OCR bloqueando eventloop/sem timeout, ausência do fluxo pendência→lançamento e dashboard contando pendências em fonte diferente do bot. Lições: mesma autoridade para fila/KPI; IDs de pendência não baseados em count+1; deduplicação por evidência; fechar conexãoSQLite explicitamente; upload limitado e OCR comtimeout; .env/dados foraGit. Trânsito Telegram permanece distinto de OCR local. VersõesdePython/pins e sugestões AppleVision eram avaliação antiga; checkpoint fase4 relata correções, sem presumir defeito atual. Fonte: unidades 30002.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch13-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 14 de 2026-09-21

Na expansão proposta dokit familiar, boleto era previsto; comprovante só mudaria para realizado após conciliar despesa, e extrato deveria deduplicar contra notas/boletos/comprovantes. Fatura detalhada era classificada porlançamento, não como despesaúnica adicional. Tiposreceita/despesa/reserva/investimento/transferência/ajuste e impactosorçamento/patrimônio eram eixos distintos. Baixaconfiança/beneficiário desconhecido/ambiguidade patrimonial exigiam pergunta; regra humanavalidada precedia inferência, sem promover toda ocorrência do merchant automaticamente. Fonte: unidades 29804.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch14-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
