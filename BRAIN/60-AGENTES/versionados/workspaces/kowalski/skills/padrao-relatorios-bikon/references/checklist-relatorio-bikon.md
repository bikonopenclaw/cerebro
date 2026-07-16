# Checklist de relatório Bikon

## Quando usar skill específica junto

- NinjaOne, RMM, inventário, offline, alertas, EOL: usar `ninjaone-relatorios` para dados e esta skill para padrão final.
- Backup ARX: usar `arx-backup` para dados/modelo operacional e esta skill para linguagem, autoria e revisão final.
- Provimento CNJ 213/2026: usar `provimento-213-2026` para checklist técnico e esta skill para acabamento Bikon.
- Relatório novo sem skill própria: usar esta skill como base e criar skill específica só se virar rotina com regra própria.

## Checklist editorial

- [ ] Título diz o que o relatório entrega.
- [ ] Cliente, período/data e escopo estão claros.
- [ ] Resumo executivo cabe em até 8 linhas.
- [ ] Status geral está coerente com os achados.
- [ ] Achados estão ordenados por criticidade/impacto.
- [ ] Recomendações são acionáveis.
- [ ] Não há promessa exagerada nem conclusão sem evidência.
- [ ] Português BR direto, sem formalismo inútil.
- [ ] Não usa travessão.

## Checklist visual

- [ ] Logo Bikon aplicado.
- [ ] Paleta Bikon aplicada.
- [ ] Cards, tabelas e badges legíveis.
- [ ] Sem aparência de export bruto de ferramenta.
- [ ] Sem cabeçalho/rodapé automático de navegador.
- [ ] Sem caminho local, `file://`, metadado de impressão ou comentário operacional.

## Checklist de autoria

- [ ] Documento externo não cita OpenClaw, Puppet Master, Kowalski, Darth Vader ou Robotnik.
- [ ] Assinatura institucional usa Bikon Tecnologia.
- [ ] Solicitante correto: `Hebert Mattedi` ou `Hebert Mattedi e Felipe Nogueira`.

## Checklist de segurança

- [ ] Sem credencial, token, chave, senha, segredo ou `.env`.
- [ ] Sem dados brutos desnecessários de cliente.
- [ ] Sem arquivo temporário ou rascunho sujo.
- [ ] Se houver recomendação com custo, impacto externo ou comunicação para cliente, houve aprovação necessária.

## Estrutura recomendada por tipo

### Relatório executivo
1. Capa.
2. Resumo executivo.
3. Indicadores principais.
4. Riscos e impactos.
5. Recomendações.
6. Próximos passos.

### Relatório técnico operacional
1. Capa.
2. Escopo.
3. Ambiente analisado.
4. Achados técnicos.
5. Evidências.
6. Plano de ação.
7. Anexos, só se úteis.

### Parecer técnico
Usar o modelo aprovado de parecer técnico Bikon. Manter capa, cards, badges e padrão visual aprovados.

### Relatório EOL, End of Life, fim de vida ou obsolescência
Usar como base obrigatória:

- HTML: `/data/.openclaw/workspace-kowalski/identidade-visual/modelos-aprovados/eol/modelo-padrao-relatorio-eol-bikon.html`
- PDF referência: `/data/.openclaw/workspace-kowalski/identidade-visual/modelos-aprovados/eol/modelo-padrao-relatorio-eol-bikon.pdf`

Regras específicas:

- Aplicar o mesmo padrão para todos os clientes, sem exceção.
- Condensar por endpoint.
- Não duplicar máquina com EOL de hardware e software.
- Separar `Itens para cotação de compra` de `Ações internas de software`.
- Hardware EOL entra como substituição física/cotação.
- Software EOL vira plano interno Bikon.
- Se a mesma máquina tiver ambos, listar uma vez na cotação por causa do hardware e colocar software como observação.
- Não citar ferramenta interna sem necessidade. Preferir `Bikon RMM` quando aplicável.

### Relatório de cliente recorrente
Manter a mesma ordem e linguagem mês a mês para facilitar comparação.
