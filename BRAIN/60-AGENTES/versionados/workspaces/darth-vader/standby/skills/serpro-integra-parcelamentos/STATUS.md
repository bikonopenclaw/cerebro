# Status do projeto, SERPRO Integra Contador / Parcelamentos

## 2026-07-02, retomada controlada com broker local

Projeto saiu do standby absoluto para retomada experimental controlada.

Modelo aprovado:
- certificado A1 permanece somente no Mac/host do Hebert;
- senha digitada localmente, não salva;
- broker local em `127.0.0.1` gera tokens temporários;
- OpenClaw/servidor não recebe certificado, senha nem token colado em chat;
- somente consultas liberadas nesta fase.

Validações realizadas com sucesso:

1. Broker local gerou token SERPRO com certificado A1 local.
2. `POST /Consultar`, `PARCSN PEDIDOSPARC163`, HTTP 200.
3. `POST /Consultar`, `PARCSN OBTERPARC164`, HTTP 200 para `numeroParcelamento=2`.
4. `POST /Consultar`, `PARCSN PARCELASPARAGERAR162`, HTTP 200.

Descobertas de payload:

- `PEDIDOSPARC163`: usar `pedidoDados.dados` como string vazia `""`.
- `OBTERPARC164`: usar `pedidoDados.dados` como string JSON com `numeroParcelamento`, exemplo `{"numeroParcelamento": 2}`.
- `PARCELASPARAGERAR162`: usar `pedidoDados.dados` como string vazia `""`.

Resultado operacional:

- Parcelamento nº 2 está em parcelamento.
- Valor consolidado: R$ 34.622,89.
- 24 parcelas.
- Parcelas disponíveis em 2026-07-02: 202604, 202605 e 202606, cada uma de R$ 1.536,24.
- Hebert informou que as três parcelas já foram pagas e devem baixar até 03/07/2026.

Arquivos principais:

- `broker-local/serpro_cert_broker.py`
- `broker-local/consultar_parcsn_pedidos.sh`
- `broker-local/consultar_parcsn_obter.sh`
- `broker-local/consultar_parcsn_parcelas.sh`
- `COMANDOS-VALIDOS-20260702.md`
- `FLUXO-APROVACAO-GERARDAS161.md`

Travas mantidas:

- Não chamar `/Emitir`.
- Não chamar `GERARDAS161`.
- Não gerar DAS real sem aprovação explícita do Hebert.
- Não colar token, certificado, senha ou retorno fiscal bruto no chat.

Próximo passo conservador:

- Em 03/07/2026, consultar novamente `PARCELASPARAGERAR162` e/ou `OBTERPARC164` para verificar baixa das parcelas pagas.
- Se necessário, mapear e testar `DETPAGTOPARC165`, ainda via `/Consultar`.

## 2026-07-03, catálogo oficial revisado e implantação v5
- Catálogo oficial Integra Contador revisado e registrado em `REFERENCIAS.md`.
- Direção operacional: estabilizar PARCSN completo primeiro; depois avaliar `PAGTOWEB PAGAMENTOS71`, consultas PGDASD, SICALC consolidação, Caixa Postal/DTE e procurações.
- Pacote local v5 preparado em `/data/.openclaw/workspace/entregas/serpro-parcsn-local-v5-20260703.tar.gz` com resumo amigável no final das consultas.
- Regra mantida: `/Emitir` e `GERARDAS161` continuam bloqueados sem aprovação explícita do Hebert.
