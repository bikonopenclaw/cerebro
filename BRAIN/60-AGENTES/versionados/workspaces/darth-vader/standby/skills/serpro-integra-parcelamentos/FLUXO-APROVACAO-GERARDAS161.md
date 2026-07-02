# Fluxo de aprovação, SERPRO PARCSN GERARDAS161

Status: proposta operacional
Dono: Darth Vader
Aprovador final: Hebert Mattedi ou Puppet Master com autorização explícita do Hebert
Escopo: emissão de DAS de parcela do parcelamento Simples Nacional Bikon via SERPRO Integra Contador

## Princípio

`GERARDAS161` é operação de impacto real. Não é teste técnico.

Só pode ser chamado depois de validação de contexto, conferência da parcela e aprovação explícita. A aprovação precisa citar a parcela e o valor.

## Travas obrigatórias

- Nunca chamar `/Emitir` em teste exploratório.
- Nunca emitir lote sem lista fechada de parcelas.
- Nunca emitir se houver divergência entre parcelas disponíveis e expectativa financeira.
- Nunca colar token, certificado, senha ou retorno fiscal bruto em chat.
- Broker local continua obrigatório para certificado A1.
- Resposta completa da SERPRO deve ficar local, fora do Brain/Git, com CNPJ mascarado em qualquer resumo.

## Estados do fluxo

1. `consulta`
   - Permitido: `PEDIDOSPARC163`, `OBTERPARC164`, `PARCELASPARAGERAR162`, `DETPAGTOPARC165`.
   - Proibido: `/Emitir`.

2. `pre-aprovacao`
   - Darth Vader consolida resumo:
     - parcelamento ativo;
     - parcelas disponíveis;
     - valor por parcela;
     - competência/parcela a emitir;
     - total previsto;
     - risco/reserva.
   - Puppet Master revisa e pergunta a Hebert se deve emitir.

3. `aprovado_para_emitir`
   - Aprovação precisa ter formato explícito:

```text
Aprovo emitir DAS PARCSN GERARDAS161 da Bikon para a parcela AAAAMM, valor R$ X.XXX,XX, parcelamento nº 2.
```

   - Aprovação genérica tipo “pode emitir” não basta.

4. `emitido`
   - Darth Vader executa uma única emissão aprovada.
   - Salva retorno/PDF/DAS localmente no workspace operacional, fora do Brain/Git.
   - Resume ao Puppet Master:
     - parcela emitida;
     - valor;
     - vencimento;
     - arquivo local gerado;
     - protocolo/identificador, se houver;
     - alerta de pagamento.

5. `bloqueado`
   - Qualquer inconsistência volta para consulta/pre-aprovação.

## Checklist antes de pedir aprovação

- [ ] Broker local funcionando.
- [ ] `PEDIDOSPARC163` confirmou parcelamento ativo.
- [ ] `OBTERPARC164` confirmou número do parcelamento e situação.
- [ ] `PARCELASPARAGERAR162` listou a parcela desejada.
- [ ] Valor da parcela confere com o esperado.
- [ ] Nenhuma chamada `/Emitir` foi feita ainda.
- [ ] Parcela e valor estão no pedido de aprovação.

## Critério para primeira emissão controlada

Na primeira execução real, emitir no máximo uma parcela.

Parcelas atualmente disponíveis no teste de 2026-07-02:

- 202604, R$ 1.536,24
- 202605, R$ 1.536,24
- 202606, R$ 1.536,24

Recomendação conservadora: emitir primeiro apenas a parcela mais antiga disponível, `202604`, se Hebert aprovar explicitamente.

## Mensagem de aprovação sugerida

```text
Hebert, confirme se aprova a emissão real do DAS via SERPRO:

Parcelamento: PARCSN nº 2
Parcela: 202604
Valor informado pela SERPRO: R$ 1.536,24
Operação: GERARDAS161 via POST /Emitir

Responda exatamente:
Aprovo emitir DAS PARCSN GERARDAS161 da Bikon para a parcela 202604, valor R$ 1.536,24, parcelamento nº 2.
```

## Pós-emissão

Depois da emissão:

- Salvar arquivo em pasta operacional local, não no Brain.
- Registrar resumo operacional sem token/segredo.
- Se houver PDF/linha digitável/código de barras, conferir antes de enviar ou pagar.
- Não enviar para cliente externo. Uso interno Bikon.
- Se for recorrente, criar rotina mensal com aprovação explícita a cada competência.
